echo this project is building... please wait...

if not exist venv (
	python -m venv venv
)

call venv/Scripts/activate.bat

echo this project is building... please wait...

pip install -r requirements.txt

echo this project has been set up successfully.

pause