import asyncio
import logging
import os
import sys

from database.connection import get_pg_connection
from config.config import Config, load_config
from psycopg import AsyncConnection, Error

config: Config = load_config()

logging.basicConfig(
    level=logging.getLevelName(level=config.log.level),
    format=config.log.format,
)

logger = logging.getLogger(__name__)

if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    connection: AsyncConnection | None = None

    try:
        connection = await get_pg_connection(
            db_name=config.db.name,
            host=config.db.host,
            port=config.db.port,
            user=config.db.user,
            password=config.db.password,
        )
        async with connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    await cursor.execute(
                        query="""
                            CREATE TABLE IF NOT EXISTS users(
                                id SERIAL PRIMARY KEY,
                                user_id BIGINT NOT NULL UNIQUE,
                                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                is_alive BOOLEAN NOT NULL
                            ); 
                        """
                    )
                    await cursor.execute(
                        query="""
                            CREATE TABLE IF NOT EXISTS orders(
                                id SERIAL PRIMARY KEY,
                                user_id BIGINT REFERENCES users(user_id),
                                status TEXT NOT NULL DEFAULT 'draft',
                                created_at TIMESTAMP DEFAULT NOW(),
                                location TEXT,
                                category TEXT,
                                coffee TEXT,
                                volume TEXT,
                                coffee_base TEXT,
                                sugar TEXT,
                                toppings TEXT,
                                additional TEXT,
                                price INTEGER,
                                confirmed_at TIMESTAMP
                            );
                        """
                    )
                    await cursor.execute(
                        query="""
                            CREATE TABLE IF NOT EXISTS prices (
                                id SERIAL PRIMARY KEY,
                                product_name TEXT NOT NULL,
                                category TEXT NOT NULL,
                                volume TEXT,
                                price INTEGER
                            );
                        """
                    )

                    coffee_data = [
                        ["espresso_x2", "classic", "60", 190],
                        ["americano", "classic", "250", 190],
                        ["americano", "classic", "350", 190],
                        ["americano", "classic", "450", 220],
                        ["cappuccino", "classic", "250", 240],
                        ["cappuccino", "classic", "350", 270],
                        ["cappuccino", "classic", "450", 300],
                        ["latte", "classic", "350", 270],
                        ["latte", "classic", "450", 300],
                        ["flat_white", "classic", "250", 240],
                        ["matcha_latte", "mokka", "350", 270],
                        ["matcha_latte", "mokka", "450", 300],
                        ["kakao", "mokka", "250", 220],
                        ["kakao", "mokka", "350", 250],
                        ["kakao", "mokka", "450", 280],
                        ["raf_classic", "cream", "350", 300],
                        ["raf_classic", "cream", "450", 350],
                        ["raf_vanilla", "cream", "350", 330],
                        ["raf_vanilla", "cream", "450", 380],
                        ["raf_nut", "cream", "350", 330],
                        ["raf_nut", "cream", "450", 380],
                        ["raf_coconut", "cream", "350", 330],
                        ["raf_coconut", "cream", "450", 380],
                        ["latte_nut", "signature", "350", 300],
                        ["latte_nut", "signature", "450", 350],
                        ["latte_peanut", "signature", "350", 300],
                        ["latte_peanut", "signature", "450", 350],
                        ["latte_spicy_maple", "signature", "350", 300],
                        ["latte_spicy_maple", "signature", "450", 350],
                        ["latte_salted_caramel", "signature", "350", 300],
                        ["latte_salted_caramel", "signature",  "450", 350],
                        ["latte_sinnabon", "signature",  "350", 330],
                        ["latte_sinnabon", "signature",  "450", 380],
                        ["raf_caramel_popcorn", "signature", "350", 350],
                        ["raf_caramel_popcorn", "signature", "450", 400],
                        ["raf_chocolate", "signature", "350", 350],
                        ["raf_chocolate", "signature", "450", 400],
                        ["bamble", "cold", "350", 320],
                        ["espresso_tonic", "cold", "350", 230],
                        ["ice_americano", "cold", "350", 190],
                        ["ice_latte", "cold", "350", 270],
                        ["ice_matcha", "cold", "350", 270],
                        ["milk", "coffee_base", "", 0],
                        ["oat_milk", "coffee_base", "", 30],
                        ["coconut_milk", "coffee_base", "", 50],
                        ["almond_milk", "coffee_base", "", 50],
                        ["syrup", "additional", "", 30],
                        ["extra_espresso", "additional", "", 50],
                        ["marshmallow", "additional", "", 30],
                        ["milk", "additional", "", 0],
                        ["cream", "additional", "", 20],
                        ["oat_milk", "additional", "", 30],
                        ["coconut_milk", "additional", "", 30],
                        ["almond_milk", "additional", "", 30]
                    ]
                    for data_list in coffee_data:
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
                                "product_name": data_list[0],
                                "category": data_list[1],
                                "volume": data_list[2],
                                "price": data_list[3]
                            },
                        ),
                logger.info("Tables `users`, `orders`, `prices`, all prices is loaded were successfully created")
    except Error as db_error:
        logger.exception("Database-specific error: %s", db_error)
    except Exception as e:
        logger.exception("Unhandled error: %s", e)
    finally:
        if connection:
            await connection.close()
            logger.info("Connection to Postgres closed")




asyncio.run(main())