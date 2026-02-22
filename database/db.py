import logging
from datetime import datetime, timezone
from decimal import Decimal
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
                INSERT INTO users(user_id, is_alive)
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
        username: str,
) -> int | None:
    async with conn.cursor() as cursor:
        order_id = await cursor.execute(
            query="""
                INSERT INTO orders (user_id, username, status)
                VALUES (
                    %(user_id)s, 
                    %(username)s, 
                    'draft'
                )
                RETURNING id;
            """,
            params={
                "user_id": user_id,
                "username": username
            },
        )
        row = await order_id.fetchone()
        return row[0] if row else None


async def update_pending_order(
        conn: AsyncConnection,
        *,
        order_id: int,
        location: str,
        category: str,
        coffee: str,
        volume: str,
        coffee_base: str,
        sugar: str,
        toppings: str,
        additional: str,
        temperature: str,
        wait_time: str,
        price: int,
        ) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                UPDATE orders
                SET location = %s,
                    category = %s,
                    coffee = %s,
                    volume = %s,
                    coffee_base = %s,
                    sugar = %s,
                    toppings = %s,
                    additional = %s,
                    temperature = %s,
                    wait_time = %s,
                    price = %s,
                    status = 'pending',
                    pending_at = NOW()
                WHERE id = %s;
            """,
            params=(location,
                    category,
                    coffee,
                    volume,
                    coffee_base,
                    sugar,
                    toppings,
                    additional,
                    temperature,
                    wait_time,
                    price,
                    order_id)
        )
    logger.info("Заказ -- %d сформирован и отрправлен для подтверждения оплаты", order_id)


async def confirmed_order(
        conn: AsyncConnection,
        *,
        order_id: int
        ) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                UPDATE orders
                SET status = 'paid',
                    confirmed_at = NOW()
                WHERE id = %s;
            """,
            params=(order_id,)
        )
    logger.info("Оплата по заказу -- %d -- подтверждена", order_id)


async def get_user_order(
        conn: AsyncConnection,
        *,
        order_id: int,
) -> tuple | None:
    async with conn.cursor() as cursor:
        user_id_from_order = await cursor.execute(
            query="""
                SELECT 
                    user_id, 
                    username, 
                    location, 
                    category, 
                    coffee, 
                    volume, 
                    coffee_base, 
                    sugar, 
                    toppings, 
                    additional,
                    temperature,
                    wait_time,
                    price 
                FROM orders 
                WHERE id = %s;
            """,
            params=(order_id,),
        )
        row = await user_id_from_order.fetchall()
    if row:
        logger.info("User ID from order has in db %s", row[0])
    else:
        logger.warning("No user with %s", order_id)
    return row if row else None

async def add_payments(
        conn: AsyncConnection,
        *,
        user_id: int,
        payment_id: str,
        order_id: int,
        price: Decimal
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                INSERT INTO payments (user_id, payment_id, order_id, price)
                VALUES (
                    %(user_id)s,
                    %(payment_id)s,
                    %(order_id)s,
                    %(price)s
                );
            """,
            params={
                "user_id": user_id,
                "payment_id": payment_id,
                "order_id": order_id,
                "price": price,
            }
        )


async def add_price(
        conn: AsyncConnection,
        *,
        product_name: str,
        category: str,
        volume: str,
        price: int
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                INSERT INTO prices (product_name, category, volume, price)
                VALUES (
                    %(product_name)s,
                    %(category)s,
                    %(volume)s,
                    %(price)s
                );    
            """,
            params={
                "product_name": product_name,
                "category": category,
                "volume": volume,
                "price": price
            },
        )

async def get_price(
        conn: AsyncConnection,
        *,
        product_name: str,
        category: str,
        volume: str | None = None
) -> int | None:
    async with conn.cursor() as cursor:
        coffee_price = await cursor.execute(
            query="""
                SELECT price
                FROM prices
                WHERE
                    product_name = %(product_name)s AND 
                    category = %(category)s AND
                    (volume = %(volume)s OR %(volume)s IS NULL);
            """,
            params={
                "product_name": product_name,
                "category": category,
                "volume": volume
            }
        )

        row = await coffee_price.fetchone()
        if row:
            logger.info("Price for %s = %s", product_name, row[0])
        else:
            logger.warning("No price for %s, %s", product_name, volume)
        return row[0] if row else None