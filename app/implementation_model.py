from app import app
import os
import pandas as pd
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
import keras

from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()

from tqdm import tqdm

# loading json and creating model
from keras.models import model_from_json

from app.preproccess import pre_processing

path_chunks = "chunks"
app.config["AUDIO_UPLOAD"] = "input"
app.config["ALLOWED_AUDIO_EXTENSION"] = "WAV"


def ndlmodel():
    
    pre_processing(app.config["AUDIO_UPLOAD"])
    #file_path = os.path.join(app.config["AUDIO_UPLOAD"], file_name)
    json_file = open('app/model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("app/model/saved_models/Emotion_Voice_Detection_Model.h5")
    print("Loaded model from disk")
    
    # evaluate loaded model on test data
    loaded_model.compile(loss='categorical_crossentropy', optimizer= 'adam', metrics=['accuracy'])

    #dirlist= os.listdir('/content/drive/MyDrive/CNN_Project/Untitled folder/')
    dirlist = os.listdir(path_chunks)
    paths=[]
    for i in dirlist:
      #path = '/content/drive/MyDrive/CNN_Project/Untitled folder/' + i
      path = path_chunks + '/' +i
      paths.append(path)

    livedf= pd.DataFrame(columns=['data','feature'])
    count = 0
    for i in paths:
      livedf.loc[count,'data'] = i
      count=count+1

    count = 0
    for i in tqdm(range(len(livedf))):
        X, sample_rate = librosa.load(livedf.data[i], res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5) # path, 
        sample_rate = np.array(sample_rate)
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
        featurelive = mfccs
        livedf.loc[count,'feature'] = featurelive
        count= count + 1

    features = livedf['feature']

    livedf2= pd.DataFrame(data=features)


    feeling_list=['female_angry','female_calm','female_fearful','female_happy','female_sad','male_angry','male_calm','male_fearful','male_happy','male_sad']
    labels = pd.DataFrame(feeling_list)

    output=[]


    for i in range(len(livedf2)):
      livedf3=pd.DataFrame(data=livedf2['feature'][i])
      livedf3=livedf3.stack().to_frame().T
      print('chaning to numpy')
      twodim= np.expand_dims(livedf3, axis=2)

      livepreds = loaded_model.predict(twodim, 
                            batch_size=32, 
                            verbose=1)
      
      livepreds1=livepreds.argmax(axis=1)
      liveabc = livepreds1.astype(int).flatten()


      lb = LabelEncoder()
      lb.fit(labels)

      livepredictions = lb.inverse_transform(liveabc)
    
      output.append(livepredictions[0])

    preddf = pd.DataFrame({'predictions': output})

    preddf = preddf.pivot_table(index=['predictions'], aggfunc='size')

    values=[]
    for i in preddf:
        values.append(i)

    index = preddf.index


    #preddf = pd.DataFrame({'Values':values},index=index)


    #plot = preddf.plot.pie( y='Values',figsize=(6,6))

    preval = pd.DataFrame({'predictions':index,'Values':values})

    preval['percent'] = (preval['Values'] / preval['Values'].sum()) * 100
    precent = preval['percent'].tolist()
    prediction = preval['predictions'].tolist()
    preval = pd.DataFrame({'percent':precent },index=index)



    plot=preval.plot.pie( y='percent',figsize=(6,6))



   # dir = 'app/static/plot'
    #for f in os.listdir(dir):
     # os.remove(os.path.join(dir, f))

    #plot.figure.savefig('app/static/plot/plot.png')

    return precent, prediction , plot
