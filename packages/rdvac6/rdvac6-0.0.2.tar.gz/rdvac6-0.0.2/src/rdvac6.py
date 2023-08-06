import pandas as pd
import numpy as np
from tqdm import tqdm
from keras.preprocessing.text import Tokenizer
tqdm.pandas(desc="progress-bar")
from gensim.models import Doc2Vec
from sklearn import utils
from sklearn.model_selection import train_test_split
from keras.preprocessing import sequence
import gensim
from gensim.models.doc2vec import TaggedDocument
import re
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf

df = pd.read_csv("SPAM text message 20170820 - Data.csv",delimiter=',',encoding='latin-1')
df = df[['Category','Message']]
df = df[pd.notnull(df['Message'])]
df.rename(columns = {'Message':'Message'}, inplace = True)
df.head()

df.shape

df.index = range(5572)
df['Message'].apply(lambda x: len(x.split(' '))).sum()

cnt_pro = df['Category'].value_counts()
plt.figure(figsize=(12,4))
sns.barplot(x=cnt_pro.index,y=cnt_pro.values, alpha=0.8)
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel('Category', fontsize=12)
plt.xticks(rotation=90)
plt.show();

def print_message(index):
    example = df[df.index == index][['Message', 'Category']].values[0]
    if len(example) > 0:
        print(example[0])
        print('Message:', example[1])
print_message(12)

print_message(0)

print_message(5000)

"""Preprocessing of Text The function to lowercase text, remove punctuation and symbols from words, and more is defined below.

"""

from bs4 import BeautifulSoup
def cleanText(text):
    text = BeautifulSoup(text, "lxml").text
    text = re.sub(r'\|\|\|', r' ', text) 
    text = re.sub(r'http\S+', r'<URL>', text)
    text = text.lower()
    text = text.replace('x', '')
    return text
df['Message'] = df['Message'].apply(cleanText)

import nltk
nltk.download('punkt')

from keras.utils import pad_sequences

df['Message'] = df['Message'].apply(cleanText)
train,test = train_test_split(df, test_size=0.000001, random_state=42)
import nltk
from nltk.corpus import stopwords
def tokenize_text(text):
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            #if len(word) < 0:
            if len(word) <= 0:
                continue
            tokens.append(word.lower())
    return tokens
train_tagged = train.apply(
    lambda r: TaggedDocument(words=tokenize_text(r['Message']), tags=[r.Category]), axis=1)
test_tagged = test.apply(
    lambda r: TaggedDocument(words=tokenize_text(r['Message']), tags=[r.Category]), axis=1)

# The maximum number of words to be used. (most frequent)
max_fatures = 500000

# Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 50

#tokenizer = Tokenizer(num_words=max_fatures, split=' ')
tokenizer = Tokenizer(num_words=max_fatures, split=' ', filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
tokenizer.fit_on_texts(df['Message'].values)
X = tokenizer.texts_to_sequences(df['Message'].values)
X = pad_sequences(X)
print('Found %s unique tokens.' % len(X))

X = tokenizer.texts_to_sequences(df['Message'].values)
X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)
print('Shape of data tensor:', X.shape)

train_tagged.values

d2v_model = Doc2Vec(dm=1, dm_mean=1, vector_size=20, window=8, min_count=1, workers=1, alpha=0.065, min_alpha=0.065)
d2v_model.build_vocab([x for x in tqdm(train_tagged.values)])

# Commented out IPython magic to ensure Python compatibility.
# %%time
# for epoch in range(30):
#     d2v_model.train(utils.shuffle([x for x in tqdm(train_tagged.values)]), total_examples=len(train_tagged.values), epochs=1)
#     d2v_model.alpha -= 0.002
#     d2v_model.min_alpha = d2v_model.alpha

print(d2v_model)

len(d2v_model.wv.key_to_index)

embedding_matrix = np.zeros((len(d2v_model.wv.key_to_index)+ 1, 20))

for i, vec in enumerate(d2v_model.dv.vectors):
    while i in vec <= 1000:
    #print(i)
    #print(model.docvecs)
          embedding_matrix[i]=vec
    #print(vec)
    #print(vec[i])

"""Measuring distance between two vectors (related to cosine similarity)"""

d2v_model.wv.most_similar(positive=['urgent'], topn=10)

d2v_model.wv.most_similar(positive=['cherish'], topn=10)

"""Create the LSTM Model"""

from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding
model = Sequential()
model.add(Embedding(len(d2v_model.wv.key_to_index)+1,20,input_length=X.shape[1],weights=[embedding_matrix],trainable=True))
def split_input(sequence):
     return sequence[:-1], tf.reshape(sequence[1:], (-1,1))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(2,activation="softmax"))
model.summary()
model.compile(optimizer="adam",loss="binary_crossentropy",metrics=['acc'])

from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding,Dropout,Activation
model1 = Sequential()
model1.add(Embedding(len(d2v_model.wv.key_to_index)+1,20,input_length=X.shape[1],weights=[embedding_matrix],trainable=True))
def split_input(sequence):
     return sequence[:-1],tf.reshape(sequence[1:], (-1,1))
