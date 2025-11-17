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
                          ["espresso_x2", "classic", "60", 150],
                          ["americano", "classic", "250", 150],
                          ["americano", "classic", "350", 150],
                          ["cappuccino", "classic", "250", 210],
                          ["cappuccino", "classic", "350", 230],
                          ["cappuccino", "classic", "450", 250],
                          ["latte", "classic", "350", 230],
                          ["latte", "classic", "450", 250],
                          ["flat_white", "classic", "250", 210],
                          ["mokkachino", "classic", "350", 290],
                          ["matcha_latte", "classic", "350", 230],
                          ["matcha_latte", "classic", "450", 250],
                          ["kakao", "classic", "250", 200],
                          ["kakao", "classic", "350", 220],
                          ["kakao", "classic", "450", 240],
                          ["raf_vanilla", "cream", "350", 250],
                          ["raf_vanilla", "cream", "450", 280],
                          ["raf_nut", "cream", "350", 250],
                          ["raf_nut", "cream", "450", 280],
                          ["raf_citrus", "cream", "350", 250],
                          ["raf_citrus", "cream", "450", 280],
                          ["raf_coconut", "cream", "350", 250],
                          ["raf_coconut", "cream", "450", 280],
                          ["latte_nut", "signature", "350", 240],
                          ["latte_nut", "signature", "450", 260],
                          ["latte_halva", "signature", "350", 240],
                          ["latte_halva", "signature", "450", 260],
                          ["latte_peanut", "signature", "350", 240],
                          ["latte_peanut", "signature", "450", 260],
                          ["latte_spicy_maple", "signature", "350", 240],
                          ["latte_spicy_maple", "signature", "450", 260],
                          ["latte_salted_caramel", "signature", "350", 240],
                          ["latte_salted_caramel", "signature",  "450", 260],
                          ["raf_caramel_popcorn", "signature", "350", 290],
                          ["raf_caramel_popcorn", "signature", "450", 320],
                          ["raf_chocolate", "signature", "350", 310],
                          ["raf_chocolate", "signature", "450", 340],
                          ["bamble", "cold", "350", 290],
                          ["espresso_tonic", "cold", "350", 260],
                          ["ice_americano", "cold", "350", 150],
                          ["ice_latte", "cold", "350", 230],
                          ["ice_matcha", "cold", "350", 230],
                          ["milkshake", "cold", "350", 290],
                          ["lemonade", "cold", "350", 210],
                          ["lemonade", "cold", "450", 230],
                        ["milk", "coffee_base", "", 0],
                        ["oat_milk", "coffee_base", "", 30],
                        ["soy_milk", "coffee_base", "", 30],
                        ["coconut_milk", "coffee_base", "", 40],
                        ["almond_milk", "coffee_base", "", 40],
                        ["syrup", "additional", "", 30],
                        ["extra_espresso", "additional", "", 30],
                        ["marshmallow", "additional", "", 30],
                        ["milk", "additional", "", 0],
                        ["oat_milk", "additional", "", 30],
                        ["soy_milk", "additional", "", 30],
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