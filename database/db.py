import logging
from datetime import datetime, timezone
from typing import Any

from psycopg import AsyncConnection

logger = logging.getLogger(__name__)


async def add_user(
    conn: AsyncConnection,
    *,
    user_id: int,
    is_alive: bool = True
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                INSERT INTO users(user_id, username, is_alive)
                VALUES(
                    %(user_id)s, 
                    %(is_alive)s
                ) ON CONFLICT DO NOTHING;
            """,
            params={
                "user_id": user_id,
                "is_alive": is_alive
            },
        )
    logger.info(
        "User added. Table=`%s`, user_id=%d, created_at='%s', is_alive=%s",
        "users",
        user_id,
        datetime.now(timezone.utc),
        is_alive,
    )


async def get_user(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> tuple[Any, ...] | None:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
                SELECT 
                    id,
                    user_id,
                    username,
                    is_alive,
                    created_at
                    FROM users WHERE user_id = %s;
            """,
            params=(user_id,),
        )
        row = await data.fetchone()
    logger.info("Row is %s", row)
    return row if row else None


async def change_user_alive_status(
    conn: AsyncConnection,
    *,
    is_alive: bool,
    user_id: int,
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                UPDATE users
                SET is_alive = %s
                WHERE user_id = %s;
            """,
            params=(is_alive, user_id)
        )
    logger.info("Updated `is_alive` status to `%s` for user %d", is_alive, user_id)


async def get_user_alive_status(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> bool | None:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
                SELECT is_alive FROM users WHERE user_id = %s;
            """,
            params=(user_id,),
        )
        row = await data.fetchone()
    if row:
        logger.info("The user with `user_id`=%s has the is_alive status is %s", user_id, row[0])
    else:
        logger.warning("No user with `user_id`=%s found in the database", user_id)
    return row[0] if row else None


async def get_order_id(
        conn: AsyncConnection,
        *,
        user_id: int,
) -> int | None:
    async with conn.cursor() as cursor:
        order_id = await cursor.execute(
            query="""
                INSERT INTO orders (user_id, status)
                VALUES (
                    %(user_id)s, 
                    'draft'
                )
                RETURNING id;
            """,
            params=(user_id,),
        )
        row = await order_id.fetchone()
        return row[0] if row else None


async def update_user_order(
        conn: AsyncConnection,
        *,
        order_id: int,
        location: str,
        volume: str,
        coffee: str,
        toppings: str,
        ) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                UPDATE orders,
                SET location = %s,
                    volume = %s,
                    coffee = %s,
                    toppings = %s,
                    status = 'confirmed',
                    confirmed_at = NOW()
                WHERE id = %s;
            """,
            params=(location, volume, coffee, toppings, order_id)
        )
    logger.info("Updated `order` for ID: %d", order_id)


async def get_user_from_order(
        conn: AsyncConnection,
        *,
        order_id: int,
) -> int | None:
    async with conn.cursor() as cursor:
        user_id_from_order = await cursor.execute(
            query="""
                SELECT user_id FROM orders WHERE id = %s;
            """,
            params=(order_id,),
        )
        row = await user_id_from_order.fetchone()
    if row:
        logger.info("User ID from order has in db %s", row[0])
    else:
        logger.warning("No user with %s", order_id)
    return row[0] if row else None
