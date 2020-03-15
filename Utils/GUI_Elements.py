import imgui
from imgui.integrations.pygame import PygameRenderer
import Utils.GUI_Functions as GF
import GUI

import tkinter as tk
from tkinter import filedialog

import os
import subprocess


imgui.create_context()
io = imgui.get_io()
smallfont = io.fonts.add_font_from_file_ttf("asset\\NotoSansTC-Black.otf", 12, io.fonts.get_glyph_ranges_chinese_full())
normalfont = io.fonts.add_font_from_file_ttf("asset\\NotoSansTC-Black.otf", 16, io.fonts.get_glyph_ranges_chinese_full())
largefont = io.fonts.add_font_from_file_ttf("asset\\NotoSansTC-Black.otf", 28, io.fonts.get_glyph_ranges_chinese_full())

WDIR = ""
ODIR = ""
LoadedFile = ""
InstIndex = 0
PersonIndex = 0
AllFileStatus = "尚未檢查"
N_Group = 10

def TkFileDialog():
    root = tk.Tk()
    root.withdraw()
    rep = filedialog.askdirectory(parent=root, initialdir=WDIR)
    root.destroy()
    return rep
        
def ProgramInfoPopup():    

    with imgui.font(largefont):
        imgui.text("軟體資訊")
        imgui.separator()
    imgui.bullet_text("版本: 0.1 alpha")
    imgui.bullet_text("開發: PUF STUDIO")
    imgui.bullet_text("Email: even311379@hotmail.com")
    imgui.bullet_text("Git Repo: https://github.com/even311379/PdfParserGUI")


def FileWindow():
    '''
    string wdir, path to project folder
    '''
    global WDIR
    global LoadedFile
    global InstIndex
    global PersonIndex
    global ReloadPDF
      
    if not WDIR:
        imgui.dummy(50, 0)
        imgui.same_line()
        if imgui.button("選擇推甄資料目錄"):
            WDIR = TkFileDialog()
            
    else:
        imgui.text("現行推甄資料目錄:")
        imgui.push_text_wrap_position(150)
        imgui.text(WDIR)
        imgui.dummy(80,0)
        imgui.same_line()
        if imgui.button("變更"):
            WDIR = TkFileDialog()
        imgui.separator()
        if GF.CheckWDIR(WDIR):
            imgui.text('目前系所:')
            IList = os.listdir(WDIR)
            _, InstIndex = imgui.combo("", InstIndex, IList)
            imgui.text('學生編號:')
            PersonList = os.listdir(WDIR+'/'+IList[InstIndex])
            _, PersonIndex = imgui.listbox("", PersonIndex, PersonList, 15)
            imgui.text(f"目前檔案: {PersonList[PersonIndex]}")
            if imgui.button("查看檔案"):
                os.startfile(f'{WDIR}/{IList[InstIndex]}/{PersonList[PersonIndex]}/{PersonList[PersonIndex]}.pdf')                
                    
        else:
            with imgui.font(largefont):
                imgui.text('目錄錯誤，請重選!')


def ParsePdfWidget():
    '''
    Use subprocess.Popen to run another script in background
    '''
    global WDIR
    global ODIR
    global N_Group
    global AllFileStatus

    with imgui.font(largefont):
        imgui.text("Step 1: 設定工作目錄")
    imgui.bullet_text("設定好推甄資料的目錄。")
    if WDIR:
        imgui.separator()
        with imgui.font(largefont):
            imgui.text("Step 2: 檢查各別檔案")
        imgui.push_text_wrap_position(450)
        imgui.bullet_text("檔案命名有些錯誤，需要額外調整，如: 10054818.pdf 變為10054818_1.pdf")
        imgui.dummy(50, 0)
        imgui.same_line()
        if imgui.button("檢查檔案"):
            AllFileStatus = GF.CheckAllFiles(WDIR)
        imgui.push_text_wrap_position(450)
        imgui.text(AllFileStatus)
        imgui.separator()
        with imgui.font(largefont):
            imgui.text("Step 3: 執行程式-解析成績單內容")    
        imgui.dummy(50, 0)
        imgui.same_line()
        if imgui.button("設定輸出目錄"):
            ODIR = TkFileDialog()    
        if ODIR != "":
            imgui.text("輸出目錄位置:")
            imgui.push_text_wrap_position(250)
            imgui.text(ODIR)
            imgui.dummy(50, 0)
            imgui.same_line()
            if imgui.button("開始解析"):
                if WDIR == "":
                    imgui.text("請設定檔案目錄")
                else:
                    subprocess.run(["python","Subprocesses/ParseScoreSheet.py", WDIR, ODIR])                        
        imgui.separator()
    if os.path.isfile('ManualFiles.log'):
        with imgui.font(largefont):
            imgui.text("Step 4: 執行程式-手動檔案分類")
        imgui.push_item_width(150)
        changed, N_Group = imgui.slider_int("幾群?", N_Group, min_value = 2, max_value = 20)
        imgui.text(f"分成{N_Group}群")        
        if imgui.button("開始分群"):
            subprocess.run(["python","Subprocesses/GroupPdf.py", ODIR, str(N_Group)])
        imgui.separator()
    if os.path.isdir(ODIR+"/Manual"):
        with imgui.font(largefont):
            imgui.text("Step 5: 手動處理")
            imgui.push_text_wrap_position(250)
            imgui.text("""
            恭喜~~~
            只剩下一咪咪手動的作業就能完工了!!

            祝你有美好的一天!!
            你現在可以關閉這個程式。
            """)


    
def ParserStaticsWidget():
    imgui.push_text_wrap_position(600)
    if os.path.isfile('ParseResult.log'):
        with imgui.font(largefont):
            imgui.text("結果")
        with open('ParseResult.log', 'r') as f:
            imgui.text(f.read())
        imgui.separator()        
        imgui.text("Run a hierarchical clustering to check how many potential groups?")
        if imgui.button("RUN"):
            subprocess.run(["python","Subprocesses/CheckGroup.py"])       
    else:
        imgui.text("尚未解析推甄資料中的成績單內容")



def ProgessBar(CV, MV, BarSize = 200):
    if CV >= MV:
        CV = MV
    imgui.dummy(10, 20)
    draw_list = imgui.get_window_draw_list()
    sp = imgui.get_item_rect_min()
    ep = imgui.get_item_rect_max()
    draw_list.add_rect(sp[0]+60,ep[1], sp[0]+60 + BarSize ,sp[1], imgui.get_color_u32_rgba(0.098, 0.098, 0.439, 1))
    draw_list.add_rect_filled(sp[0]+60,ep[1], sp[0]+60 + CV/MV * BarSize ,sp[1], imgui.get_color_u32_rgba(0.098, 0.098, 0.439, 1))
    draw_list.add_text(sp[0]+60 + BarSize + 10, sp[1] + 2, imgui.get_color_u32_rgba(1,0.5,0.5,1), f'{round(CV/MV* 100, 2)} %')    

    
'''

use the following stuff to set size of windows if resize.

https://github.com/ocornut/imgui/issues/933

however, this will disable user resize...

prevent user to resize to very ugly size:

imgui.push_style_var(imgui.STYLE_WINDOW_MIN_SIZE, (x,y,))
imgui.text("Alpha text")
imgui.pop_style_var(1)


##wrap text
imgui.core.push_text_wrap_position()

'''