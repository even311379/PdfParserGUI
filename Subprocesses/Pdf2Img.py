import sys
import os
import shutil
from pdf2image import convert_from_path

def Pdf2Imgs(FilePath):
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')
    images = convert_from_path(FilePath)
    os.mkdir('tmp')
    for i, img in enumerate(images):
        img.save(f'tmp/{i}.png')

if __name__ == "__main__":
    path = str(sys.argv[1])    
    Pdf2Imgs(path)
