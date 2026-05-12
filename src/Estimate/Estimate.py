import json
import os

def load_thetas(filepath="data/theta.json"):
	"""
	Attempts to load the previously saved thetas from the JSON file.
	If the file cannot be accessed (e.g. model not trained yet), 
	it returns 0 for both parameters, as instructed.
	"""
	if not os.path.exists(filepath):
		print(f"Warning: Model not trained yet or {filepath} not found. Using default values (0).")
		return (0.0, 0.0)
	
	try:
		with open(filepath, 'r') as f:
			data = json.load(f)
			return (data.get("theta0", 0.0), data.get("theta1", 0.0))

	except (IOError, json.JSONDecodeError):
		print("Error reading thetas file. Using default values (0).")
		return (0.0, 0.0)

def predict_price(mileage, theta0, theta1):
	"""
	Uses the linear regression hypothesis: estimatePrice(mileage) = theta0 + (theta1 * mileage)
	to predict the price of a car for a given mileage.
	"""
	return (theta0 + (theta1 * mileage))

def main():
	# Load the parameters (which might be 0 if train_model hasn't been run)
	theta0, theta1 = load_thetas()
	
	# Prompt the user continuously until they quit
	while True:
		try:
			# Get input from the user
			user_input = input("Enter a car's mileage to estimate its price (or type 'quit' to exit): ")
			
			# Check for quitting mechanism
			if user_input.strip().lower() in ['quit', 'q', 'exit']:
				break
				
			# Convert user input to float
			mileage = float(user_input)
			
			if mileage < 0:
				print("Mileage cannot be negative. Please enter a positive number.\n")
				continue
			
			# Use the specified hypothesis formula
			estimated_price = predict_price(mileage, theta0, theta1)
			
			# Give back the estimated price
			# Ensure price doesn't go below 0 purely mathematically
			estimated_price_clamped = max(0.0, estimated_price)
			print(f"The estimated price for {mileage} km is: {estimated_price_clamped:.2f}\n")
			
		except ValueError:
			print("Invalid input! Please enter a numeric value for the mileage.\n")

		except EOFError:
			# Handles unexpected interactions (like pressing Ctrl+D)
			break

if __name__ == "__main__":
	main()
