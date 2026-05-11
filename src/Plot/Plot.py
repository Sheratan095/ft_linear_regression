import matplotlib.pyplot as plt  # type: ignore[import-untyped]
import sys
import os

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

	if (len(args) != 1):
		print("Usage: python Plot.py <data_file_path>\n")
		return
	filePath = args[0]

	km, price = load_data(filePath)

	if km is None or price is None:
		print("Error: Could not load data.")
		return

	plot_data(km, price)


def plot_data(km, price):
	# Plot the data points in a scatter plot using colors suitable for dark background.
	fig = plt.figure(figsize=(10, 6), facecolor=plt.rcParams['figure.facecolor'])
	ax = fig.add_subplot(1, 1, 1, facecolor=plt.rcParams['axes.facecolor'])
	ax.scatter(km, price, color='cyan', edgecolors='white', label='Data')
	ax.set_title('Kilometers vs Price')
	ax.set_xlabel('Kilometers (km)')
	ax.set_ylabel('Price')
	ax.legend()
	ax.grid(True, color='gray', alpha=0.3)
	plt.show()



if __name__ == "__main__":
	main(sys.argv[1:])
