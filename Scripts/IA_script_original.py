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

from BlazeFunctions.IA import PlotarGraficos
from BlazeFunctions.IA import SepararTreinamento
from BlazeFunctions.IA import EncapsularSequencias

# np.set_printoptions(threshold=np.inf)
   
  
input_size = 5

LancesBlaze = Lances.Get(100, ReturnType='cor')

train_x, val_x, train_y, val_y = SepararTreinamento(input=LancesBlaze,input_size=input_size, return_lst=['train_x','val_x', 'train_y', 'val_y'])

train_x = np.array(EncapsularSequencias(train_x))
val_x = np.array(EncapsularSequencias(val_x))

train_y = np.array(train_y)
val_y = np.array(val_y)

model = Sequential()

model.add(BatchNormalization())
model.add(LSTM(units=64))
model.add(Dense(10,activation='tanh'))
model.add(Dense(2, activation='sigmoid'))

# predict_input = Lances.Get(input_size,ReturnType='cor')

lr = 0.009

SGD_optimizer = SGD(learning_rate=lr, momentum= 0.9)
Adagrad_optimizer = Adagrad(learning_rate=lr)

model.compile(loss='mse', optimizer=Adagrad_optimizer, metrics=['accuracy'],run_eagerly=True)

history = model.fit(train_x, train_y, epochs=20,validation_data=(val_x,val_y))




PlotarGraficos(history, '- IA')

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

quit()
# learning_rates = [5, 2, 0.5, 0.01]
# optimizers = [SGD(learning_rate=lr, momentum=0.9) for lr in learning_rates]

# for layer, optimizer in zip(model.layers, optimizers):
#     layer.optimizer = optimizer
























































































pesos_sinapticos = 2 * np.random.random((LeituraMáximaDeLances,15)) -1


bias = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

Taxa_Aprendizado = 0.1

def sigmoid(x):
  return 1/(1 + np.exp(-x))

def tanh(x):
   if x > 20:
      return 1
   elif x < -20:
      return - 1
   else:
    tangente_hip = (math.e**x - math.e**(-x)) / (math.e**x + math.e**(-x))
    if tangente_hip < 0.5 and tangente_hip > -0.5:
       return 0
    else:
       return tangente_hip

def tanh_final(x):
   if x > 20:
      return 1
   elif x < -20:
      return - 1
   else:
    tangente_hip = (math.e**x - math.e**(-x)) / (math.e**x + math.e**(-x))
    if tangente_hip > 0.5:
       return 1
    elif tangente_hip > -0.5:
      return 0
    else:
       return -1


def sigmoid_derivate(x):
  return x * (1-x)

def Calcular_Gradiente(y_real,y_previsto,Input_Layer):
   custo = np.sum(np.square(y_real - y_previsto))
   Gradiente_Pesos = custo * Input_Layer
   Gradiente_Bias = custo
   return np.array(Gradiente_Pesos), Gradiente_Bias, custo



dados_x = []
dados_y = []




for gen in range(1000):
  for indice, input_layer in enumerate():
    output = np.dot(input_layer, pesos_sinapticos)+bias
    output_somado = sigmoid(np.sum(output))


    Gradiente_Pesos, Gradiente_Bias, custo = Calcular_Gradiente(resultados_treinamento[indice],output,input_layer)

    Taxa_Aprendizado_Pesos = np.array(Taxa_Aprendizado * np.ones_like(Gradiente_Pesos))
    Taxa_Aprendizado_Pesos = Taxa_Aprendizado_Pesos.flatten().T

    # print('Gradiente_pesos: ',Gradiente_Pesos)
    # print('Taxa_Aprendizado: ',Taxa_Aprendizado_Pesos)

    pesos_sinapticos = pesos_sinapticos + Gradiente_Pesos * Taxa_Aprendizado_Pesos
    pesos_sinapticos = pesos_sinapticos
    bias += Gradiente_Bias * Taxa_Aprendizado

    os.system('cls')
    print('Layer: ',i)
    print('gen: ',gen)
    print('pesos: ',pesos_sinapticos)
    print('bias: ', bias)
    print('gradiente_pesos: ', Gradiente_Pesos)
    print('gradiente_bias: ', Gradiente_Bias)
    print('custo: ', custo)



  Acertos = 0
  custos = 0
  for i2 in range(0,i):
    input_layer = [lance[0] for lance in train_x]
    output = tanh_final(np.sum(np.dot(input_layer, pesos_sinapticos))+bias)
    if output == resultados_treinamento[i2]:
      Acertos += 1
    else:
      custos += 1

  if Acertos + custos == 0:
    Taxa_Acertos = 0
  else:
    Taxa_Acertos = round(Acertos / (Acertos + custos),3)*100


  print('Taxa de acerto: %', Taxa_Acertos)


  dados_y.append(Taxa_Acertos)
  dados_x.append(gen)

  PlotarGraficos.plotarGraficoXY(dados_x, dados_y)


# for i in range(0,len(LancesBlaze_treinamento)):
#   input_layer = LancesBlaze_treinamento[i]
#   output = tanh_final(np.sum(np.dot(input_layer, pesos_sinapticos))+bias)
#   if output == resultados_treinamento[i]:
#      Acertos += 1
#   else:
#     custos += 1

print('Taxa de acerto final: %',Taxa_Acertos)




# for i in range(0,len(output)):
#     if output[i] >0.5:
#       output[i] = 1
#       print('achou na posição: ',i)
#     else:
#       output[i] = 0


# print(LancesBlaze)
# print('------------------')
# print(LancesBlaze_treinamento)
# print('------------------')
# print(output)
# print('------------------')
# print(resultados_treinamento)
# print('------------------')
# print(pesos_sinapticos)


