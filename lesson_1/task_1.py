def str_type(new_list):
    for word in new_list:
        print(type(word), word)


some_str = ['разработка', 'сокет', 'декоратор']
some_byte = [
    '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
    '\u0441\u043e\u043a\u0435\u0442',
    '\u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430'
    ]

str_type(some_str)
print('*' * 30)
str_type(some_byte)
