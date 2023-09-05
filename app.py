from flask import Flask, request, render_template
from flask import Response
from datetime import datetime
import pandas
import pickle
import json
import requests

headers = {"Authorization": "Bearer ya29.a0ARrdaM_YkI6oUm949UJteFylUpoLGG114jpBLlEiTSJZkfPSqwPaUcWmJKHRN9aPNBpOZoXdbCjC5BRezFaooZSVvfFqMyKkbmb_ZuuxrzkARnNJh06-Dm-xvq4FVlpmnoBm1IF2n4seBnhRjV79Si4XmNS7"}

model_path = 'saved_models/model.pkl'
model = pickle.load(open(model_path, 'rb'))

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predictRouteClient():

        if request.form is not None:
            path = request.form['filepath']
            data = pandas.read_csv(path)
            y_pred = model.predict(data)
            data['isFraud'] = y_pred
            output_path = "predictions/"+ "Output_"+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + ".csv"
            data.to_csv(output_path, index=False)
            file_name = "Output_"+ datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + ".csv"
            para = {
                    "name": file_name,
                    "parents":["1UGQyeMhA8YR0UFT5suftSckVvfXcBd-d"]

                    }
            files = {
                    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                    'file': open("./"+ output_path, "rb")
                    }
            r = requests.post(
                     "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                    headers=headers,
                     files=files
                    )
            print(r.text)
    
            return file_name
        else:
            print('Nothing Matched')
    

if __name__ == "__main__":
    app.run()




'''
from flask import Flask, request, render_template
import pandas as pd
import pickle
import json
import requests
from datetime import datetime

# Define constants
HEADERS = {"Authorization": "Bearer ya29.a0ARrdaM_YkI6oUm949UJteFylUpoLGG114jpBLlEiTSJZkfPSqwPaUcWmJKHRN9aPNBpOZoXdbCjC5BRezFaooZSVvfFqMyKkbmb_ZuuxrzkARnNJh06-Dm-xvq4FVlpmnoBm1IF2n4seBnhRjV79Si4XmNS7"}
MODEL_PATH = 'saved_models/model.pkl'

# Load the machine learning model
model = pickle.load(open(MODEL_PATH, 'rb'))

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict_route_client():
    if request.form and 'filepath' in request.form:
        path = request.form['filepath']
        data = pd.read_csv(path)
        y_pred = model.predict(data)
        data['isFraud'] = y_pred
        
        # Define the output path for the CSV file
        output_path = "predictions/Output_" + datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + ".csv"
        
        # Save the data to the output path
        data.to_csv(output_path, index=False)
        
        # Define file name for Google Drive upload
        file_name = "Output_" + datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + ".csv"
        
        # Define parameters for Google Drive upload
        para = {
            "name": file_name,
            "parents": ["1UGQyeMhA8YR0UFT5suftSckVvfXcBd-d"]
        }
        
        # Prepare files for upload
        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': open("./" + output_path, "rb")
        }
        
        # Make a POST request to upload the file to Google Drive
        response = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=HEADERS,
            files=files
        )
        
        # Print the response text for debugging purposes
        print(response.text)
    
        return file_name
    else:
        print('Nothing Matched')

if __name__ == "__main__":
    app.run()
'''
