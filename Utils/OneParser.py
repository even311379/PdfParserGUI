'''
this script is for quick add new patterns in ScoreSheetParser.py

I just test things here, and add the parsers back to add more parsers,in case

'''

import pdftotext
import re
import regex
import os

target_folder = 'H:/DA_Work/pdfData/oo/manual/G0'
#target_file = 'H:/DA_Work/pdfData/oo/manual/G0/10149802.pdf'

#with open(target_file, "rb") as f:
#    pdf = pdftotext.PDF(f)

#scoresheet = pdf[2]
#with open('scoresheet.txt', "w+") as f:
#    f.write(scoresheet)

#print(scoresheet)

def test(scoresheet):
    try:
        name = re.findall('姓名：(\S+?)\s', scoresheet)[0]
        school = re.findall('(\S*?)[\s]*?學生個人成績單暨年級百分比對照表', scoresheet)[0]
        s1 = re.findall("智育成績([\s\S]*?)德育成績",scoresheet)[0]
        s2 = regex.findall("\s(\d?\d\.?\d?\d?)\s",s1, overlapped = True)
        print(s2[3::4][:-1])
        return True
    except:
        return False


A = 0
for pdffile in [target_folder + '\\' + f for f in os.listdir(target_folder)]:
    
    if not pdffile.endswith('.pdf'):
        continue
    with open(pdffile, "rb") as f:
        pdf = pdftotext.PDF(f)
    scoresheet = pdf[2]
    if test(scoresheet):
        A += 1
print(A)
