"""Загружает тестовые данные из seed.sql, если база ещё пустая.

Запускается из entrypoint.sh сразу после миграций. Если в таблице услуг уже
есть записи, скрипт ничего не делает, поэтому перезапуск контейнера не трогает
данные, которые появились во время работы.
"""

import asyncio
from pathlib import Path

import asyncpg

from core.config import settings

SEED_FILE = Path(__file__).with_name("seed.sql")


async def main() -> None:
    # asyncpg понимает обычный адрес postgresql://, без приставки драйвера SQLAlchemy
    url = str(settings.db.url).replace("postgresql+asyncpg://", "postgresql://", 1)
    conn = await asyncpg.connect(url)
    try:
        if await conn.fetchval("SELECT EXISTS (SELECT 1 FROM services)"):
            print("seed: в базе уже есть данные, пропускаю")
            return
        await conn.execute(SEED_FILE.read_text(encoding="utf-8"))
        print("seed: тестовые данные загружены")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
