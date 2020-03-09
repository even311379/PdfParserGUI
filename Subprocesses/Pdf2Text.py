import sys
import time
import os
import pdftotext

def WritePdfText(fp):
	with open(fp, "rb") as f:
		pdf = pdftotext.PDF(f)
	for i in range(len(pdf)):
		if  not os.path.isdir('tmp'):
			time.sleep(10)
		with open(f'tmp/{i}.txt', 'w+', encoding='utf-8') as nf:
			nf.write(pdf[i])


if __name__ == "__main__":	
	fp = str(sys.argv[1])
	WritePdfText(fp)