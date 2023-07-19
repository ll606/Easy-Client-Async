call venv/Scripts/activate.bat
pip install nuitka
python -m nuitka launch.py --show-progress --standalone --include-plugin-directory=views --include-plugin-directory=static --enable-plugin=tk-inter --windows-disable-console
python -m nuitka --module views/task/view.py
pause