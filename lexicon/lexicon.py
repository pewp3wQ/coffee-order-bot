LEXICON_RU: dict[str, str | dict] = {
    "/start": "Я бот Service Coffee, в котором "
              'ты можешь сделать быстрый заказ своего любимого кофе\n\n'
              'Начнем ?',

    "description": "Привет, я бот кофейни Service Coffee, я приму твой заказ и отправлю нашим баристам,"
                   "чтобы ты смог забарть заказ без ожидания",

    "inline_kb_text": {
        'category': 'Что сегодня выберете ?',
        'location': 'Откуда заберете заказ ?',
        'volume': 'Какой объем желаете ?',
        'coffee': 'Что будете пить сегодня ?',
        'coffee_base': 'На каком молоке хотите сделать',
        'sugar': 'Сколько ложек сахара положить ?',
        'toppings': 'Какой топпинг добваить ?',
        'additional': 'Что нибудь еще добавить ?'
    }
}

ORDER_DATA: dict[str, dict] = {
    'category': {
        'classic': 'Классическое кофе',
        'cream_coffee': 'Кофе на основе сликов',
        'signature_coffee': 'Авторское кофе',
        'cold': 'Колд'
    },
    'location': {
        'ordzhonikidze': 'Орджоникидзе',
        'microdistrict': '202-микр'
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
            "sizes": ["250", "350"],
            "prices": { "250": 150, "350": 150 }
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

          "latte_halva": {
            "name": "Латте халва",
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

          "milkshake": {
            "name": "Молочный коктейль",
            "category": "cold",
            "sizes": ["350"],
            "prices": { "350": 290 }
          },

          "lemonade": {
            "name": "Домашний лимонад",
            "category": "cold",
            "sizes": ["350", "450"],
            "prices": { "350": 210, "450": 230 }
          }
        },
    "coffee": {
        "classic": {
          "espresso_x2": "Эспрессо х2",
          "americano": "Американо",
          "cappuccino": "Капучино",
          "flat_white": "Флэт уайт",
          "kakao": "Какао",
          "latte": "Латте",
          "mokkachino": "Моккачино",
          "matcha_latte": "Матча латте"
        },

        "cream_coffee": {
          "raf_vanilla": "Раф ваниль",
          "raf_nut": "Раф орех",
          "raf_citrus": "Раф цитрус",
          "raf_coconut": "Раф кокос"
        },

        "signature_coffee": {
          "latte_nut": "Латте орех",
          "latte_halva": "Латте халва",
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
          "ice_matcha": "Айс-матча",
          "milkshake": "Молочный коктейль",
          "lemonade": "Домашний лимонад"
        }
    },
    'coffee_base': {
        'milk': 'Молоко',
        'oat_milk': 'Овсяное',
        'soy_milk': 'Соевое',
        'coconut_milk': 'Кокосовое',
        'almond_milk': 'Миндальное'
    },
    'sugar': {
        'nothing': 'Без сахара',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5'
    },
    'toppings': {
        'nothing': 'Без топпинга',
        'chocolate': 'Шоколад',
        'nuts': 'Орех',
        'carmel': 'Карамель',
        'syrup': 'Клиновый сироп',
        'peach': 'Персик',
        'orange': 'Апельсин'
    },
    'additional': {
        'nothing': 'Без доп. добавок',
        'extra_espresso': 'Эсперссо',
        'marshmallow': 'Маршмелоу',
        'milk': 'Молоко',
        'oat_milk': 'Овсяное молоко',
        'soy_milk': 'Соевое молоко',
        'coconut_milk': 'Кокосовое молоко',
        'almond_milk': 'Миндальное молоко'
    },
    'noting': 'Ничего'
}

GROUP_BUTTONS: dict[str, str] = {
    'queue': 'Взялся за заказ',
    'ready': 'Заказ готов'
}
