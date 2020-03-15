import webbrowser
import os
import shutil
import OpenGL.GL as gl
import pygame
from pdf2image import convert_from_path


def OpenHelper():
    webbrowser.open('https://github.com/even311379/PdfParserGUI', new=2)

def CheckWDIR(wdir):
    try:
        f0 = os.listdir(wdir)[3]
        f1 = os.listdir(wdir+'/'+ f0)[0]
        t_pdf = os.listdir(wdir+'/'+f0+'/'+f1)[0]
        if '.pdf' in t_pdf:
            return True
        else:
            return False

    except:
        return False	

def CheckAllFiles(WDIR):
    upper_most = WDIR
    all_pdf_files = [ f'{upper_most}/{i}/{j}/{j}.pdf' for i in os.listdir(upper_most) for j in os.listdir(upper_most+'/'+i) ]
    N_NameError = 0
    ErrorPath = []
    for f in all_pdf_files:
        if not os.path.exists(f):
            N_NameError += 1
            ErrorPath.append(f)
    
    if N_NameError:
        s = "**發現命名錯誤**: \n"
        for path in ErrorPath:
            s += path + '\n'
        return s
    else:
        return "一切正常"


def loadImage(image_name):

    image = pygame.image.load(image_name)
    textureSurface = pygame.transform.flip(image, False, True)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA,
                 gl.GL_UNSIGNED_BYTE, textureData)

    return texture, width, height

def Pdf2Imgs(FilePath):
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')
    images = convert_from_path(FilePath)
    os.mkdir('tmp')
    for i, img in enumerate(images):
        img.save(f'tmp/{i}.png')

    return FilePath

def SetCustomStyle1(style):
    '''
    style from https://github.com/ocornut/imgui/issues/707#issuecomment-252413954
    '''
    style.window_rounding = 5.3    
    style.frame_rounding = 2.3
    style.scrollbar_rounding = 0

    style.colors[0] = (0.90, 0.90, 0.90, 0.90) # ImGuiCol_Text
    style.colors[1] = (0.60, 0.60, 0.60, 1.00) #ImGuiCol_TextDisabled
    style.colors[2] = (0.09, 0.09, 0.15, 1.00) #ImGuiCol_WindowBg
    style.colors[3] = (0.00, 0.00, 0.00, 0.00) #ImGuiCol_ChildWindowBg
    style.colors[4] = (0.05, 0.05, 0.10, 0.85) #ImGuiCol_PopupBg
    style.colors[5] = (0.70, 0.70, 0.70, 0.65) #ImGuiCol_Border
    style.colors[6] = (0.00, 0.00, 0.00, 0.00) # ImGuiCol_BorderShadow
    style.colors[7] = (0.00, 0.00, 0.01, 1.00) # ImGuiCol_FrameBg
    style.colors[8] = (0.90, 0.80, 0.80, 0.40) # ImGuiCol_FrameBgHovered
    style.colors[9] = (0.90, 0.65, 0.65, 0.45) #ImGuiCol_FrameBgActive
    style.colors[10] = (0.00, 0.00, 0.00, 0.83) #ImGuiCol_TitleBg
    style.colors[11] = (0.40, 0.40, 0.80, 0.20) #ImGuiCol_TitleBgCollapsed
    style.colors[12] = (0.00, 0.00, 0.00, 0.87) # ImGuiCol_TitleBgActive
    style.colors[13] = (0.01, 0.01, 0.02, 0.80) #ImGuiCol_MenuBarBg
    style.colors[14] = (0.20, 0.25, 0.30, 0.60) #ImGuiCol_ScrollbarBg
    style.colors[15] = (0.55, 0.53, 0.55, 0.51) #ImGuiCol_ScrollbarGrab
    style.colors[16] = (0.56, 0.56, 0.56, 1.00) #ImGuiCol_ScrollbarGrabHovered
    style.colors[17] = (0.56, 0.56, 0.56, 0.91) #ImGuiCol_ScrollbarGrabActive
    style.colors[18] = (0.10, 0.10, 0.10, 0.99) #ImGuiCol_ComboBg
    style.colors[19] = (0.90, 0.90, 0.90, 0.83) #ImGuiCol_CheckMark
    style.colors[20] = (0.70, 0.70, 0.70, 0.62) #ImGuiCol_SliderGrab
    style.colors[21] = (0.30, 0.30, 0.30, 0.84) #ImGuiCol_SliderGrabActive
    style.colors[22] = (0.48, 0.72, 0.89, 0.49) #ImGuiCol_Button
    style.colors[23] = (0.50, 0.69, 0.99, 0.68) #ImGuiCol_ButtonHovered
    style.colors[24] = (0.80, 0.50, 0.50, 1.00) #ImGuiCol_ButtonActive
    style.colors[25] = (0.30, 0.69, 1.00, 0.53) #ImGuiCol_Header
    style.colors[26] = (0.44, 0.61, 0.86, 1.00) #ImGuiCol_HeaderHovered
    style.colors[27] = (0.38, 0.62, 0.83, 1.00) #ImGuiCol_HeaderActive
    style.colors[28] = (0.50, 0.50, 0.50, 1.00) #ImGuiCol_Column
    style.colors[29] = (0.70, 0.60, 0.60, 1.00) #ImGuiCol_ColumnHovered
    style.colors[30] = (0.90, 0.70, 0.70, 1.00) #ImGuiCol_ColumnActive
    style.colors[31] = (1.00, 1.00, 1.00, 0.85) #ImGuiCol_ResizeGrip
    style.colors[32] = (1.00, 1.00, 1.00, 0.60) #ImGuiCol_ResizeGripHovered
    style.colors[33] = (1.00, 1.00, 1.00, 0.90) #ImGuiCol_ResizeGripActive
    style.colors[34] = (0.50, 0.50, 0.90, 0.50) #ImGuiCol_CloseButton
    style.colors[35] = (0.70, 0.70, 0.90, 0.60) #ImGuiCol_CloseButtonHovered
    style.colors[36] = (0.70, 0.70, 0.70, 1.00) #ImGuiCol_CloseButtonActive
    style.colors[37] = (1.00, 1.00, 1.00, 1.00) #ImGuiCol_PlotLines
    style.colors[38] = (0.90, 0.70, 0.00, 1.00) #ImGuiCol_PlotLinesHovered
    style.colors[39] = (0.90, 0.70, 0.00, 1.00) #ImGuiCol_PlotHistogram
    style.colors[40] = (1.00, 0.60, 0.00, 1.00) #ImGuiCol_PlotHistogramHovered
    style.colors[41] = (0.00, 0.00, 1.00, 0.35) #ImGuiCol_TextSelectedBg
    style.colors[42] = (0.20, 0.20, 0.20, 0.35) #ImGuiCol_ModalWindowDarkening


