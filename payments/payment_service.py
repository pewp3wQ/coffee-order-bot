from decimal import Decimal

from psycopg.connection_async import AsyncConnection

from database.db import (
    confirmed_order,
    get_user_order,
    add_payments
)


async def handle_payment_success(conn: AsyncConnection, order_id: int, payment_id: str, amount: Decimal, income_amount: Decimal):
    """Логика только для успешной оплаты"""
    await confirmed_order(conn, order_id=order_id)

    order_info = await get_user_order(conn, order_id=order_id)
    user_id = order_info[0][0]  # Лучше использовать именованные поля или dict

    await add_payments(conn, user_id=user_id, payment_id=payment_id,
                       order_id=order_id, price=income_amount)

    return user_id, order_info[0]


async def handle_payment_canceled(conn, order_id):
    pass
    """Логика для отмены"""
    # await cancel_order_in_db(conn, order_id=order_id)
    # logger.info(...)