from os import path, environ
from kaggle import api

# Connector to connect to kaggle and download the datasets
# https://github.com/Kaggle/kaggle-api


class KaggleConnector:
	def __init__(self):
		# Get the user home directory
		self.user_home = path.expanduser("~")
		self.credentials_exists = path.exists(path.join(self.user_home, ".kaggle/kaggle.json")) or \
				("KAGGLE_USERNAME" in environ and "KAGGLE_KEY" in environ)

		if not self.credentials_exists:
			raise Exception("Kaggle credentials not found")
		else:
			api.authenticate()

	def download_dataset(self, dataset_name, output_dir):
		api.dataset_download_files(dataset_name, path=output_dir, unzip=True)

	def download_competition(self, competition_name, output_dir):
		api.competition_download_files(competition_name, path=output_dir, unzip=True)

	def list_competitions(self):
		return api.competitions_list()