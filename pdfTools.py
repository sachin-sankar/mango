from os import listdir , remove, rmdir
from os.path import getsize
from PIL import Image
import exceptions
from requests import get
import sites
from shutil import copyfileobj
from user_agent import generate_user_agent

def buildPdf(images : list,fileName : str):
	print(f'Building pdf {fileName}')
	converted = []
	for imageFile in images:
		image = Image.open(imageFile)
		converted.append(image.convert('RGB'))
		print(f'{imageFile} Converted')	
	converted[0].save(fileName,save_all=True,append_images=converted[1:])

	
def downloadImage(url : str,folder: str = ''):
	sizeDownloaded = 0
	try:
		res = get(url, stream = True,headers={'User-Agent':generate_user_agent(device_type='desktop')})
	except Exception as e:
		raise exceptions.CannotRetriveImage(e)
	fileName = url.split('/')[-1]
	if res.status_code == 200:
	    try:
		    with open(fileName,'wb') as f:
	        	copyfileobj(res.raw, f)
	        	print('Downloaded image',fileName)
	        	sizeDownloaded += getsize(fileName)
	        	return fileName
	    except FileExistsError:
	    	print(f'{fileName} aldready exists')
	else:
		raise exceptions.CannotRetriveImage(f'{url} : Response code {res.status_code}')
	print(f'Images downloaded for {sizeDownloaded} bytes')

def downloadImages(urlList : list,folder:str=''):
	imageFiles = []
	for url in urlList:
		imageFiles.append(downloadImage(url,folder))
	return imageFiles

def removeImages(imageUrls : str):
	for file in imageUrls:
		remove(file)