import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
    def standartization(file):
        df = pd.read_excel(file, index_col=0)
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
        return np_array


class ZStat:
    @staticmethod
    def z_statistics(dct_of_param):
        z_dct = {}
        params_lst = []
        sample_avg = 0

        for key in dct_of_param:
            params_lst.append(dct_of_param[key])
            sample_avg += dct_of_param[key]

        sample_avg = sample_avg / len(params_lst)

        intermediary = 0

        for elem in params_lst:
            intermediary += (elem - sample_avg) ** 2

        standard_deviation = (intermediary / len(params_lst)) ** 0.5

        index = 0
        for key in dct_of_param:
            z_dct[key] = (params_lst[index] - sample_avg) / standard_deviation
            index += 1

        return z_dct


class LocalMoranIndex:
    @staticmethod
    def l_index_calculation(weight_matrix, z_stat):
        z_stat_vector = []
        lisa_dict = {}
        lisa_vector = []

        for key in z_stat:
            z_stat_vector.append(z_stat[key])
            lisa_dict[key] = 0

        intrm_array = weight_matrix.tolist()

        for i in range(len(intrm_array)):
            for j in range(len(intrm_array[i])):
                intrm_array[i][j] = intrm_array[i][j] * z_stat_vector[i] * z_stat_vector[j]

        for elem in intrm_array:
            summary = 0
            for sub_elem in elem:
                summary += sub_elem
            lisa_vector.append(summary)

        index = 0
        for key in lisa_dict:
            lisa_dict[key] = lisa_vector[index]
            index += 1

        return lisa_dict


class GlobalMoranIndex:
    def __init__(self, lisa_dict):
        self.lisa_dict = lisa_dict
        self.result = 0
        self.number = 0
        for key in lisa_dict:
            self.result += lisa_dict[key]
            self.number += 1

    def __str__(self):
        return (f'Значение Ig = {self.result}'
                f'Значение E(I) = {-1 / (self.number - 1)}')

    def __repr__(self):
        return self.result


class MoranScatterplot:
    def __init__(self, weight_matrix, z_dict, lisa_dict):
        self.weight_matrix = weight_matrix
        self.z_dict = z_dict
        self.lisa_dict = lisa_dict
        self.z_vector = []
        self.l_vector = []
        self.places = []

        for key in self.z_dict:
            self.z_vector.append(z_dict[key])
            self.places.append(key)

        for key in self.lisa_dict:
            self.l_vector.append(lisa_dict[key])

        self.wz_vector = (np.array(self.weight_matrix) @ np.array(self.z_vector)).tolist()

    def quarter_definition(self):
        quarter_vector = []

        for i in range(len(self.places)):
            if self.z_vector[i] > 0 and self.wz_vector[i] > 0:
                quarter_vector.append('HH')
            elif self.z_vector[i] < 0 and self.wz_vector[i] > 0:
                quarter_vector.append('LH')
            elif self.z_vector[i] < 0 and self.wz_vector[i] < 0:
                quarter_vector.append('LL')
            elif self.z_vector[i] > 0 and self.wz_vector[i] < 0:
                quarter_vector.append('HL')
            else:
                quarter_vector.append('NA')
        return quarter_vector

    def dataframe(self):
        df = pd.DataFrame({'Муниципальное образование': self.places, 'z': self.z_vector, 'Wz': self.wz_vector,
                           'LISA': self.l_vector, 'Квадрант': MoranScatterplot.quarter_definition(self)})
        print(df)
        with open('diagram_dataframe.xlsx', 'w', encoding='utf8'):
            df.to_excel('diagram_dataframe.xlsx')

    def diagram(self):
        figure, axis = plt.subplots()
        axis.set_title("Диаграмма рессеяния Морана")

        axis.set_xlim(-10, 10)
        axis.set_ylim(-10, 10)
        axis.spines["left"].set_position("center")
        axis.spines["bottom"].set_position("center")
        axis.spines['top'].set_visible(False)
        axis.spines['right'].set_visible(False)
        axis.set_aspect("equal")
        plt.xlabel('z')
        plt.ylabel('Wz')

        x = np.array(self.z_vector)
        y = np.array(self.wz_vector)
        plt.scatter(x, y, s=12, c="#8B0000", marker="D")
        plt.show()


