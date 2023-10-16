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

LancesBlaze = Lances.Get(300, ReturnType='cor')

train_x, val_x, train_y, val_y = SepararTreinamento(input=LancesBlaze, input_size=input_size, return_lst=['train_x','val_x', 'train_y', 'val_y'])

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
model.add(Dense(5, activation='relu'))
model.add(BatchNormalization())



#-------------OUTPUT
model.add(Dense(2, activation='sigmoid'))


lr = 0.05

SGD_optimizer = SGD(learning_rate=lr, momentum= 0.7)
Adagrad_optimizer = Adagrad(learning_rate=lr)

model.compile(loss='mse', optimizer=SGD_optimizer, metrics=['accuracy'],run_eagerly=True)

history = model.fit(train_x, train_y, epochs=60,validation_data=(val_x,val_y))




PlotarGraficos(history, '')

def ComandosFinais():
  InserirComando = True

  
  while InserirComando == True:

    User_input = input('Modelo treinado com sucesso, digite "s" para salvar ou "c" para cancelar: ')

    match User_input:
      case 's':
        ModelPath = input('Digite o nome e extensao do arquivo: ')
        model.save(ModelPath)
        print('Modelo salvo com sucesso!')
        InserirComando = False
      case 'c':
        quit()

ComandosFinais()
