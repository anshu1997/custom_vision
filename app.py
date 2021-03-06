from flask import Flask, render_template,url_for
#from PIL import Image
from flask import request
from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models
import os
from werkzeug.utils import secure_filename

#app = Flask(__name__,static_url_path="/static")
# Initialize the app
app = Flask(__name__)


# Now there is a trained endpoint that can be used to make a prediction
training_key = "Your Training Key"
prediction_key = "Your Prediction Key"
projectid="Your Project ID"

predictor = prediction_endpoint.PredictionEndpoint(prediction_key)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")

def main():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])

def upload_file():
	isfile=False
	results = []
	if request.method == 'POST':
		f = request.files['photo']	
        isfile=True
        target = os.path.join(APP_ROOT,'./static')
        print(target)
        filename = secure_filename(f.filename)
        destination = "/".join([target,filename])
        print(destination)
        f.save(destination)

        ff = open(destination)
        results = predictor.predict_image(projectid, ff)
        ff.close()
	return render_template('index.html',isfile=isfile,predictions=results.predictions,fname=filename)

if __name__ == "__main__":
    app.run()
