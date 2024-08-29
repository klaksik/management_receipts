import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from asyncpg import Connection


class UniquePreparedStatementConnection(Connection):
    """
    Class for creating unique prepared SQL statements using UUID.
    """

    def _get_unique_id(self, prefix: str) -> str:
        """
        Generate a unique identifier for prepared statements.

        :param prefix: Prefix for the identifier
        :return: String with the unique identifier
        """
        return f"__asyncpg_{prefix}_{uuid.uuid4()}__"


# Create an asynchronous SQLAlchemy engine with caching and connection settings.
engine = create_async_engine(
    "postgresql+asyncpg://postgres.xzjawosavmpkxwiduzdy:Pn&Zut7rnnUDMML@aws-0-us-east-1.pooler.supabase.com:6543/postgres",
    echo=False,
    connect_args={
        "connection_class": UniquePreparedStatementConnection,
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    },
)

# Create a base class for declarative models
Base = declarative_base()

# Metadata for the database
metadata = MetaData()

# Factory for creating asynchronous sessions
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    """
    Asynchronous function to create the database and tables.
    Executes migrations or creates tables if they do not exist.
    """
    async with engine.begin() as conn:
        # Apply migrations or create tables
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Asynchronous function to obtain a database connection using SQLAlchemy.

    Yields:
        session: An asynchronous SQLAlchemy session.
    """
    async with async_session() as session:
        yield session