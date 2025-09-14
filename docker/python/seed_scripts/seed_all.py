from asyncio import sleep
import asyncio
import importlib
import os
import pkgutil
from .db import get_current_migration_version

APP_ENV = os.getenv("APP_ENV", "production").lower()
SEED_COUNT = int(os.getenv("SEED_COUNT", 10))
MIGRATION_VERSION: str = os.getenv("MIGRATION_VERSION")

def get_max_seed_version():
    import seed_scripts.versions
    version_modules = [
        int(name[1:].split("_")[0])
        for _, name, _ in pkgutil.iter_modules(seed_scripts.versions.__path__)
        if name.startswith("V") and name.endswith("_seed")
    ]
    return max(version_modules) if version_modules else "0"

def run_seed_for_version(now_version):
    for version in range(1, int(now_version) + 1):
        module_name = f"seed_scripts.versions.V{version}_seed"
        print(f"Проверяю наличие модуля: {module_name}")
        try:
            module = importlib.import_module(module_name)
            print(f"Импортирую модуль: {module_name}")
            module.run_seed(SEED_COUNT)
        except ModuleNotFoundError:
            print(f"Не найден скрипт сидирования для версии {version}")
        except AttributeError:
            print(f"Модуль {module_name} не содержит функцию run_seed")

async def main():
    if APP_ENV == "dev":
        mig_ver = MIGRATION_VERSION
        max_version = get_max_seed_version()

        if not mig_ver:
            print(f"→ MIGRATION_VERSION не задана, производится сидирование всех версий (1..{max_version})")
            mig_ver=max_version

        try:
            expected_version = int(mig_ver)
        except ValueError:
            print("❌❌❌MIGRATION_VERSION задана некорректно.❌❌❌")
            return

        time_out_count = 4
        time_out_time = 10
        cur_version = get_current_migration_version()

        while time_out_count != 0 and cur_version is None:
            print("❌❌❌Не удалось получить текущую версию миграции. Проверь подключение к базе и наличие таблицы flyway_schema_history.❌❌❌")
            print(f"Попытка №{5 - time_out_count}, следующая через {time_out_time} секунд.")
            await asyncio.sleep(time_out_time)
            cur_version = get_current_migration_version()
            time_out_count -= 1

        if time_out_count == 0:
            print("❌❌❌Не удалось получить текущую версию миграции. Проверь подключение к базе и наличие таблицы flyway_schema_history.❌❌❌")
            return

        time_out_count = 4
        time_out_time = 10

        while time_out_count != 0 and expected_version != int(get_current_migration_version()):
            print(f"⏳⏳⏳MIGRATION_VERSION={expected_version}, текущая в БД: {get_current_migration_version()}⏳⏳⏳")
            print(f"Попытка №{5 - time_out_count}, следующая через {time_out_time} секунд.")
            await asyncio.sleep(time_out_time)
            time_out_count -= 1

        if time_out_count != 0:
            print(f"✅✅✅Миграция завершена. Начинаем сидирование до версии {expected_version}✅✅✅")
            run_seed_for_version(expected_version)
        else:
            print("❌❌❌Не получилось дождаться миграции.❌❌❌")

if __name__ == "__main__":
    asyncio.run(main())