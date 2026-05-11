import pandas as pd

def load_data(file_path):

	print(f"\nLoading data from {file_path}...")

	# Open the file and load the data into a pandas DataFrame
	try:
		data = pd.read_csv(file_path)

	except FileNotFoundError:
		print(f"ERROR: File {file_path} not found\n")
		return (None)
	
	except pd.errors.EmptyDataError:
		print(f"ERROR: File {file_path} is empty\n")
		return (None)

	except pd.errors.ParserError:
		print(f"ERROR: File {file_path} is not a valid CSV\n")
		return (None)


	# Check if the required columns 'km' and 'price' are present in all rows
	# Remove rows with missing values in 'km' or 'price' columns
	try:
		count_before_remove = len(data)
		data = data.dropna(subset=["km", "price"])
		count_after_remove = len(data)

		if count_after_remove == 0:
			print("Error: No valid data available after removing rows with missing values.\n")
			return (None)
		
		print(f"Removed {count_before_remove - count_after_remove} rows with missing values. Remaining rows: {count_after_remove}")

	except KeyError:
		print("Error: Required columns 'km' and/or 'price' not found in CSV.\n")
		return (None)


	# Check if all values in 'km' and 'price' columns are numeric and convert them to numpy arrays
	try:
		km_raw = data["km"].astype(float).to_numpy()
		price_raw = data["price"].astype(float).to_numpy()

	except ValueError as e:
		print(f"Error: Non-numeric value found in CSV: {e}\n")
		return (None)
	
	print("Data loaded successfully\n")

	return(km_raw, price_raw)
