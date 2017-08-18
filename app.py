
from flask import Flask,render_template, request, redirect, url_for, send_from_directory, send_file
from werkzeug import secure_filename
import sys
import os
import subprocess
import time
import glob
from imagemaker import make_image
import uuid
import urllib.parse
from flask_mail import Mail, Message

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'images/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'JPG', 'PNG', 'JPEG', 'jpeg'])

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ['RECIPIENT_EMAIL']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASS']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/images/wallpapers/<filename>')
def render_image(filename):
    return send_file('images/wallpapers/' + filename)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wallpaper', methods=['GET', 'POST'])
def wallpaper():
    if request.method == 'GET':
        return render_template('image.html')
    else:
        return render_template('image.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'GET':
        return render_template('upload.html')
    else:
        try:
            for upload in request.files.getlist('file'):
                if upload and allowed_file(upload.filename.lower()):
                    upload_img = secure_filename(upload.filename)
                    upload.save(os.path.join(app.config['UPLOAD_FOLDER'], upload_img))
                    result_img = make_image(upload_img)
                    try:
                        email_photo(result_img, 'images/wallpapers/' + result_img)
                    except:
                        print("ERROR: email_photo function failed.")
            return send_from_directory('images/wallpapers', result_img, as_attachment=True)
        except:
            return render_template('upload.html')

#gets the image the user will want to download
@app.route('/images/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    try:
        return send_from_directory('images/wallpapers', filename, as_attachment=True)
    except:
        return send_from_directory('images/', 'IMG_2174.jpg', as_attachment=True)

"""@app.route("/wakemydyno.txt")
def keep_app_awake():
    return send_file(
        "static/wakemydyno.txt"), 200"""

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#for a future project
def email_photo(image, image_path):
    msg = Message(image,
                  sender= os.environ['RECIPIENT_EMAIL'],
                  recipients=[os.environ['RECIPIENT_EMAIL']]
                  )
    with app.open_resource(image_path) as fp:
        msg.attach(image, "image/png", fp.read())
    a = mail.send(msg)
    return a

if __name__ == '__main__':
    app.run()
