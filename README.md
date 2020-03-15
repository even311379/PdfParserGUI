# PdfParser With PyImgui

Windows 10 Build Success branch

(1) Need to mannaul fix some source code for pyinstaller

Add this in envs\PdfGUI\Lib\site-packages\PyInstaller\utils\misc.py L128
As this post suggest
https://github.com/pyinstaller/pyinstaller/issues/4034
```code
if fnm in ('-', None):
    continue
```

(2) use cmd to run the build results to prevent debug message disappeared

(3) then just keeps google and add some hidden imports back, and everything should be fine!

(4) Can not run multiprocess!! It just make so many GUI window pops up, so I end up turn off multiprocess for now!

Download the builds here:

https://drive.google.com/open?id=1-NkQtVqe8gvVSKaCasAwswsj7edc6f-p