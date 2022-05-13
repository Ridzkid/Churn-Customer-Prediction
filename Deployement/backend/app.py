from os import access
from flask import Flask, jsonify, request
import pickle
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np

app = Flask(__name__)

with open("preprocesing.pkl", "rb") as f:
    prepocess = pickle.load(f)
model = load_model('modell.h5')


columns = ['tenure',  'OnlineSecurity', 'Contract', 'MonthlyCharges', 'TotalCharges']
classes = ['Yes', 'No']

@app.route("/")
def home():
    return "<h1>Welcome To My World!</h1>"

@app.route("/predict", methods=['GET','POST'])
def model_prediction():
    if request.method == "POST":
        content = request.json
        try:
            data= [content['tenure'],
                   content['OnlineSecurity'],
                   content['Contract'],
                   content['MonthlyCharges'],
                   content['TotalCharges']]
                   
            data = pd.DataFrame([data], columns=columns)
            prepo= prepocess.transform(data)
            res = model.predict(prepo)
            res = np.where(res > 0.5, 1, 0)
            response = {"code": 200, "status":"OK", 
                        "result":{"prediction":str(res[0].item()),
                                   "description":classes[res[0].item()]}}
            return jsonify(response)
        except Exception as e:
            response = {"code":500, "status":"ERROR", 
                        "result":{"error_msg":str(e)}}
            return jsonify(response)
    return "<p>Silahkan gunakan method POST untuk mengakses hasil prediksi dari model</p>"