import re
import csv


def write_to_csv(files_list, csv_file_name):
    def get_data(data_files):
        os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []

        def matrix_adapt(matrix):
            result = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
            for i in range(0, len(data_files)):
                matrix_row = []
                for j in range(0, 4):
                    matrix_row.append(matrix[j][i])
                result.append(matrix_row)
            return result

        for file_name in data_files:
            with open(file_name, 'r') as file:
                new_file = file.readlines()
                for line in new_file:
                    os_prod_list += re.findall(r'(?<=Изготовитель системы:)\s+([^:\n]+)\s*$', line)
                    os_name_list += re.findall(r'(?<=Название ОС:)\s+([^:\n]+)\s*$', line)
                    os_code_list += re.findall(r'(?<=Код продукта:)\s+([^:\n]+)\s*$', line)
                    os_type_list += re.findall(r'(?<=Тип системы:)\s+([^:\n]+)\s*$', line)

        head = [os_prod_list, os_name_list, os_code_list, os_type_list]
        main_data = matrix_adapt(head)
        return main_data

    data = get_data(files_list)
    with open(f'{csv_file_name}.csv', 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in data:
            f_n_writer.writerow(row)


info_for_report = ['info_1.txt', 'info_2.txt', 'info_3.txt']
write_to_csv(info_for_report, 'report_file')
