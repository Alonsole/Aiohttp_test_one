import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Загрузка переменных окружений
dotenv_file = '.env'
load_dotenv(dotenv_file)

# Настройки подключения к базе данных
DB_HOST = os.environ.get("POSTGRES_DBHOST", "127.0.0.1")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_NAME = os.environ.get("POSTGRES_DBNAME", "postgres")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "1234")

# Подключение к базе данных PostgreSQL
DSN = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
#  Асинхронный движок базы для создания ДБ
engine = create_async_engine(DSN)
#  Асинхронный движок базы для создания Таблиц
engine_table = create_async_engine(f"{DSN}/{DB_NAME}")
# Управление соединениями с базой данных и выполнение запросов
Session = async_sessionmaker(bind=engine_table, expire_on_commit=False)