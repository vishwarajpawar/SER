from app import app
import os   

from numpy.lib.function_base import percentile
import pandas as pd
import librosa
import numpy as np
from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()
# loading json and creating model
from keras.models import model_from_json


app.config["AUDIO_UPLOAD"]="input"
app.config["ALLOWED_AUDIO_EXTENSION"]="WAV"


def dlmodel(file_name):

        file_path=os.path.join(app.config["AUDIO_UPLOAD"], file_name)
        json_file = open('app/model/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("app/model/saved_models/Emotion_Voice_Detection_Model.h5")
        print("Loaded model from disk")
        
        # evaluate loaded model on test data
        loaded_model.compile(loss='categorical_crossentropy', optimizer= 'adam', metrics=['accuracy'])

        #livedf= pd.DataFrame(columns=['feature'])
        X, sample_rate = librosa.load(file_path, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
        sample_rate = np.array(sample_rate)
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
        featurelive = mfccs
        livedf2 = featurelive

        livedf2= pd.DataFrame(data=livedf2)

        livedf2 = livedf2.stack().to_frame().T

        livedf2

        twodim= np.expand_dims(livedf2, axis=2)

        livepreds = loaded_model.predict(twodim, 
                                batch_size=32, 
                                verbose=1)

        livepreds

        livepreds1=livepreds.argmax(axis=1)

        liveabc = livepreds1.astype(int).flatten()

        feeling_list=['Female_Angry','Female_Calm','Female_Fearful','Female_Happy','Female_Sad','Male_Angry','Male_Calm','Male_Fearful','Male_Happy','Male_Sad']

        labels = pd.DataFrame(feeling_list)

        print(liveabc)

        labels

        lb = LabelEncoder()
        lb.fit(labels.values.ravel())
        livepredictions = lb.inverse_transform(liveabc)
        livepredictions[0]
        prediction=livepredictions[0].split("_")
        return prediction
    