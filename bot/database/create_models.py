import asyncio

from bot.database.base_model import engine, Base
from bot.database.__all_models import Users, Warns

async def create_tables():
    try:
        async with engine.begin() as conn:
            # Создаём все таблицы, описанные через Base
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Таблицы успешно созданы!")
            
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")

if __name__ == "__main__":
    asyncio.run(create_tables())
