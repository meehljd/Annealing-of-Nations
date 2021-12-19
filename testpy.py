from utils.data_manager import DataManager

# Import List of Airports from Google Sheets API
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
print(sheet_data)
# Create Combinations of


