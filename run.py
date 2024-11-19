from app import app
import os

UPLOAD_FOLDER = 'static/uploads'
CLOTHES_FOLDER = '/clothes'
LAUNDERER_FOLDER = '/launderers'
BILL_FOLDER = '/bills'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER + CLOTHES_FOLDER, exist_ok=True)
app.config['CLOTHES_FOLDER'] = UPLOAD_FOLDER + CLOTHES_FOLDER

os.makedirs(UPLOAD_FOLDER + LAUNDERER_FOLDER, exist_ok=True)
app.config['LAUNDERER_FOLDER'] = UPLOAD_FOLDER + LAUNDERER_FOLDER

os.makedirs(UPLOAD_FOLDER + BILL_FOLDER, exist_ok=True)
app.config['BILL_FOLDER'] = UPLOAD_FOLDER + BILL_FOLDER

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)    