import moran_index

list_of_places, dict_of_parameter = moran_index.LoadData('test_data.txt').file_processing()
moran_index.SpatialWeightMatrix.matrix_creation(list_of_places)
