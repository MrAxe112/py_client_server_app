task_list = ["разработка", "администрирование", "protocol", "standard"]

str_to_byte_list = []
byte_to_str_list = []


for n in task_list:
    byte = n.encode("utf-8")
    print(byte, type(byte))
    str_to_byte_list.append(byte)

print("*" * 30)

for n in str_to_byte_list:
    word = n.decode("utf-8")
    print(word, type(word))
    byte_to_str_list.append(word)
