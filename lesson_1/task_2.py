def func(new_list):
    def word_to_byte(target):
        try:
            byte = eval("b'" + target + "'")
            print(byte, type(byte), len(byte))
        except Exception as err:
            print(f'Error: "{target}", {err}')
            pass

    if type(new_list) is str:
        word_to_byte(new_list)
    else:
        for word in new_list:
            word_to_byte(word)


if __name__ == "__main__":
    line = ['class', 'function', 'method']
    func(line)
