
from flask import Flask,render_template, request, redirect, url_for, send_from_directory, send_file
from werkzeug import secure_filename
import sys
import os
import subprocess 
import time
import glob
from imagemaker import make_image
#from flask_dropzone import Dropzone 

app = Flask(__name__, static_url_path='/static')
#dropzone = Dropzone(app)
app.config['UPLOAD_FOLDER'] = 'images/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'JPG', 'PNG', 'JPEG', 'jpeg'])
#app.config['DEBUG'] = True

"""app.config.update(
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=1,
    DROPZONE_INPUT_NAME='photo',
    DROPZONE_MAX_FILES=1
)"""


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
		#print("post request made")
		try:
			for upload in request.files.getlist('file'):
				if upload and allowed_file(upload.filename.lower()):
					upload_img = secure_filename(upload.filename)
					upload.save(os.path.join(app.config['UPLOAD_FOLDER'], upload_img))
					result_img = make_image(upload_img)
					root_path = os.path.sep.join(app.instance_path.split(os.path.sep))
					return send_from_directory('images/wallpapers', result_img, as_attachment=True)
					print(result_img)
					return uploaded_file(result_img)
			return uploaded_file(result_img)
		except:
			return render_template('upload.html')
	#return redirect(url_for('wallpaper'))
			
#gets the image the user will want to download
@app.route('/images/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
	print("here in uploaded_file")
	#subprocess.call(["./imagemaker/imagetest.py", "images/" + filename])
	try:
		return send_from_directory('images/wallpapers', filename, as_attachment=True)
	except:
		return send_from_directory('images/', 'IMG_2174.jpg', as_attachment=True)
	#return render_template('imagePage.html', filename = "/images/wallpapers/" + filename[1:] )

@app.route("/wakemydyno.txt")
def keep_app_awake():
    return send_file(
        "static/wakemydyno.txt"), 200

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
