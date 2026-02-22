import logging
import os
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class LogSettings:
    level: str
    format: str


@dataclass
class GroupData:
    group_id: int
    thread_id: int


@dataclass
class DatabaseSettings:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class RedisSettings:
    host: str
    port: int
    db: int
    password: str
    username: str

@dataclass
class WebhookSettings:
    base_url: str
    secret: str
    path: str
    server: str
    port: int


@dataclass
class PaymentWebhook:
    path: str
    account_id: int
    secret_key: str


@dataclass
class Config:
    bot: TgBot
    log: LogSettings
    group: GroupData
    db: DatabaseSettings
    redis: RedisSettings
    webhook: WebhookSettings
    payment_webhook: PaymentWebhook



def load_config(path: str | None = None) -> Config:
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(".env file not found at '%s', skipping...", path)
        else:
            logger.info("Loading .env from '%s'", path)
    env.read_env(path)
    token = env("BOT_TOKEN")
    admin_ids = env("ADMIN_IDS")

    if not token:
        raise ValueError("BOT_TOKEN must not be empty")

    db = DatabaseSettings(
        name=env("POSTGRES_DB"),
        host=env("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        user=env("POSTGRES_USER"),
        password=env("POSTGRES_PASSWORD"),
    )

    redis = RedisSettings(
        host=env("REDIS_HOST"),
        port=env.int("REDIS_PORT"),
        db=env.int("REDIS_DATABASE"),
        password=env("REDIS_PASSWORD", default=""),
        username=env("REDIS_USERNAME", default=""),
    )

    logg_settings = LogSettings(
        level=env("LOG_LEVEL"),
        format=env("LOG_FORMAT")
    )

    group_data = GroupData(
        group_id=env('GROUP_ID'),
        thread_id=env('THREAD_ID')
    )

    webhook = WebhookSettings(
        base_url=env('BASE_WEBHOOK_URL'),
        secret=env('WEBHOOK_SECRET'),
        path=env('WEBHOOK_PATH'),
        server=env('WEB_SERVER_HOST'),
        port=env('WEB_SERVER_PORT')
    )

    payments_webhook = PaymentWebhook(
        path=env('PAYMENTS_WEBHOOK_PATH'),
        account_id=env('PAYMENTS_ACCOUNT_ID'),
        secret_key=env('PAYMENTS_SECRET_KEY'),
    )

    logger.info("Configuration loaded successfully")

    return Config(
        bot=TgBot(token=token, admin_ids=admin_ids),
        db=db,
        redis=redis,
        log=logg_settings,
        group=group_data,
        webhook=webhook,
        payment_webhook=payments_webhook
    )