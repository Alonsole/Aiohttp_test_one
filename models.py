import asyncio
from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import traceback
from db_settings import *

class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {"id": self.id}


class Announcement(Base):
    """Модель таблицы объявлений"""
    __tablename__ = 'announcement'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=False)
    author = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class User(Base):
    """Модель таблицы Пользователей"""
    __tablename__ = "app_user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(15), nullable=False)
    registration_time = Column(DateTime, default=datetime.now)

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat(),
        }


async def init_table():
    """
    Функция создания Таблиц
    """
    # Создаем сессию для взаимодействия с базой данных
    async with Session() as session:
        new_user = User(name="Maksim", password="1")
        session.add(new_user)
        await session.commit()
        print(f'Создана первая тестовая учетная запись')

    async with Session() as session:
        new_announcement = Announcement(title="Test Title", description="Test Description", author="Maksim Velichko")
        session.add(new_announcement)
        await session.commit()
        print(f'Создана первая тестовая запись')


async def init_db():
    """
    Асинхронная функция для удаления и создания базы данных.
    """
    try:
        # Открываем соединение
        async with engine.connect() as conn:
            # Устанавливаем уровень изоляции
            await conn.execution_options(isolation_level="AUTOCOMMIT")
            # 1 Проверка и удаление + закрыть все активные соединения 2 Создание
            await conn.execute(text(f'DROP DATABASE IF EXISTS {DB_NAME} WITH (FORCE);'))  # 1
            await conn.execute(text(f'CREATE DATABASE {DB_NAME};'))  # 2
        # Создаем таблицы
        async with engine_table.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print(f'База данных {DB_NAME} успешно создана.')
    except Exception as e:
        print(f'Произошла ошибка при создании базы данных: {e} \n {traceback.format_exc()}')


async def close_orm():
    await engine.dispose()


async def main():
    await init_db()
    await init_table() # Заливка первых тест данных - можно отключить
    await close_orm()


if __name__ == "__main__":
    asyncio.run(main())
