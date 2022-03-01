import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', encoding="utf-8") as file:
        data = json.loads(file.read())

    data['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})

    with open('orders.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, separators=(',', ': '), ensure_ascii=False)

    print(f'Данные добавлены в orders.json')


write_order_to_json('Товар_1', '15', '936', 'Кузнецов', '15.2.2022')
write_order_to_json('Товар_2', '1', '9036,96', 'Ларин', '31.01.2021')
