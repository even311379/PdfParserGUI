'''
Test whether new added parser can actually parse some in manual group

'''
try:
    from Subprocesses.ScoreSheetParsers import complete_patterns, missing_patterns
except:
    from ScoreSheetParsers import complete_patterns, missing_patterns

import os

def ParseProcess(ListOfPath):
    DD = []
    Failed_files = []
    for f in ListOfPath:
        R = complete_patterns(f)
        if type(R) == list:
            if len(R) != 20:                
                Failed_files.append(f)
                continue            
            DD.append(R)
        
        elif R == 'skipped':
            RM = missing_patterns(f) # result of missing
            if RM:
                if len(RM) != 20:
                    Failed_files.append(f)
                    continue
                DD.append(RM)
            else:
                Failed_files.append(f)
        else:
            Failed_files.append(f)

    return DD, Failed_files


if __name__ == '__main__':
    WDIR = "H:\DA_Work\pdfData\oo\manual\G0"
    all_pdf_files = [f'{WDIR}/{ff}' for ff in os.listdir(WDIR) if ff.endswith('.pdf')]
    DD, _ = ParseProcess(all_pdf_files)
    print(len(DD))


