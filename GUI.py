from __future__ import absolute_import
import sys
import pygame
import OpenGL.GL as gl
from imgui.integrations.pygame import PygameRenderer
import imgui


import matplotlib.pyplot as plt
import numpy as np
import os

import Utils.GUI_Functions as GF
import Utils.GUI_Elements as GE

import subprocess

#from Subprocesses import ParseScoreSheet

def main():

    # Theme Index
    THEME_INDEX = 2

    # window visible params
    bShowInfoPopUp = False
    bShowFiles = True
    bShowParsePdf = True
    bShowParserStatics = True

    bShowImg = False
    bShowTestWindow = True


    #delete cache files
    if os.path.isfile('ParseResult.log'):
        os.remove('ParseResult.log')
    if os.path.isfile('ManualFiles.log'):
        os.remove('ManualFiles.log')
    if os.path.isfile('Cluster.png'):
        os.remove('Cluster.png')

    pygame.init()    
    size = 1280, 720 # 720p
    # size = 1920, 1080 # 1080p

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE  )
    pygame.display.set_caption("PDF成績單解析器")
    
    clock = pygame.time.Clock()

    favicon = pygame.image.load('asset\\Logo.png')
    pygame.display.set_icon(favicon)

    imgui.create_context()
    
    impl = PygameRenderer()        

    io = imgui.get_io()
    smallfont = io.fonts.add_font_from_file_ttf("asset\\NotoSansTC-Black.otf", 12, io.fonts.get_glyph_ranges_chinese_full())
    normalfont = io.fonts.add_font_from_file_ttf("asset\\NotoSansTC-Black.otf", 16, io.fonts.get_glyph_ranges_chinese_full())
    largefont = io.fonts.add_font_from_file_ttf("asset\\NotoSansTC-Black.otf", 28, io.fonts.get_glyph_ranges_chinese_full())
    io.fonts.add_font_default()
    impl.refresh_font_texture()
    io.display_size = size

    style = imgui.get_style()
    if THEME_INDEX == 1: 
        GF.SetCustomStyle1(style)            
    elif THEME_INDEX == 2:
        GF.SetCustomStyle2(style)            
    elif THEME_INDEX == 3:
        GF.SetCustomStyle3(style)
                
    CV = 0
    MV = 200
    while 1:
        clock.tick(30) # fixed 15 fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # remove cache here
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                print('resize is triggered!')

            # shortcut bindings
            if event.type == pygame.KEYDOWN:
                if event.mod == pygame.KMOD_LCTRL and event.key == pygame.K_q:
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    GF.OpenHelper()

            impl.process_event(event)
        imgui.push_style_var(imgui.STYLE_FRAME_PADDING,(10,12.5))
        imgui.new_frame()

        # Main menu region
        if imgui.begin_main_menu_bar():
            with imgui.font(normalfont):
                if imgui.begin_menu("設定", True):
                    if imgui.begin_menu(label= "主題", enabled = True):
                        if THEME_INDEX == 1:
                            imgui.menu_item("默認", None, True, True)
                        else:
                            c, _ = imgui.menu_item("默認", None, False, True)
                            if c:
                                GF.SetCustomStyle1(style)
                                THEME_INDEX = 1
                        if THEME_INDEX == 2:
                            imgui.menu_item("CorporateGrey", None, True, True)
                        else:
                            c, _ = imgui.menu_item("CorporateGrey", None, False, True)
                            if c:
                                GF.SetCustomStyle2(style)
                                THEME_INDEX = 2
                        if THEME_INDEX == 3:
                            imgui.menu_item("Light", None, True, True)
                        else:
                            c, _ = imgui.menu_item("Light", None, False, True)
                            if c:
                                GF.SetCustomStyle3(style)
                                THEME_INDEX = 3
                        imgui.end_menu()

                    clicked_quit, selected_quit = imgui.menu_item("Quit", "L-Ctrl + Q", False, True)
                    if clicked_quit:
                        sys.exit()
                    imgui.end_menu()

                if imgui.begin_menu("視窗", True):
                    if not bShowFiles:
                        F, _ = imgui.menu_item(label = "選擇目錄", shortcut = None, selected = False, enabled = True)
                    else:
                        F, _ = imgui.menu_item(label = "選擇目錄", shortcut = None, selected = True, enabled = True)
                    if F:
                        bShowFiles = not bShowFiles                                                                
                    if not bShowParsePdf:
                        o, _ = imgui.menu_item(label = "解析成績單",shortcut = None, selected = False, enabled = True)
                    else:
                        o, _ = imgui.menu_item(label = "解析成績單",shortcut = None, selected = True, enabled = True)
                    if o:
                        bShowParsePdf = not bShowParsePdf
                    if not bShowParserStatics:
                        r, _ = imgui.menu_item(label = "解析結果",shortcut = None, selected = False, enabled = True)
                    else:
                        r, _ = imgui.menu_item(label = "解析結果",shortcut = None, selected = True, enabled = True)
                    if r:
                        bShowParserStatics = not bShowParserStatics

                    imgui.end_menu()

                if imgui.begin_menu("資訊", True):
                    I, _ = imgui.menu_item("關於", None, selected = False, enabled = True)
                    h, _ = imgui.menu_item("幫助", shortcut = "F1", selected = False, enabled = True)
                    if I:
                        bShowInfoPopUp = True
                        
                    if h:
                        GF.OpenHelper()


                    imgui.end_menu()

            #imgui.pop_style_var(1)
            imgui.end_main_menu_bar()

        # Conditional windows
        if bShowFiles:
            imgui.set_next_window_position(0, 35,imgui.ONCE)
            imgui.set_next_window_size(230, 685,imgui.ONCE)
            with imgui.font(normalfont):
                bFileWindow = imgui.begin("選擇目錄", True, flags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE)  
                if not bFileWindow[1]:
                    bShowFiles = False
                GE.FileWindow()
                imgui.end()

        if bShowParsePdf:
            imgui.set_next_window_position(230, 35, imgui.ONCE)
            imgui.set_next_window_size(450, 685, imgui.ONCE)
            with imgui.font(normalfont):
                bParsePdf = imgui.begin("解析成績單", True)
                if not bParsePdf[1]:
                    bShowParsePdf = False
                GE.ParsePdfWidget()
                imgui.end()

        if  bShowParserStatics:
            imgui.set_next_window_position(680, 35, imgui.ONCE)
            imgui.set_next_window_size(600, 685, imgui.ONCE)
            with imgui.font(normalfont):
                bParserStats = imgui.begin("解析結果", True)
                if not bParserStats[1]:
                     bShowParserStatics = False
                GE.ParserStaticsWidget()
                if os.path.isfile('Cluster.png'):            
                    img_info = GF.loadImage('Cluster.png')
                    imgui.image(img_info[0], img_info[1], img_info[2]) 
                imgui.end()

        if (bShowInfoPopUp):
            imgui.open_popup("資訊")

        imgui.set_next_window_size(600, 300)
        imgui.font(normalfont)
        if imgui.begin_popup_modal(title = "資訊", visible = True, flags = 0)[0]:                
            GE.ProgramInfoPopup()                
            imgui.separator()
            bShowInfoPopUp = False
            imgui.end_popup()       
            
        if THEME_INDEX == 1: 
            gl.glClearColor(0.1, 0.1, 0.1, 1) # for default theme
        elif THEME_INDEX == 2:
            gl.glClearColor(0.45, 0.55, 0.6, 1) # for light theme
        elif THEME_INDEX == 3:
            gl.glClearColor(0.25, 0.25, 0.25, 1.00)

        imgui.pop_style_var()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()


        CV += 1


        #738C99
if __name__ == "__main__":
    main()
