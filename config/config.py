from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class LogSettings:
    level: str
    format: str


@dataclass
class GroupData:
    group_id: int
    thread_id: int


@dataclass
class Config:
    bot: TgBot
    log: LogSettings
    group: GroupData





def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(token=env('BOT_TOKEN')),
        log=LogSettings(level=env('LOG_LEVEL'), format=env('LOG_FORMAT')),
        group=GroupData(group_id=env('GROUP_ID'), thread_id=env('THREAD_ID'))
    )