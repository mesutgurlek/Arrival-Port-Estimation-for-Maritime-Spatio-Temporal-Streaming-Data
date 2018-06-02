import pandas as pd
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.recurrent import LSTM, GRU
from keras.layers import Convolution1D, MaxPooling1D, AtrousConvolution1D, RepeatVector
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, CSVLogger
from keras.layers.wrappers import Bidirectional
from keras import regularizers
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import *
from keras.optimizers import RMSprop, Adam, SGD, Nadam
from keras.initializers import *

import seaborn as sns
sns.despine()

get_ipython().magic(u'matplotlib inline')
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')

import transaction_reader as t_r

file = ('../Dataset/preprocess_outputs/port_calc_processed.csv')

WINDOW = 50
EMB_SIZE = 5
STEP = 20
FORECAST = 1
train_percentage = 0.8
val_percentage = 0.1

reader = t_r.Transaction_Reader(file)

X_train, X_test, X_val, Y_val, Y_train, Y_test = [], [], [], []
x_train_count = int(reader.total_transactions * train_percentage)
x_val_count = int(reader.total_transactions * train_percentage)
for j in range(reader.total_transactions):
    data, labels = reader.next_batch()
    for i in range(0, reader.trans_freqs[reader.current_batch], STEP):
        try:
            x_i = data[i:i+WINDOW]
            y_i = labels[i+WINDOW]
        except Exception as e:
            break
        if reader.current_batch <= x_train_count:
            X_train.append(x_i)
            Y_train.append(y_i)
        elif reader.current_batch > x_train_count and current_batch <= x_train_count + x_val_count:
            X_val.append(x_i)
            Y_val.append(y_i)
        else:
            X_test.append(x_i)
            Y_test.append(y_i)
    
X_train, X_val, X_test, Y_train, Y_val, Y_test = np.array(X_train), np.array(X_val), np.array(X_test), np.array(Y_train), np.array(Y_val), np.array(Y_test)
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], EMB_SIZE))
X_val = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], EMB_SIZE))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], EMB_SIZE))

no_class = Y_train.shape[1]

model = Sequential()
model.add(Convolution1D(input_shape = (WINDOW, EMB_SIZE),
                        nb_filter=16,
                        filter_length=4,
                        border_mode='same'))
model.add(BatchNormalization())
model.add(LeakyReLU())
model.add(Dropout(0.5))

model.add(Convolution1D(nb_filter=8,
                        filter_length=4,
                        border_mode='same'))
model.add(BatchNormalization())
model.add(LeakyReLU())
model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(64))
model.add(BatchNormalization())
model.add(LeakyReLU())


model.add(Dense(no_class))
model.add(Activation('softmax'))

opt = Nadam(lr=0.002)

reduce_lr = ReduceLROnPlateau(monitor='val_acc', factor=0.9, patience=30, min_lr=0.000001, verbose=1)
checkpointer = ModelCheckpoint(filepath="multivariate.hdf5", verbose=1, save_best_only=True)


model.compile(optimizer=opt, 
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, Y_train, 
          nb_epoch = 100, 
          batch_size = 128, 
          verbose=1, 
          validation_data=(X_val, Y_val),
          callbacks=[reduce_lr, checkpointer],
          shuffle=True)

model.load_weights("multivariate.hdf5")
pred = model.predict(np.array(X_test))

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
C = confusion_matrix([np.argmax(y) for y in Y_test], [np.argmax(y) for y in pred])

plt.figure()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='best')
plt.show()

plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='best')
plt.show()

