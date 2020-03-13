call C:\Users\admin\Anaconda3\condabin\conda_hook.bat
call conda create --name PdfGUI python=3.7
call conda activate PdfGUI
call conda install -c conda-forge poppler
pip install -r requirements.txt
exit