model1.add(LSTM(50,return_sequences=False))
model1.add(Dense(2,activation="softmax"))
model1.add(Activation('relu'))
model1.add(Dense(256,name='FC1'))
model1.add(Dropout(0.5))
model1.summary()
model1.compile(optimizer="adam",loss="binary_crossentropy",metrics=['acc'])

from keras.utils import plot_model
plot_model(model, to_file='model.png')

from keras.utils import plot_model
plot_model(model1, to_file='model1.png')

Y = pd.get_dummies(df['Category']).values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.15, random_state = 42)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

import logging
logging.getLogger('tensorflow').disabled = True

batch_size = 32
history=model.fit(X_train, Y_train, epochs =10, batch_size=batch_size, verbose = 2)

plt.plot(history.history['acc'])
plt.title('model accuracy')
plt.ylabel('acc')
plt.xlabel('epochs')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
plt.savefig('model_accuracy.png')
# summarize history for loss
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
plt.savefig('model_loss.png')

# evaluate the model
train_loss, train_acc = model.evaluate(X_train, Y_train, verbose=2)
test_loss, test_acc = model.evaluate(X_test, Y_test, verbose=2)
print('Train accuracy:', train_acc)
print('Test accuracy:', test_acc)

from keras.utils import to_categorical
# predict probabilities for test set
yhat_probs = model.predict(X_test, verbose=0)
yhat_classes = np.argmax(yhat_probs, axis=1)
print(yhat_probs)
# predict crisp classes for test set
yhat_classes = model.predict(X_test, verbose=2)
print(yhat_classes)
# reduce to 1d array
yhat_probs = yhat_probs[:, 0]

rounded_labels=np.argmax(Y_test, axis=1)
rounded_labels

yhat_classes.mean(axis=1)

yhat_classes=np.argmax(Y_test,axis = 1)
yhat_classes
print(rounded_labels.shape)
print(yhat_classes.shape)

from sklearn.metrics import confusion_matrix,classification_report
cm = confusion_matrix(rounded_labels, yhat_classes)
print(cm)
print(classification_report(rounded_labels, yhat_classes))

import seaborn as sns
lstm_val = confusion_matrix(rounded_labels, yhat_classes)
f, ax = plt.subplots(figsize=(5,5))
sns.heatmap(lstm_val, annot=True, linewidth=0.7, linecolor='pink', fmt='g', ax=ax, cmap="summer")
plt.title('LSTM Classification Confusion Matrix')
plt.xlabel('Y predict')
plt.ylabel('Y test')
plt.show()

validation_size = 200

X_validate = X_test[-validation_size:]
Y_validate = Y_test[-validation_size:]
X_test = X_test[:-validation_size]
Y_test = Y_test[:-validation_size]
score,acc = model.evaluate(X_test, Y_test, verbose = 1, batch_size = batch_size)

print("score: %.2f" % (score))
print("acc: %.2f" % (acc))

model.save('Mymodel.h5')

message = ['Congratulations! you have won a $1,000 Walmart gift card. Go to http://bit.ly/123456 to claim now.']
print(message)
seq = tokenizer.texts_to_sequences(message)

padded = pad_sequences(seq, maxlen=X.shape[1], dtype='int32', value=0)

pred = model.predict(padded)

labels = ['ham','spam']
print(pred, labels[np.argmax(pred)])

message = ["This is a good Message"]
seq = tokenizer.texts_to_sequences(message)
padded = pad_sequences(seq, maxlen=X.shape[1], dtype='int32', value=0)
pred = model.predict(padded)
labels = ['ham','spam']
print(pred, labels[np.argmax(pred)])

message = ['Ravi is good fellow']
seq = tokenizer.texts_to_sequences(message)
padded = pad_sequences(seq, maxlen=X.shape[1], dtype='int32', value=0)
pred = model.predict(padded)
labels = ['ham','spam']
if np.argmax(pred) < len(labels):
    print(pred, labels[np.argmax(pred)])
else:
    print("Invalid index:", np.argmax(pred))

message = ['As technology continues to advance at a rapid pace, Go to http://bit.ly/123456 to claim now. our world is becoming more interconnected and convenient than ever before. The internet and smartphones have revolutionized the way we communicate, access information, and conduct business. Social media platforms allow us to connect with people from all over the world and share our experiences in real-time. E-commerce websites have made it possible to shop for almost anything from the comfort of our homes']
seq = tokenizer.texts_to_sequences(message)
padded = pad_sequences(seq, maxlen=X.shape[1], dtype='int32', value=0)
pred = model.predict(padded)
labels = ['ham','spam']
if np.argmax(pred) < len(labels):
    print(pred, labels[np.argmax(pred)])
else:
    print("Invalid index:", np.argmax(pred))

message = []
sentence = input("Enter the Sentences:")
words = sentence.split()
message.append(words)
seq = tokenizer.texts_to_sequences(message)
padded = pad_sequences(seq, maxlen=X.shape[1], dtype='int32', value=0)
pred = model.predict(padded)
labels = ['ham','spam']
if np.argmax(pred) < len(labels):
    print(pred, labels[np.argmax(pred)])
else:
    print("Invalid index:", np.argmax(pred))