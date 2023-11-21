import os
class Exportacao:
    
    def __init__(self, exportar = '../../data_set/house_data_transformado.csv'):
        self.exportar = exportar

    def exportar (self, data_set):
        path_to_export = self.exportar
        #path = '../../data_set/house_data_transformado.csv'
        data_set.to_csv(path_to_export, index=False)

    def teste_exportar (self):

        if os.path.exists(self.exportar) == False:
            data_set_exportado = 0
            return data_set_exportado, 0

        else:
            data_set_exportado = 1
            return data_set_exportado, self.exportar