import logging
import uuid
from decimal import Decimal

from aiohttp import web
from aiogram import Bot
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification

from config.config import load_config, Config
from payments.get_db_pool import get_transaction_session
from payments.sender import send_order_to_group
from payments.payment_service import handle_payment_success, handle_payment_canceled


logger = logging.getLogger(__name__)
config: Config = load_config()

Configuration.account_id = config.payment_webhook.account_id
Configuration.secret_key = config.payment_webhook.secret_key

async def create_payment_check(price: str, order_id: int):
    my_payment = Payment.create({
        "amount": {
            "value": f"{price}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/stepiks_aiogram_bot"
        },
        "capture": True,
        "description": f"Заказ № {order_id}",
        "metadata": {
            "order_id": order_id
        }
    }, uuid.uuid4())

    return my_payment


async def yookassa_webhook_handler(request):
    bot: Bot = request.app['bot']

    try:
        event_json = await request.json()

        notification = WebhookNotification(event_json)
        payment = notification.object

        order_id = int(payment.metadata.get('order_id'))
        amount = payment.amount.value
        income_amount = Decimal(payment.income_amount.value)
        payment_id = payment.payment_method.id

        async with get_transaction_session(request.app) as connection:
            response_data: dict = {}

            if notification.event == "payment.succeeded":
                user_id, order_data = await handle_payment_success(
                    connection, order_id, payment_id, amount, income_amount
                )

                response_data = {"type": "success", "user_id": user_id, "order": order_data}

            elif notification.event == "payment.canceled":
                await handle_payment_canceled(connection, order_id)
                response_data = {"type": "canceled"}

            if response_data and response_data["type"] == "success":
                await send_order_to_group(bot, order_id, response_data["order"])
                await bot.send_message(
                    chat_id=response_data["user_id"],
                    text=f"🎉 Оплата прошла успешно! Заказ №{order_id} в работе."
                )

        return web.Response(text="OK", status=200)


    except Exception as e:
        logger.exception(f"Webhook processing error: {e}")
        return web.Response(status=500)


