import moran_index

list_of_places, dict_of_parameter = moran_index.LoadData('test_data.txt').file_processing()
weight_matrix = moran_index.SpatialWeightMatrix.standartization('matrix nso.xlsx')
z_stat = moran_index.ZStat.z_statistics(dict_of_parameter)
lisa = moran_index.LocalMoranIndex.l_index_calculation(weight_matrix, z_stat)
g_index = moran_index.GlobalMoranIndex(lisa)
print(weight_matrix)
print(z_stat)
print(lisa)
print(g_index)
visualizing = moran_index.MoranScatterplot(weight_matrix, z_stat, lisa)
visualizing.dataframe()
visualizing.diagram()