def SetCustomStyle2(style):
    '''
    CorporateGrey
    from https://github.com/ocornut/imgui/issues/707#issuecomment-468798935
    '''
    style.colors[0]  = (1.00, 1.00, 1.00, 1.00)
    style.colors[1]  = (0.40, 0.40, 0.40, 1.00)
    style.colors[2]  = (0.25, 0.25, 0.25, 1.00)
    style.colors[3]  = (0.25, 0.25, 0.25, 1.00)
    style.colors[4]  = (0.25, 0.25, 0.25, 1.00)
    style.colors[5]  = (0.12, 0.12, 0.12, 0.71)
    style.colors[6]  = (1.00, 1.00, 1.00, 0.06)
    style.colors[7]  = (0.42, 0.42, 0.42, 0.54)
    style.colors[8]  = (0.42, 0.42, 0.42, 0.40)
    style.colors[9]  = (0.56, 0.56, 0.56, 0.67)
    style.colors[10] = (0.19, 0.19, 0.19, 1.00)
    style.colors[11] = (0.22, 0.22, 0.22, 1.00)
    style.colors[12] = (0.17, 0.17, 0.17, 0.90)
    style.colors[13] = (0.335, 0.335, 0.335, 1.000)
    style.colors[14] = (0.24, 0.24, 0.24, 0.53)
    style.colors[15] = (0.41, 0.41, 0.41, 1.00)
    style.colors[16] = (0.52, 0.52, 0.52, 1.00)
    style.colors[17] = (0.76, 0.76, 0.76, 1.00)
    style.colors[18] = (0.65, 0.65, 0.65, 1.00)
    style.colors[19] = (0.52, 0.52, 0.52, 1.00)
    style.colors[20] = (0.64, 0.64, 0.64, 1.00)
    style.colors[21] = (0.54, 0.54, 0.54, 0.35)
    style.colors[22] = (0.52, 0.52, 0.52, 0.59)
    style.colors[23] = (0.76, 0.76, 0.76, 1.00)
    style.colors[24] = (0.38, 0.38, 0.38, 1.00)
    style.colors[25] = (0.47, 0.47, 0.47, 1.00)
    style.colors[26] = (0.76, 0.76, 0.76, 0.77)
    style.colors[27] = (0.000, 0.000, 0.000, 0.137)
    style.colors[28] = (0.700, 0.671, 0.600, 0.290)
    style.colors[29] = (0.702, 0.671, 0.600, 0.674)
    style.colors[30] = (0.26, 0.59, 0.98, 0.25)
    style.colors[31] = (0.26, 0.59, 0.98, 0.67)
    style.colors[32] = (0.26, 0.59, 0.98, 0.95)
    style.colors[33] = (0.61, 0.61, 0.61, 1.00)
    style.colors[34] = (1.00, 0.43, 0.35, 1.00)
    style.colors[35] = (0.90, 0.70, 0.00, 1.00)
    style.colors[36] = (1.00, 0.60, 0.00, 1.00)
    style.colors[37] = (0.73, 0.73, 0.73, 0.35)
    style.colors[38] = (0.80, 0.80, 0.80, 0.35)
    style.colors[39] = (1.00, 1.00, 0.00, 0.90)
    style.colors[40] = (0.26, 0.59, 0.98, 1.00)
    style.colors[41] = (1.00, 1.00, 1.00, 0.70)
    style.colors[42] = (0.80, 0.80, 0.80, 0.20)

    style.popup_rounding = 3;

    style.window_padding = (4, 4);
    style.frame_padding  = (6, 4);
    style.item_spacing   = (6, 2);

    style.scrollbar_size = 18;

    style.window_border_size = 1;
    style.child_border_size  = 1;
    style.popup_border_size  = 1;
    style.frame_border_size  = 0; 

    style.window_rounding    = 3;
    style.child_rounding     = 3;
    style.frame_rounding     = 3;
    style.scrollbar_rounding = 2;
    style.grab_rounding      = 3;


