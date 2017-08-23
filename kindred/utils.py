
import os
import zipfile
import hashlib
import requests
import logging
import traceback
import time

def _calcSHA256(filename):
	return hashlib.sha256(open(filename, 'rb').read()).hexdigest()

def _findDir(name, path):
	if os.path.isdir(path):
		for root, dirs, files in os.walk(path):
			if name in dirs:
				return os.path.abspath(os.path.join(root, name))
	return None

# From: https://stackoverflow.com/questions/32763720/timeout-a-file-download-with-python-urllib
def _downloadFile(url,filename,timeout=180):
	# Make the actual request, set the timeout for no data to 10 seconds and enable streaming responses so we don't have to keep the large files in memory
	request = requests.get(url, timeout=10, stream=True)

	# Open the output file and make sure we write in binary mode
	with open(filename, 'wb') as fh:
		downloadedSize = 0.0
		# Walk through the request response in chunks of 1024 * 1024 bytes, so 1MiB
		for chunk in request.iter_content(1024 * 1024):
			# Write the chunk to the file
			fh.write(chunk)
			# Optionally we can check here if the download is taking too long
			downloadedSize += (len(chunk) / float(1024*1024))

			currentDateTime = time.strftime("%Y/%m/%d %H:%M:%S")
			print("%s : Downloaded %.1f MB" % (currentDateTime,downloadedSize))
			

def _downloadFiles(files,downloadDirectory):
	#oldTimeout = socket.getdefaulttimeout()
	#ssl.SSLSocket.settimeout(180)

	if not os.path.isdir(downloadDirectory):
		os.mkdir(downloadDirectory)

	for url,shortName,expectedSHA256 in files:
		downloadedPath = os.path.join(downloadDirectory,shortName)
	
		print downloadedPath
		if os.path.isfile(downloadedPath):
			downloadedSHA256 = _calcSHA256(downloadedPath)
			if not downloadedSHA256 == expectedSHA256:
				os.remove(downloadedPath)
				print "HELLO"

		if not os.path.isfile(downloadedPath):
			#wget.download(url,out=downloadedPath,bar=None)
			try:
				_downloadFile(url,downloadedPath)
			except Exception as e:
				logging.error(traceback.format_exc())
				print(type(e))
				raise
			
			downloadedSHA256 = _calcSHA256(downloadedPath)
			assert downloadedSHA256 == expectedSHA256, "SHA256 mismatch with downloaded file: %s" % shortName
			
			if shortName.endswith('.zip'):
				zip_ref = zipfile.ZipFile(downloadedPath, 'r')
				zip_ref.extractall(path=downloadDirectory)
				zip_ref.close()

				os.remove(downloadedPath)
	
	#socket.setdefaulttimeout(oldTimeout)
