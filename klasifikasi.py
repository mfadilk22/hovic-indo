import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import spacy
from spacy.util import minibatch, compounding
from spacy import load, displacy
from spacy.training.example import Example
import pickle

model_path = 'model/'
# load model
model = tf.keras.models.load_model(model_path+"model_NN.h5")
model_ner = spacy.load(model_path+"NER_3")
token = Tokenizer()
with open(model_path+'token_NN.pickle', 'rb') as handle:
    token = pickle.load(handle)

colors= {'ORGANISASI':'#54dda4', "ORANG":'#54dda4', "LOKASI":'#54dda4', "PENYAKIT":'#54dda4', "VAKSIN":'#54dda4'}
options = {'ents': ['ORGANISASI',"ORANG","LOKASI","PENYAKIT","VAKSIN"], 'colors':colors}

def klasifikasi_kata(sentences):
    hasil_dict = dict()
    hasil_dict['doc'] = []

    teks = [sentences]
    sequences = token.texts_to_sequences(teks)
    padded = pad_sequences(sequences, maxlen=22, padding="post", truncating="post")
    res = model.predict(padded)
    res_rounded_value = round((res[0][0]*100),2)
    res_string = res_rounded_value
    hasil_dict["klasifikasi"] = res_string

    doc = model_ner(sentences)
    hasil_doc = displacy.render(doc, style="ent", options=options)
    # hasil_doc = Markup(hasil_doc)
    # hasil_doc = hasil_doc.replace("\n\n","\n")
    for ent in doc.ents:        
        hasil_dict['doc'].append([ent.text, ent.label_])    
        
    hasil_dict['ner'] = hasil_doc

    return hasil_dict