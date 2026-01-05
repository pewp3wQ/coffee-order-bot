LEXICON_RU: dict[str, str | dict] = {
    "/start": "Я бот Service Coffee, в котором "
              'ты можешь сделать быстрый заказ своего любимого кофе\n\n'
              'Начнем ?',

    "description": "Привет, я бот кофейни Service Coffee, я приму твой заказ и отправлю нашим баристам,"
                   "чтобы ты смог забарть заказ без ожидания",

    "inline_kb_text": {
        'category': 'Что сегодня для вас приготовим?',
        'location': 'Где вам будет удобнее забрать заказ?',
        'volume': 'Какой объем желаете?',
        'coffee': 'Какой кофе хотите сегодня?',
        'coffee_base': 'На каком молоке будем готовить?',
        'sugar': 'Сколько ложек сахара добавить?',
        'toppings': 'Какой сироп желаете?',
        'additional': 'Добавим что-нибудь еще?',
        'wait_time': 'Через сколкьо Вас ждать?',
        'temperature': 'Сделать напиток погорячее?'
    }
}

ORDER_DATA: dict[str, dict] = {
    'category': {
        'classic': 'Классика',
        'mokka': 'Матча латте, Какао',
        'cream': 'Кофе на основе сливок',
        'signature': 'Спешл',
        'cold': 'Холодные кофе'
    },
    'location': {
        'ordzhonikidze': 'Орджоникидзе, д. 17',
        'microdistrict': '203 мкр. к. 30'
    },
    'volume': {
        '60': '60 мл',
        '250': '250 мл',
        '350': '350 мл',
        '450': '450 мл'
    },
    'coffee_items': {
          "espresso_x2": {
            "name": "Эспрессо х2",
            "category": "classic",
            "sizes": ["60"],
            "prices": { "60": 150 }
          },

          "americano": {
            "name": "Американо",
            "category": "classic",
            "sizes": ["250", "350", "450"],
            "prices": { "250": 170, "350": 170, "450": 170}
          },

          "cappuccino": {
            "name": "Капучино",
            "category": "classic",
            "sizes": ["250", "350", "450"],
            "prices": { "250": 210,
                        "350": 230,
                        "450": 250 }
          },

          "latte": {
            "name": "Латте",
            "category": "classic",
            "sizes": ["350", "450"],
            "prices": { "350": 230, "450": 250 }
          },

          "flat_white": {
            "name": "Флэт уайт",
            "category": "classic",
            "sizes": ["250"],
            "prices": { "250": 210 }
          },

          "mokkachino": {
            "name": "Моккачино",
            "category": "classic",
            "sizes": ["350"],
            "prices": { "350": 290 }
          },

          "matcha_latte": {
            "name": "Матча латте",
            "category": "classic",
            "sizes": ["350", "450"],
            "prices": { "350": 230, "450": 250 }
          },

          "kakao": {
            "name": "Какао",
            "category": "classic",
            "sizes": ["250", "350", "450"],
            "prices": { "250": 200, "350": 220, "450": 240 }
          },

          "raf_vanilla": {
            "name": "Раф ваниль",
            "category": "cream",
            "sizes": ["350", "450"],
            "prices": { "350": 250, "450": 280 }
          },

          "raf_nut": {
            "name": "Раф орех",
            "category": "cream",
            "sizes": ["350", "450"],
            "prices": { "350": 250, "450": 280 }
          },

          "raf_citrus": {
            "name": "Раф цитрус",
            "category": "cream",
            "sizes": ["350", "450"],
            "prices": { "350": 250, "450": 280 }
          },

          "raf_coconut": {
            "name": "Раф кокос",
            "category": "cream",
            "sizes": ["350", "450"],
            "prices": { "350": 250, "450": 280 }
          },

          "latte_nut": {
            "name": "Латте орех",
            "category": "signature",
            "sizes": ["350", "450"],
            "prices": { "350": 240, "450": 260 }
          },

          "latte_peanut": {
            "name": "Латте арахис",
            "category": "signature",
            "sizes": ["350", "450"],
            "prices": { "350": 240, "450": 260 }
          },

          "latte_spicy_maple": {
            "name": "Латте пряный с клёном",
            "category": "signature",
            "sizes": ["350", "450"],
            "prices": { "350": 240, "450": 260 }
          },

          "latte_salted_caramel": {
            "name": "Латте солёная карамель",
            "category": "signature",
            "sizes": ["350", "450"],
            "prices": { "350": 240, "450": 260 }
          },

          "raf_caramel_popcorn": {
            "name": "Раф карамельный попкорн",
            "category": "signature",
            "sizes": ["350", "450"],
            "prices": { "350": 290, "450": 320 }
          },

          "raf_chocolate": {
            "name": "Раф шоколад",
            "category": "signature",
            "sizes": ["350", "450"],
            "prices": { "350": 310, "450": 340 }
          },

          "bamble": {
            "name": "Бамбл",
            "category": "cold",
            "sizes": ["350"],
            "prices": { "350": 290 }
          },

          "espresso_tonic": {
            "name": "Эспрессо-тоник",
            "category": "cold",
            "sizes": ["350"],
            "prices": { "350": 260 }
          },

          "ice_americano": {
            "name": "Айс-американо",
            "category": "cold",
            "sizes": ["350"],
            "prices": { "350": 150 }
          },

          "ice_latte": {
            "name": "Айс-латте",
            "category": "cold",
            "sizes": ["350"],
            "prices": { "350": 230 }
          },

          "ice_matcha": {
            "name": "Айс-матча",
            "category": "cold",
            "sizes": ["350"],
            "prices": { "350": 230 }
          },
        },
    "coffee": {
        "classic": {
          "espresso_x2": "Эспрессо х2",
          "americano": "Американо",
          "cappuccino": "Капучино",
          "flat_white": "Флэт уайт",
          "latte": "Латте",
        },
        "mokka": {
          "kakao": "Какао",
          "matcha_latte": "Матча латте"
        },
        "cream": {
          "raf_vanilla": "Раф ваниль",
          "raf_nut": "Раф орех",
          "raf_coconut": "Раф кокос"
        },
        "signature": {
          "latte_nut": "Латте орех",
          "latte_peanut": "Латте арахис",
          "latte_spicy_maple": "Латте пряный с клёном",
          "latte_salted_caramel": "Латте солёная карамель",
          "raf_caramel_popcorn": "Раф карамельный попкорн",
          "raf_chocolate": "Раф шоколад"
        },
        "cold": {
          "bamble": "Бамбл",
          "espresso_tonic": "Эспрессо-тоник",
          "ice_americano": "Айс-американо",
          "ice_latte": "Айс-латте",
          "ice_matcha": "Айс-матча"
        }
    },
    'coffee_base': {
        'milk': 'Молоко 3.2 %',
        'oat_milk': 'Овсяное',
        'coconut_milk': 'Кокосовое',
        'almond_milk': 'Миндальное'
    },
    'sugar': {
        '0.5': '0.5',
        '1': '1',
        '1.5': '1.5',
        '2': '2',
        '2.5': '2.5',
        '3': '3',
        '3.5': '3.5',
        '4': '4',
        'nothing': 'Без сахара'
    },
    'toppings': {
        "nothing": "Без сиропа",
        "caramel": "Карамель",
        "salted_caramel": "Солёная карамель",
        "vanilla": "Ваниль",
        "chocolate": "Шоколад",
        "hazelnut": "Лесной орех",
        "coconut": "Кокос",
        "almond": "Миндаль",
        "pistachio": "Фисташка",
        "cinnabon": "Синнабон",
        "maple": "Клён",
        "mint": "Мята",
        "cherry": "Вишня",
        "strawberry": "Клубника",
        "pomegranate": "Гранат",
        "banana": "Банан",
        "peach": "Персик",
        "orange": "Апельсин"
    },
    'additional': {
        'nothing': 'Без доп. добавок',
        'extra_espresso': 'Эспрессо',
        'marshmallow': 'Маршмеллоу',
        'milk': 'Молоко 3.2 % (20 мл.)',
        'oat_milk': 'Овсяное молоко (20 мл.)',
        'coconut_milk': 'Кокосовое молоко (20 мл.)',
        'almond_milk': 'Миндальное молоко (20 мл.)'
    },
    'temperature': {
        'yes': 'Да',
        'no': ' Нет'
    },
    'wait_time': {
        'short': '2-3 минуты',
        'medium': '5 минут',
        'long': ' 10 минут'
    }
}

GROUP_BUTTONS: dict[str, str] = {
    'queue': 'Взялся за заказ',
    'ready': 'Заказ готов'
}

ADMIN_MENU: dict[str, dict] = {
    'main_menu': {
        'change_price': 'Поменять цену товара',
        'remove_item': 'Убрать товар из меню',
        'add_item': 'Добваить товар в меню',
        'send_messages': 'Сделать рассылку'
    },

    'change_price_menu': {
        'price_coffee': 'Поменять цену кофе',
        'price_milk': 'Поменять цену молока',
        'price_topping': 'Поменять цену топпинга',
        'price_additional': 'Поменять цену добавок',
    },

    'remove_item': {
        'coffee': 'Убрать кофе из меню',
        'milk': 'Убрать молоко из меню',
        'topping': 'Убрать топпинг из меню',
        'additional': 'Убрать доп. добавку из меню',
    }
}