def SetCustomStyle3(style):
    '''
    light
    from https://github.com/ocornut/imgui/issues/707#issuecomment-439117182
    '''
    style.window_rounding    = 2.0             
    style.scrollbar_rounding = 3.0          
    style.grab_rounding      = 2.0          
    style.anti_aliased_lines = True
    style.anti_aliased_fill  = True
    style.window_rounding    = 2
    style.child_rounding     = 2
    style.scrollbar_size     = 16
    style.scrollbar_rounding = 3
    style.grab_rounding      = 2
    style.item_spacing     = (10,4)
    style.indent_spacing     = 22
    style.frame_padding    = (6, 4)    
    style.alpha              = 1.0
    style.frame_rounding     = 3.0

    style.colors[0] = (0.00, 0.00, 0.00, 1.00)
    style.colors[1] = (0.60, 0.60, 0.60, 1.00)
    style.colors[2] = (0.86, 0.86, 0.86, 1.00)
    style.colors[3] = (0.00, 0.00, 0.00, 0.00)
    style.colors[4] = (0.00, 0.00, 0.00, 0.00)
    style.colors[5] = (0.93, 0.93, 0.93, 0.98)
    style.colors[6] = (0.71, 0.71, 0.71, 0.08)
    style.colors[7] = (0.00, 0.00, 0.00, 0.04)
    style.colors[8] = (0.71, 0.71, 0.71, 0.55)
    style.colors[9] = (0.94, 0.94, 0.94, 0.55)
    style.colors[10] = (0.71, 0.78, 0.69, 0.98)
    style.colors[11] = (0.85, 0.85, 0.85, 1.00)
    style.colors[12] = (0.82, 0.78, 0.78, 0.51)
    style.colors[13] = (0.78, 0.78, 0.78, 1.00)
    style.colors[14] = (0.86, 0.86, 0.86, 1.00)
    style.colors[15] = (0.20, 0.25, 0.30, 0.61)
    style.colors[16] = (0.90, 0.90, 0.90, 0.30)
    style.colors[17] = (0.92, 0.92, 0.92, 0.78)
    style.colors[18] = (1.00, 1.00, 1.00, 1.00)
    style.colors[19] = (0.184, 0.407, 0.193, 1.00)
    style.colors[20] = (0.26, 0.59, 0.98, 0.78)
    style.colors[21] = (0.26, 0.59, 0.98, 1.00)
    style.colors[22] = (0.71, 0.78, 0.69, 0.40)
    style.colors[23] = (0.725, 0.805, 0.702, 1.00)
    style.colors[24] = (0.793, 0.900, 0.836, 1.00)
    style.colors[25] = (0.71, 0.78, 0.69, 0.31)
    style.colors[26] = (0.71, 0.78, 0.69, 0.80)
    style.colors[27] = (0.71, 0.78, 0.69, 1.00)
    style.colors[28] = (0.39, 0.39, 0.39, 1.00)
    style.colors[29] = (0.26, 0.59, 0.98, 0.78)
    style.colors[30] = (0.26, 0.59, 0.98, 1.00)
    style.colors[31] = (0.39, 0.39, 0.39, 1.00)
    style.colors[32] = (0.14, 0.44, 0.80, 0.78)
    style.colors[33] = (0.14, 0.44, 0.80, 1.00)
    style.colors[34] = (1.00, 1.00, 1.00, 0.00)
    style.colors[35] = (0.26, 0.59, 0.98, 0.45)
    style.colors[36] = (0.26, 0.59, 0.98, 0.78)
    style.colors[37] = (0.39, 0.39, 0.39, 1.00)
    style.colors[38] = (1.00, 0.43, 0.35, 1.00)
    style.colors[39] = (0.90, 0.70, 0.00, 1.00)
    style.colors[40] = (1.00, 0.60, 0.00, 1.00)
    style.colors[41] = (0.26, 0.59, 0.98, 0.35)
    style.colors[42] = (0.20, 0.20, 0.20, 0.35)
    #style.colors[43] = (0.26, 0.59, 0.98, 0.95)
    #style.colors[44] = (0.71, 0.78, 0.69, 0.80)
    #style.colors[45] = (0.70, 0.70, 0.70, 0.70)
