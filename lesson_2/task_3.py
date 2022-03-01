import yaml


data = {
    'clients': ['Сергей И', 'Лев Т', 'John S', 'Леонид Ж'],
    'items_quantity': 4,
    'item_price': {
        'product_1': '999₫-1000₫',
        'product_2': '150₫-500₫',
        'product_3': '10000₫-300000₫',
        'product_4': '321€-516₫'
    },

}

with open("test.yaml", 'w', encoding='utf-8') as f_n:
    yaml.dump(data, f_n, default_flow_style=False, allow_unicode=True)

with open("test.yaml", "r", encoding='utf-8') as f_n:
    content = yaml.load(f_n, Loader=yaml.FullLoader)
    print(content == data)
