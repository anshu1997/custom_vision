from flask import Flask, render_template
from PIL import Image
from flask import request
from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models
from werkzeug.utils import secure_filename

#app = Flask(__name__,static_url_path="/static")
# Initialize the app
app = Flask(__name__)


# Now there is a trained endpoint that can be used to make a prediction
training_key = "3df4462657d8403090db9cb591a7e285"
prediction_key = "3cb74b07eb924c75b11888bc64c776e4"
projectid="7fa336ce-fb4d-49b0-a44a-46fce8c90483"

predictor = prediction_endpoint.PredictionEndpoint(prediction_key)

@app.route("/")

def main():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])

def upload_file():
	isfile=False
	results = []
	if request.method == 'POST':
		f = request.files['photo']
		results = predictor.predict_image(projectid, f)
		sfname = 'static/img/'+str(secure_filename(f.filename))
        f.save(sfname)
        isfile=True    
	return render_template('index.html',isfile=isfile,predictions=results.predictions,fname=f.filename,imgadr=sfname)

if __name__ == "__main__":
    app.run()