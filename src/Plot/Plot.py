import matplotlib.pyplot as plt  # type: ignore[import-untyped]
import sys
import os
import json

# Add the project root to sys.path to allow importing from Utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils.Data import load_data

# Use a dark style for plots by default and set darker frame colors
plt.style.use('dark_background')
# Set figure and axes background to a deep dark color and text to white for readability
plt.rcParams['figure.facecolor'] = '#121212'
plt.rcParams['axes.facecolor'] = '#121212'
plt.rcParams['savefig.facecolor'] = '#121212'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

def main(args):

	# Parse command-line arguments
	# Expected: python Plot.py <data_file_path> [--data-only|--regression-only|--both]
	# Default behavior is to plot both
	
	if len(args) < 1:
		print("Usage: python Plot.py <data_file_path> [--data-only|--regression-only|--both]\n")
		print("  --data-only:        Plot only the data points")
		print("  --both:             Plot both data and regression line (default)\n")
		return

	filePath = args[0]
	plot_mode = "both"  # Default mode
	
	# Check if a plot mode flag was provided
	if len(args) > 1:
		mode_arg = args[1].lower()
		if mode_arg in ["--data-only", "--both"]:
			plot_mode = mode_arg.lstrip("--")
		else:
			print(f"Warning: Unknown argument '{args[1]}'. Using default mode 'both'.\n")

	km, price = load_data(filePath)

	if km is None or price is None:
		print("Error: Could not load data.")
		return

	plot_data(km, price, plot_mode)


def load_thetas(filepath="data/theta.json"):
	"""
	Loads the trained thetas from the JSON file.
	If the file doesn't exist or can't be read, returns default values (0, 0).
	"""
	if not os.path.exists(filepath):
		print(f"Warning: {filepath} not found. Using default thetas (0, 0).")
		return 0.0, 0.0
	
	try:
		with open(filepath, 'r') as f:
			data = json.load(f)
			return data.get("theta0", 0.0), data.get("theta1", 0.0)
	except (IOError, json.JSONDecodeError):
		print("Error reading thetas file. Using default values (0, 0).")
		return 0.0, 0.0


def plot_data(km, price, plot_mode="both"):
	"""
	Plots the data and/or regression line based on the specified mode.
	
	Args:
		km: Array of kilometer values
		price: Array of price values
		plot_mode: One of "data-only", "regression-only", or "both"
	"""

	# Load the trained parameters (theta0 and theta1) from the training program
	theta0, theta1 = load_thetas()
	
	# Create the figure and axes
	fig = plt.figure(figsize=(10, 6), facecolor=plt.rcParams['figure.facecolor'])
	ax = fig.add_subplot(1, 1, 1, facecolor=plt.rcParams['axes.facecolor'])
	
	# Plot data points if requested
	if plot_mode in ["data-only", "both"]:
		ax.scatter(km, price, color='cyan', edgecolors='white', label='Data', s=50)
	
	# Plot regression line if requested
	if plot_mode in ["both"]:
		# Calculate and plot the regression line
		# The regression line is defined by: price = theta0 + theta1 * mileage
		# We calculate the line by finding the price at the min and max mileage values
		km_min = min(km)
		km_max = max(km)
		
		# Create two points on the regression line (at min and max km values)
		# This allows us to draw a line across the entire data range
		line_km = [km_min, km_max]
		line_price = [theta0 + theta1 * km_min, theta0 + theta1 * km_max]
		
		# Plot the regression line in a distinct color
		ax.plot(line_km, line_price, color='red', linewidth=2, label=f'Regression Line (θ₀={theta0:.2f}, θ₁={theta1:.6f})')
	
	# Set titles and labels
	ax.set_title('Kilometers vs Price with Linear Regression')
	ax.set_xlabel('Kilometers (km)')
	ax.set_ylabel('Price')
	ax.legend()
	ax.grid(True, color='gray', alpha=0.3)
	plt.show()



if __name__ == "__main__":
	main(sys.argv[1:])
