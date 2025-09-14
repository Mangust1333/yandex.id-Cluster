from .db import session
from sqlalchemy import text

def truncate_table(table_name):
    try:
        session.execute(text(f"TRUNCATE TABLE {table_name} CASCADE;"))
        session.commit()
        print(f"→ Таблица {table_name} была очищена")
    except Exception as e:
        session.rollback()
        print(f"⚠️ Ошибка при очистке таблицы {table_name}: {e}")


