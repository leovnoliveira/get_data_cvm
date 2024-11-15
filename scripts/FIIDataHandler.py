import ssl
import requests
import urllib3
import pandas as pd
import zipfile
import os

# Configurar cifras para o contexto SSL
context = ssl.create_default_context()
context.set_ciphers(':HIGH:!DH:!aNULL')

# Desabilitar avisos de SSL (opcional, use com cautela)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FIIDataHandler:

    def __init__(self, start_year = 2010, end_year = 2025):
        
        self.years = range(start_year, end_year)
        self.months = range(1, 13)
        self.base_url = 'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/'
        self.data_folder = os.getcwd()
        self.fii_data = pd.DataFrame()
        self.registartion_data = pd.DataFrame()

    def download_data(self):

        for year in self.years:
            for month in self.months:
                url = f'{self.base_url}inf_diario_fi_{year}{month:02}.zip'
                file_path = os.path.join(self.data_folder, f'inf_diario_fi_{year}{month:02}.zip')

                if not os.path.exists(file_path):

                    response = requests.get(url)
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f'Dados baixados para {year}-{month:02}')

                else:
                    print(f'Dados já existem para {year}-{month:02}')

    def extract_data(self):
        file_list = [file for file in os.listdir(self.data_folder) if file.startswith('inf_diario_fi')
        and file.endswith('.zip')]
        data_frames = []

        for file in file_list:
            file_path = os.path.join(self.data_folder, file)
        
        # Verifique se o arquivo é um ZIP válido
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as z:
                    for csv_file in z.namelist():
                        print(f'Processando {csv_file}')
                        df = pd.read_csv(z.open(csv_file), sep=';', encoding='ISO-8859-1')
                        data_frames.append(df)
            else:
                print(f"Aviso: {file_path} não é um arquivo zip válido")




        self.fii_data = pd.concat(data_frames, ignore_index=True)
        print("Extração dos dados completa.")
        
       
    
    def load_registration_data(self):

        url = 'https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv'
        response = requests.get(url)
        if response.status_code == 200:
            from io import StringIO
            csv_data = StringIO(response.text)
            self.registartion_data = pd.read_csv(csv_data, sep = ';', encoding = 'ISO-8859-1')
            self.registartion_data = self.registartion_data[['CNPJ_FUNDO', 'DENOM_SOCIAL']].drop_duplicates()
            print("Dados de registro carregados com sucesso.")

        else:
            print('Falha em acessar os dados. Erro:', response.status_code)
        self.registration_data = pd.read_csv(url, sep = ';', encoding='ISO-8859-1')
        

    def clean_data(self):
        if self.fii_data.empty:
            print('Sem dados de FII para limpar. Por favor, extraia-os primeiro')

        
        self.fii_data['DT_COMPTC'] = pd.to_datetime(self.fii_data['DT_COMPTC'], errors = 'coerce')
        data_inicio_mes = self.fii_data['DT_COMPTC'].sort_values().unique()[-0]
        data_fim_mes = self.fii_data['DT_COMPTC'].sort_values().unique()[-1]

        self.fii_data = self.fii_data[self.fii_data['DT_COMPTC'].isin([data_inicio_mes, data_fim_mes])]
        self.fii_data.dropna(inplace = True)
        print('Limpeza dos dados completa')

    def merge_data(self):
        if self.fii_data.empty or self.registration_data.empty:
            print('Falando dados para mergear. Por favor, insira os dados de registro e dos FII primeiro')

            return

        self.fii_data = pd.merge(
            self.fii_data,
            self.registration_data,
            how = 'left',
            left_on = ['CNPJ_FUNDO'],
            right_on = ['CNPJ_FUNDO']
        )
        
        self.fii_data = self.fii_data[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'DT_COMPTC', 'VL_QUOTA', 'VL_PATRIM_LIQ_x', 'VL_PATRIM_LIQ_y', 'NR_COTST']]
        print('Merge dos dados completo')
        print('Colunas após o merge:', self.fii_data.columns)

        required_columns = ['CNPJ_FUNDO', 'DENOM_SOCIAL', 'DT_COMPTC', 'VL_QUOTA', 'VL_PATRIM_LIQ',
                            'NR_COTST']
        missing_columns = [col for col in required_columns if col not in self.fii_data.columns]

        if missing_columns:
            print(f'As colunas seguintes estão ausentes após o merge: {missing_columns}')

        else:
            self.fii_data = self.fii_data[required_columns]
            print('Merge dos dados completo')
            print(self.fii_data.columns)


    def get_final_data(self):
        return self.fii_data
        






