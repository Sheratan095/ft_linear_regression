import sys
import os

# Ensure project src directory is on sys.path so `Utils` package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils.Data import load_data


def main():
	filePath = "data/data.csv"
	km, price = load_data(filePath)
	if km is None or price is None:
		return

	print(f"Kilometers: {km}, count = {len(km)}")
	print(f"Prices: {price}, count = {len(price)}")



if __name__ == "__main__":
	main()