from uuid import UUID
import asyncpg
from typing import List, Any, Dict

db_pool: asyncpg.pool.Pool | None = None

def import_db_pool():
    global db_pool
    if db_pool is None:
        from .db import db_pool

async def fetch_user_profile(user_id: UUID) -> List[Dict[str, Any]]:
    """
    Возвращает развёрнутый профиль пользователя user_id.
    Результат — список словарей, каждая строка — отдельное сочетание данных.
    """
    sql = """
SELECT
    u.user_id,
    u.login,
    u.avatar,
    u.is_premium_user,

    -- Личные данные
    pdr.name            AS first_name,
    pdr.surname         AS last_name,
    pdr.gender,
    pdr.birth_date      AS date_of_birth,
    pdr.locality        AS locality,
    tz.utc_offset,
    tz.city             AS tz_city,

    -- Устройства
    d.device_id,
    d.device_type,
    d.device_name,
    d.os,
    d.os_version,
    d.last_login,
    d.last_ip,

    -- Водительское удостоверение
    dl.number           AS driver_license_number,
    dl.date_of_issue    AS dl_issue_date,
    dl.expiration_date  AS dl_expire_date,

    -- Паспорт
    ip.number           AS passport_number,
    ip.nationality,
    ip.expiration_date  AS passport_expire_date,

    -- Медицинские страховки
    cmi.number          AS compulsory_insurance_number,
    vmi.number          AS voluntary_insurance_number,

    -- Способы восстановления
    rm.method_type,
    pn.phone_number,
    be.email            AS backup_email,
    sq.question,
    sq.answer,

    -- Адреса и заметки по сервисам
    addr.address_id,
    addr.country,
    addr.city           AS addr_city,
    addr.street,
    addr.building,
    ua.address_type     AS addr_type,
    san.service_id,
    san.description     AS service_note

FROM users AS u
    LEFT JOIN personal_data_records AS pdr
        ON pdr.user_id = u.user_id
    LEFT JOIN time_zones AS tz
        ON tz.time_zone_id = pdr.time_zone_id

    LEFT JOIN devices AS d
        ON d.user_id = u.user_id

    LEFT JOIN driver_licenses AS dl
        ON dl.user_id = u.user_id

    LEFT JOIN international_passports AS ip
        ON ip.user_id = u.user_id

    LEFT JOIN compulsory_medical_insurances AS cmi
        ON cmi.user_id = u.user_id

    LEFT JOIN voluntary_medical_insurances AS vmi
        ON vmi.user_id = u.user_id

    LEFT JOIN recovery_methods AS rm
        ON rm.user_id = u.user_id
    LEFT JOIN phone_numbers AS pn
        ON pn.user_id = u.user_id
    LEFT JOIN backup_emails AS be
        ON be.user_id = u.user_id
    LEFT JOIN security_questions AS sq
        ON sq.user_id = u.user_id

    LEFT JOIN user_addresses AS ua
        ON ua.user_id = u.user_id
    LEFT JOIN addresses AS addr
        ON addr.address_id = ua.address_id
    LEFT JOIN service_address_notes AS san
        ON san.user_id = u.user_id
       AND san.addresses_id = addr.address_id

WHERE u.user_id = $1;
    """
    async with db_pool.acquire() as conn:
        records = await conn.fetch(sql, user_id)
        return [dict(rec) for rec in records]


async def fetch_device_activity(device_id: UUID) -> List[Dict[str, Any]]:
    """
    Возвращает историю активности для конкретного device_id за последние 7 дней,
    исключая action_name = 'VIEWED_PAGE'.
    """
    sql = """
SELECT
    ah.activity_id,
    ah.created_at      AS activity_time,

    -- Информация о пользователе
    u.user_id,
    u.login           AS user_login,

    -- Информация об устройстве
    d.device_id,
    d.device_type,
    d.device_name,

    -- Детали действия
    a.action_id,
    a.action_name,
    a.action_description,
    ah.details        AS action_details

FROM activity_history AS ah
    JOIN users AS u
        ON u.user_id = ah.user_id
    JOIN devices AS d
        ON d.device_id = ah.device_id
    JOIN actions AS a
        ON a.action_id = ah.action_id

WHERE
    ah.device_id = $1
    AND ah.created_at >= NOW() - INTERVAL '7 days'
    AND a.action_name != 'VIEWED_PAGE'
ORDER BY ah.created_at DESC;
    """
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(sql, device_id)
        return [dict(r) for r in rows]


