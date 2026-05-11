import pandas as pd

def main():
	filePath = "data/data.csv"
	data = loadData(filePath)
	if data is None:
		return

	print("Data loaded successfully:")
	print(data.head())

def loadData(filePath):

	try:
		data = pd.read_csv(filePath)

	except FileNotFoundError:
		print(f"ERROR: File {filePath} not found")
		return None
	
	except pd.errors.EmptyDataError:
		print(f"ERROR: File {filePath} is empty")
		return None

	except pd.errors.ParserError:
		print(f"ERROR: File {filePath} is not a valid CSV")
		return None

	return data

if __name__ == "__main__":
	main()