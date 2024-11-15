from DFPDataHandler import DFPDataHandler

# Uso
handler = DFPDataHandler(start_year=2020, end_year=2025)
handler.download_data()
handler.extract_data()
handler.clean_data()
unique_companies = handler.get_unique_companies()
print(unique_companies)