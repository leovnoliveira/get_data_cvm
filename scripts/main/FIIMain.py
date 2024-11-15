from FIIDataHandler import FIIDataHandler

# Uso
handler = FIIDataHandler(start_year=2021, end_year=2023)
handler.download_data()
handler.extract_data()
handler.load_registration_data()
handler.clean_data()
handler.merge_data()
final_data = handler.get_final_data()
print(final_data)