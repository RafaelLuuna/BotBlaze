#--------------------------------[CARREGAR LANCES]--------------------------------#
import numpy as np
import requests
import math
import os
import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, LeakyReLU, LSTM, BatchNormalization
from keras.optimizers import Adagrad, SGD

import matplotlib.pyplot as plt

import BlazeFunctions.Lances as Lances

from BlazeFunctions.IA_Functions import PlotarGraficos
from BlazeFunctions.IA_Functions import SepararTreinamento
from BlazeFunctions.IA_Functions import EncapsularSequencias
from BlazeFunctions.IA_Functions import AgruparSequancias

# DESATIVA FILTRO QUANDO VAI DAR PRINT EM UMA ARRAY
# np.set_printoptions(threshold=np.inf)
   
  
input_size = 6

LancesBlaze = Lances.Get(600, ReturnType='cor')

train_x, val_x, train_y, val_y = SepararTreinamento(input=LancesBlaze,input_size=input_size, return_lst=['train_x','val_x', 'train_y', 'val_y'])

# -------------TREINAMENTO DO MODELO LSTM
# group_size = 20
# train_x, train_y = AgruparSequancias(train_x, train_y, group_size)
# val_x, val_y = AgruparSequancias(val_x, val_y, group_size)

# train_x = np.array(EncapsularSequencias(train_x))
# val_x = np.array(EncapsularSequencias(val_x))

train_x = np.array(train_x)
val_x = np.array(val_x)
train_y = np.array(train_y)
val_y = np.array(val_y)


model = Sequential()

#-------------MODELO LSTM
# model.add(BatchNormalization())
# model.add(LSTM(units=64))
# model.add(BatchNormalization())
# model.add(Dense(10,activation='tanh'))
# model.add(BatchNormalization())

#-------------MODELO SEQUENCIAL
model.add(BatchNormalization())
model.add(Dense(input_size, activation='tanh'))
model.add(BatchNormalization())
model.add(Dense(5, activation='tanh'))
model.add(BatchNormalization())
model.add(Dense(5, activation='tanh'))
model.add(BatchNormalization())



#-------------OUTPUT
model.add(Dense(2, activation='sigmoid'))

# predict_input = Lances.Get(input_size,ReturnType='cor')

lr = 0.05

SGD_optimizer = SGD(learning_rate=lr, momentum= 0.7)
Adagrad_optimizer = Adagrad(learning_rate=lr)

model.compile(loss='mse', optimizer=SGD_optimizer, metrics=['accuracy'],run_eagerly=True)

history = model.fit(train_x, train_y, epochs=60,validation_data=(val_x,val_y))




PlotarGraficos(history, '- 20 lances')

def ComandosFinais():
  InserirComando = True

  
  while InserirComando == True:

    User_input = input('Modelo treinado com sucesso, digite "s" para salvar, "c" para cancelar ou "t" para testar o modelo: ')

    match User_input:
      case 's':
        ModelPath = input('Digite o nome e extensao do arquivo: ')
        model.save(ModelPath)
        print('Modelo salvo com sucesso!')
        InserirComando = False
      case 'c':
        quit()
      case 't':
        input_layer = Lances.Get(30)
        input_layer_1 = np.array(input_layer[0:5]).reshape(1,5)
        input_layer_2 = np.array(input_layer[5:10]).reshape(1,5)
        input_layer_3 = np.array(input_layer[10:15]).reshape(1,5)
        input_layer_4 = np.array(input_layer[15:20]).reshape(1,5)
        input_layer_5 = np.array(input_layer[20:25]).reshape(1,5)
        input_layer_6 = np.array(input_layer[25:]).reshape(1,5)
        input_layer = [input_layer_1,input_layer_2,input_layer_3,input_layer_4,input_layer_5,input_layer_6]
        input_layer = [np.array(input) for input in input_layer]

        print('Inout: ',input_layer)
        print('Palpite IA: ',np.argmax(model.predict(input_layer)))

ComandosFinais()
