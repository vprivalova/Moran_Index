import pandas as pd
import numpy as np


class LoadData:
    def __init__(self, file):
        self.file = file
        self.lst_places = []
        self.dct_param = {}

    def file_processing(self):
        with open(self.file, 'r', encoding='utf-8') as tf:
            for elem in tf:
                self.lst_places.append(elem.split(';')[0])
                self.dct_param[elem.split(';')[0]] = int(elem.split(';')[1])
        return self.lst_places, self.dct_param


class SpatialWeightMatrix:

    @staticmethod
    def matrix_creation(value):
        arr = []
        for i in range(len(value)):
            s = []
            for j in range(len(value)):
                s.append(0)
            arr.append(s)

        arr2 = np.array(arr)
        df = pd.DataFrame(arr2, columns=value, index=value)
        with open('matrix.xlsx', 'w', encoding='utf8'):
            df.to_excel('matrix.xlsx')
        print('Введите в excel файл данные о границах соседей')

    @staticmethod
    def standartization():
        df = pd.read_excel('matrix.xlsx', index_col=0)
        np_array = df.to_numpy()
        ls_array = np_array.tolist()
        for i in range(len(ls_array)):
            counter = 0
            for j in range(len(ls_array)):
                if ls_array[i][j] != 0:
                    counter += 1
            for h in range(len(ls_array)):
                if counter != 0:
                    x = ls_array[i][h] / counter
                    ls_array[i][h] = x

        np_array = np.array(ls_array)
        print(np_array)

