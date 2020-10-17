import requests
import shutil

class ImageUtils:

	def write_image_to_file(self, image_url, file_path):
		try:
			response = requests.get(image_url, stream=True)
		except Exception as e:
			print('[x] Failed to get image url: {}'.format(image_url))
			print(e)
			return

		if(response.status_code != 200):
			print('[x] Could Not Connect to IMDb')
			return

		response.raw.decode_content = True

		file = open(file_path, "wb+")
		print('Saving {}'.format(file_path))
		shutil.copyfileobj(response.raw, file)
		#file.write(response.content)
		file.close()