async def fetch_open_support_sessions(agent_id: UUID) -> List[Dict[str, Any]]:
    """
    Возвращает все открытые сессии поддержки для заданного агента (agent_id),
    в которых хотя бы в одном сообщении реакция LIKE или DISLIKE.
    """
    sql = """
SELECT
    ss.session_id,
    ss.started_at,
    ss.session_status,

    -- Запросивший пользователь
    u.user_id        AS requester_id,
    u.login          AS requester_login,

    -- Агент
    sa.agent_id,
    sa.agent_name,

    -- Сообщения
    sm.message_id,
    sm.sender        AS sender_type,
    sm.reaction_type,
    sm.message_text,
    sm.sent_at,

    -- Вложения к сообщениям
    sma.attachment_id,
    sma.file_url,
    sma.file_type,
    sma.uploaded_at

FROM support_sessions AS ss
    JOIN users AS u
        ON u.user_id = ss.user_id
    LEFT JOIN support_agents AS sa
        ON sa.agent_id = ss.agent_id
    JOIN support_messages AS sm
        ON sm.session_id = ss.session_id
    LEFT JOIN support_message_attachments AS sma
        ON sma.message_id = sm.message_id

WHERE
    ss.session_status = 'OPEN'
    AND ss.agent_id = $1
ORDER BY ss.started_at ASC, sm.sent_at ASC;
    """
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(sql, agent_id)
        return [dict(r) for r in rows]


async def fetch_group_transactions(group_id: UUID) -> List[Dict[str, Any]]:
    """
    Возвращает все успешные транзакции (status = 'SUCCESS') за последний месяц
    для всех пользователей из family_group_members с заданным group_id,
    вместе с информацией о платёжной карте и сервисе.
    """
    sql = """
SELECT
    t.transaction_id,
    t.amount,
    t.currency,
    t.status,
    t.transaction_type,
    t.description,
    t.created_at,

    -- Пользователь и карта
    u.user_id,
    u.login,
    bc.bank_name,
    bc.payment_system,
    bc.is_default AS is_default_card,

    -- Сервис
    s.service_id,
    s.service_name

FROM transactions AS t
    JOIN users AS u
        ON u.user_id = t.user_id
    JOIN bank_cards AS bc
        ON bc.bank_card_id = t.bank_card_id
    LEFT JOIN services AS s
        ON s.service_id = t.service_id

WHERE
    t.user_id IN (
        SELECT user_id
        FROM family_group_members
        WHERE group_id = $1
    )
    AND t.status = 'SUCCESS'
    AND t.created_at >= DATE_TRUNC('month', NOW()) - INTERVAL '1 month'
ORDER BY t.created_at DESC;
    """
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(sql, group_id)
        return [dict(r) for r in rows]


async def fetch_admins_activity(min_actions: int = 0) -> List[Dict[str, Any]]:
    """
    Возвращает список администраторов (role = 'ADMIN') с количеством действий
    за последние 30 дней, где actions_last_30d > min_actions.
    """
    sql = """
WITH excluded_actions AS (
    SELECT action_id
    FROM actions
    WHERE action_name IN ('HEARTBEAT', 'VIEWED_PAGE')
)
SELECT
    u.user_id,
    u.login,
    r.role        AS user_role,
    COUNT(ah.activity_id) AS actions_last_30d

FROM users AS u
    JOIN user_roles AS ur
        ON ur.user_id = u.user_id
    JOIN roles AS r
        ON r.role_id = ur.role_id
    JOIN activity_history AS ah
        ON ah.user_id = u.user_id
       AND ah.created_at >= NOW() - INTERVAL '30 days'
       AND ah.action_id NOT IN (SELECT action_id FROM excluded_actions)

WHERE
    r.role = 'admin'

GROUP BY
    u.user_id,
    u.login,
    r.role

HAVING
    COUNT(ah.activity_id) > $1

ORDER BY
    actions_last_30d DESC;
    """
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(sql, min_actions)
        return [dict(r) for r in rows]
