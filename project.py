import os
import pandas as pd
from pathlib import Path


class PriceMachine():

    def __init__(self,):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self,):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''

        file_path = input('Введите путь к папке с прайс-листами \n ->>')
        os.chdir(file_path)
        f_list = sorted(Path(".").glob('price*.csv'))
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        i = 0

        for k in range(len(f_list)):
            if os.path.isfile(f_list[k]):

                df = pd.read_csv(f_list[i])
                df_temp = pd.DataFrame(df)

                df_temp.rename(columns={'название': 'наименование', 'продукт': 'наименование'},inplace=True)
                df_temp.rename(columns={'товар': 'наименование'}, inplace=True)
                df_temp.rename(columns={'розница': 'цена'}, inplace=True)
                df_temp.rename(columns={'фасовка': 'вес', 'масса': 'вес'}, inplace=True)

                df_temp['цена за кг'] = df_temp['цена'] / df_temp['вес']
                df_temp['файл'] = f_list[k]

                df_t = df_temp[['наименование', 'цена', 'вес', 'файл', 'цена за кг']]

                if i == 0:
                    self.data = df_t.copy()

                else:
                    df_t2 = self.data.copy()
                    self.data = pd.concat([df_t2, df_t])

            else:
                pass

            i += 1

        self.export_to_html()
        self.find_text()


    def export_to_html(self):

        df = pd.DataFrame(self.data)
        html_table = df.to_html(index=False, justify='left')
        html_file = open('myPrice.html', 'w')
        html_file.write(html_table)
        html_file.close()

        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''

    def find_text(self,):
        # self.data['наименование', 'цена', 'вес', 'файл', 'цена за кг'].str.lower().data
        # print(self.data)

        while 1 :
            text = input('\n Введите запрос продукта ( exit - выход из программы  )\n ->>')
            if text != 'exit':
                if self.data['наименование'].str.contains(text).any():
                    df_1 = self.data[self.data['наименование'].str.contains(text)]
                    df_2 = df_1.sort_values(by=['цена за кг'], ascending=[True])
                    print (df_2)
                else:
                    print(f'Товар {text} не найден')
                continue
            else:
                print('the end')
                exit()

        else:
            exit()



pm = PriceMachine()
pm.load_prices()


'''
    Логика работы программы
'''
print('the end')