from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool


@asynccontextmanager
async def get_transaction_session(app):
    pool: AsyncConnectionPool = app.get('db_pool')

    if not pool:
        raise RuntimeError("DB Pool not found in app")

    async with pool.connection() as connection:
        async with connection.transaction():
            yield connection