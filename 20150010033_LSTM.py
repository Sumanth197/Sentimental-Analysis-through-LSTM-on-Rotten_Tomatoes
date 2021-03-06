# -*- coding: utf-8 -*-
"""Q3_LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v3KlaKX8-UoAS3boR1NctAL-s5tY4vAF
"""

from google.colab import drive
drive.mount('/content/gdrive')

import numpy as np
import pandas as pd
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

file_path = 'gdrive/My Drive/mrdata.tsv'

df = pd.read_csv(file_path, delimiter='\t')

df.head()

X = df['Phrase']
Y = df['Sentiment']

Y = np.asarray(Y)
Y

no_classes = df['Sentiment'].nunique()
no_classes,Y

from keras.preprocessing.text import Tokenizer
max_features = 30000
tokenizer = Tokenizer(num_words= max_features)
tokenizer.fit_on_texts(list(X))
X = tokenizer.texts_to_sequences(X)

from keras.preprocessing import sequence
max_words = 30
X = sequence.pad_sequences(X, maxlen=max_words)

X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2, random_state= 42)
y_test1 = y_test
y_test1, y_test

from keras.models import Sequential
from keras.layers import Dense,Embedding,LSTM
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

batch_size=256
epochs=10
embed_dim = 100

model= Sequential()
model.add(Embedding(max_features,embed_dim,input_length=X_train.shape[1]))
model.add(LSTM(100, dropout_U=0.2,dropout_W=0.2, return_sequences=True))
model.add(LSTM(100, dropout_U=0.2,dropout_W=0.2, return_sequences=False))
model.add(Dense(no_classes,activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

y_train = to_categorical(y_train, no_classes) 

X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2, random_state= 42)

model.fit(X_train, y_train, validation_data=(X_valid, y_valid), epochs=epochs, batch_size=batch_size, verbose=2)

y_pred_test =  model.predict_classes(X_test, batch_size=batch_size, verbose=1)

#print('Accuracy :', accuracy_score(np.argmax(y_test,axis=1),y_pred_test)*100)

y_test = to_categorical(y_test, no_classes)
score, acc = model.evaluate(X_test, y_test)
print('Accuracy', acc)

y_true = np.asarray(y_test1).flatten()
scores = confusion_matrix(y_true, y_pred_test)
print(scores)