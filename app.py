from flask import Flask,flash, redirect, url_for, render_template, request, send_from_directory
import os
from markupsafe import Markup
from werkzeug.utils import secure_filename
import spacy
from spacy.util import minibatch, compounding
from spacy import load, displacy
from spacy.training.example import Example
from pathlib import Path

import pickle
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask_wtf import FlaskForm
from wtforms import FileField
from flaskext.markdown import Markdown

from klasifikasi import klasifikasi_kata

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config["DEBUG"] = True
app.config['ALLOWED_EXTENSIONS'] = ['txt']
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

model_path = 'model/'

# load model
model = tf.keras.models.load_model(model_path+"model_NN.h5")
model_ner = spacy.load(model_path+"NER_3")
token = Tokenizer()
with open(model_path+'token_NN.pickle', 'rb') as handle:
    token = pickle.load(handle)

@app.route("/")
def index():
	return render_template(('index.html'), prediksi_teks = False)

@app.route("/klasifikasi", methods=['GET', 'POST'])
def klasifikasi_teks():
	if request.method == "POST":
		message = request.form['teks_vaksin']
		hasil_pred = klasifikasi_kata(message)

	return render_template(('index.html'), prediksi_teks = hasil_pred['klasifikasi'], ner = hasil_pred['doc'], pesan = message)    


if __name__ == '__main__':
	app.run(debug=True)