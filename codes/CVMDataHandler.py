import os
import zipfile
import requests
import pandas as pd

class CVMDataHandler:

    def __init__(self, start_year=2010, end_year=2025):

        self.years = range(start_year, end_year)
        self.url_base = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/'
        self.data_folder = os.getcwd()
        self.data = pd.DataFrame()

    def download_data(self):

        for year in self.years:
            url = f'{self.url_base}DFP/DADOS/dfp_cia_aberta_{year}.zip'
            file_path = os.path.join(self.data_folder, f'dfp_cia_aberta_{year}.zip')

            if not os.path.exists(file_path):
                response = requests.get(url)

                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f'Downloaded data for {year}')

            else:
                print(f'Data for {year} already downloaded')

    def extract_data(self):

        file_list = [file for file in os.listdir(self.data_folder) if file.endswith('.zip')]
        demonstrations = []

        for file in file_list:

            with zipfile.ZipFile(file) as z:

                year = file[-8:-4]
                for csv_file in z.namelist():

                    print(f'Processando {csv_file} de {year}')
                    
                    chunked_data = pd.read_csv(z.open(csv_file), sep = ';',
                                                      decimal = ',',
                                                      encoding = 'ISO-8859-1',
                                                      chunksize = 10000)
                    
                    df = pd.concat(chunked_data, ignore_index= True)

                    df['tipo_doc'] = 'dfp'
                    demonstrations.append(df)

                self.data = pd.concat(demonstrations, ignore_index= True)
                print('Carregamento e extração de dados completa!')

    def clean_data(self):
        if self.data.empty:
            print("Sem dados para limpar! Por favor, extraia-os antes.")
            return

        self.data[['con_ind', 'tipo_dem']] = self.data['GRUPO_DFP'].str.split("-", expand=True)
        self.data['tipo_dem'] = self.data['tipo_dem'].str.strip()
        self.data['con_ind'] = self.data['con_ind'].astype(str)

        # Remove unnecessary columns
        self.data = self.data.loc[:, ~self.data.columns.isin(['ST_CONTA_FIXA', 'COLUNA_DF', 'GRUPO_DFP'])]
        # Filter rows
        self.data = self.data[self.data['ORDEM_EXERC'] != 'PENÚLTIMO']

    def get_unique_companies(self):
        if self.data.empty:
            print("Sem dados disponíveis. Por favor, limpe-os antes")
            return []
        return self.data['DENOM_CIA'].unique()

    def get_data(self):
        return self.data

# Usage
handler = CVMDataHandler(start_year=2020, end_year=2025)
handler.download_data()
handler.extract_data()
handler.clean_data()
unique_companies = handler.get_unique_companies()
print(unique_companies)

