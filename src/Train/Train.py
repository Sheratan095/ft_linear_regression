import sys
import os
import json

# Ensure project src directory is on sys.path so Utils is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils.Data import load_data

def train_model(km, price, learning_rate=0.1, epochs=1000):
	"""
	Trains a linear regression model using gradient descent.
	"""
	m = len(km) # m is the number of examples in the dataset
	
	# Standardize data to ensure gradient descent converges correctly and quickly
	# Without this, the cost function could easily diverge due to the large scale of 'km'.
	km_mean = sum(km) / m
	km_std = (sum((x - km_mean) ** 2 for x in km) / m) ** 0.5
	
	price_mean = sum(price) / m
	price_std = (sum((y - price_mean) ** 2 for y in price) / m) ** 0.5
	
	km_norm = [(x - km_mean) / km_std for x in km]
	price_norm = [(y - price_mean) / price_std for y in price]
	
	# Initialize both thetas to 0 (as instructed)
	theta0 = 0.0
	theta1 = 0.0
	
	# Gradient Descent loop
	for epoch in range(epochs):
		# We need to accumulate the errors to calculate the mean gradient
		sum_error_theta0 = 0.0
		sum_error_theta1 = 0.0
		
		for i in range(m):
			# estimatePrice(mileage) = theta0 + (theta1 * mileage)
			estimate = theta0 + (theta1 * km_norm[i])
			error = estimate - price_norm[i]
			
			sum_error_theta0 += error
			# For theta1 we multiply the error by the input feature (mileage)
			sum_error_theta1 += error * km_norm[i]
		
		# Calculate tmp updates using the mathematical formulas:
		# tmp theta0 = learningRate * (1/m) * sum(estimate - price)
		tmp_theta0 = learning_rate * (1/m) * sum_error_theta0
		# tmp theta1 = learningRate * (1/m) * sum((estimate - price) * mileage)
		tmp_theta1 = learning_rate * (1/m) * sum_error_theta1
		
		# Simultaneously update the parameters by subtracting the gradient
		theta0 -= tmp_theta0
		theta1 -= tmp_theta1

	# After finding the parameters for normalized data, we need to scale them back 
	# so they can be plotted and used directly on unnormalized 'km' values by the Estimate program.
	# From: (price - price_mean) / price_std = theta0 + theta1 * (km - km_mean) / km_std
	# price = price_mean + price_std * theta0 + price_std * theta1 * (km - km_mean) / km_std
	# price = (price_mean + price_std * theta0 - price_std * theta1 * km_mean / km_std) + (price_std * theta1 / km_std) * km
	
	final_theta1 = theta1 * price_std / km_std
	final_theta0 = price_mean + (theta0 * price_std) - (final_theta1 * km_mean)

	return final_theta0, final_theta1

def save_thetas(theta0, theta1, filepath="data/theta.json"):
	"""
	Saves the trained thetas to a JSON file so they can be loaded by the Estimate program.
	"""
	try:
		with open(filepath, 'w') as f:
			json.dump({"theta0": theta0, "theta1": theta1}, f, indent=4)
		print(f"Model trained successfully! Saved theta0 and theta1 to {filepath}.")
	except IOError as e:
		print(f"Failed to save thetas: {e}")

def main():
	filePath = "data/data.csv"
	# Wait for data format which may return km, price
	data = load_data(filePath)
	if data is None or data[0] is None or data[1] is None:
		return
		
	km, price = data
	
	if len(km) == 0:
		print("Dataset is empty.")
		return
		
	print(f"Starting training on {len(km)} data points...")
	
	# Note: Using learning rate of 0.1 and 2000 epochs due to normalization
	theta0, theta1 = train_model(km, price, learning_rate=0.1, epochs=2000)
	
	print(f"Computed Theta0: {theta0}")
	print(f"Computed Theta1: {theta1}")
	
	save_thetas(theta0, theta1)

if __name__ == "__main__":
	main()
