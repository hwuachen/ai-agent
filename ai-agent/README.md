# Create environment
python.exe -m venv env
.\env\Scripts\activate
pip install -r requirements.txt

# debug live mode
flask --app app.py --debug
