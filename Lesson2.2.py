"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    """
    Функцию в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer),
    дата (date).
    Функция записывает данных в виде словаря в файл orders.json.
    """

    with open('orders.json', 'r', encoding='utf-8',) as file_out:
        data = json.load(file_out)

    with open('orders.json', 'w', encoding='utf-8') as file_in:
        orders_list = data['orders']
        order_info = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date}
        orders_list.append(order_info)
        json.dump(data, file_in, indent=4)  # величина отступа задана через indent


# checking the function
write_order_to_json('book', '2', '700', 'Demidov I.A.', '15.11.2021')
write_order_to_json('notebook', '20', '100000', 'Ivanov A.A.', '16.11.2021')
write_order_to_json('whiteboard', '11', '3000', 'Lenin V.I.', '17.11.2021')
