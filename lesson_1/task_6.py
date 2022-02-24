from chardet import detect


new_list = ["сетевое программирование", "сокет", "декоратор"]

with open('test_file.txt', 'w', encoding="utf-8", errors='namereplace') as file:
    for line in new_list:
        file.write(line)
        file.write('\n')

print("*" * 30)

with open('test_file.txt', 'rb') as file:
    content = file.read()
encodings = detect(content)["encoding"]
print(f"кодировка файла: '{encodings}'")

print("*" * 30)

with open('test_file.txt', encoding=encodings, errors='namereplace') as file:
    for line in file:
        print(line)
