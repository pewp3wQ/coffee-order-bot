LEXICON_RU: dict[str, dict] = {
    'command': {'/start': 'Воспользуется меню и выберете /order - для заказа кофе на вынос'},
    'inline_kb_text': {'location': 'Откуда заберете заказ ?',
                       'volume': 'Какой объем желаете ?',
                       'coffee': 'Какой кофе сегодня будете ?',
                       'toppings': 'Какой топпинг добваить ?',
                       'good': 'Хорошо'}

}

ORDER_DATA: dict[str, dict] = {
    'location': {
        'ordj': 'Орджоникидзе',
        'micro': '202-микр'
    },
    'volume': {
        'small': '0.3',
        'medium': '0.5',
        'large': '0.75'
    },
    'coffee': {
        'latte': 'Латте',
        'capuchino': 'Капучино',
        'americano': 'Американо',
        'escpresso': 'Эсперссо',
        'mackachino': 'Маккачино',
        'limonde': 'Лимонад',
        'cacao': 'Какао'
    },
    'toppings': {
        'noting': 'Без топпинга',
        'chocolate': 'Шоколад',
        'nuts': 'Орех',
        'carmel': 'Карамель',
        'syrup': 'Клиновый сироп',
        'peach': 'Персик',
        'orange': 'Апельсин'
    },
    'good': {'good': 'Хорошо'}
}

GROUP_BUTTONS: dict[str, str] = {
    'queue': 'Взялся за заказ',
    'ready': 'Заказ готов'
}