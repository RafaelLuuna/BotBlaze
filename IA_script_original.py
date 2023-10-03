#--------------------------------[CARREGAR LANCES]--------------------------------#
import numpy as np
import requests
import math
import os
import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, LeakyReLU, LSTM, BatchNormalization
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adagrad, SGD
from keras.callbacks import Callback
import keras.backend as K

import copy

import matplotlib.pyplot as plt


np.set_printoptions(threshold=np.inf)

def PlotarGraficos(history, modelName):
  losses = history.history['loss']
  val_losses = history.history['val_loss']
  accuracies = history.history['accuracy']
  val_accuracies = history.history['val_accuracy']

  # Plotando as perdas
  plt.figure(figsize=(12, 6))
  plt.subplot(1, 2, 1)
  plt.plot(history.epoch, losses, label='Loss', color='blue', marker='o')
  plt.plot(history.epoch, val_losses, label='Val_Loss', color='green', marker='o')
  plt.title('Loss Over Time '+ modelName)
  plt.xlabel('Epoch')
  plt.ylabel('Loss')
  plt.legend()

  # Plotando as métricas de precisão
  plt.subplot(1, 2, 2)
  plt.plot(history.epoch, accuracies, label='Accuracy', color='blue', marker='o')
  plt.plot(history.epoch, val_accuracies, label='Val_Accuracie', color='green', marker='o')
  plt.title('Accuracy Over Time '+ modelName)
  plt.xlabel('Epoch')
  plt.ylabel('Accuracy')
  plt.legend()

  plt.tight_layout()
  plt.show()

def CarregarLances(NumLances, ReturnType='cor'):
    UltimosLances = []
    if NumLances < 300:
      result_json = (requests.get("https://blaze-1.com/api/roulette_games/history")).json()
      resultados = reversed(result_json['records'])
      for resultado in resultados:
          match ReturnType:
              case 'cor':
                  match resultado['color']:
                      case 'white':
                          UltimosLances.append(0)
                      case 'red':
                          UltimosLances.append(1)
                      case 'black':
                          UltimosLances.append(2)
              case 'numero':
                  UltimosLances.append(resultado['roll'])

    else:
      total_pages = int(NumLances / 300) + 1
      for page in reversed(range(1, total_pages+1)):
          result_json = (requests.get("https://blaze-1.com/api/roulette_games/history?page=" + str(page))).json()
          resultados = reversed(result_json['records'])
          print('page :',page)
          for resultado in resultados:
            Cor = 0
            match ReturnType:
              case 'cor':
                  match resultado['color']:
                      case 'white':
                          UltimosLances.append(0)
                      case 'red':
                          UltimosLances.append(1)
                      case 'black':
                          UltimosLances.append(2)
              case 'numero':
                  UltimosLances.append(resultado['roll'])
    UltimosLances = UltimosLances[len(UltimosLances)-NumLances:]
    return UltimosLances

def SepararTreinamento(input, input_dim, input_type='cor', input_val_rate=0.2, return_lst=['train_x','train_y']):
  split_val = int(len(input) * input_val_rate)
  input_val = input[:split_val]
  input = input[split_val:]
  if input_type == 'cor':
    train_x = [input[i:i + input_dim] for i in range(0,len(input)-input_dim+1)]
    val_x = [input_val[i:i + input_dim] for i in range(0,len(input_val)-input_dim+1)]


  train_y = []
  for i in train_x[1:]:
    match input_type:
      case 'cor':
        match i[input_dim-1]:
          case 0:
            train_y.append([0,0])
          # case 1 | 2 | 3 | 4 | 5 | 6 | 7:
          case 1:
            train_y.append([1,0])
          # case 8 | 9 | 10 | 11 | 12 | 13 | 14:
          case 2:
            train_y.append([0,1])

          case 1:
            train_y.append(1)
          case _:
            train_y.append(0)



  val_y = []
  for i in val_x[1:]:
    match input_type:
      case 'cor':
        match i[input_dim-1]:
          case 0:
            val_y.append([0,0])
          # case 1 | 2 | 3 | 4 | 5 | 6 | 7:
          case 1:
            val_y.append([1,0])
          # case 8 | 9 | 10 | 11 | 12 | 13 | 14:
          case 2:
            val_y.append([0,1])



  train_x = train_x[:-1]
  val_x = val_x[:-1]

  output = []
  for item in return_lst:
     match item:
        case 'train_x':
           output.append(train_x)
        case 'val_x':
           output.append(val_x)
        case 'train_y':
           output.append(train_y)
        case 'val_y':
           output.append(val_y)


  return tuple(output)

   
  
input_dim = 5

LancesBlaze = CarregarLances(100)

train_x, val_x, train_y, val_y = SepararTreinamento(input=LancesBlaze,input_dim=input_dim, return_lst=['train_x','val_x', 'train_y', 'val_y'])


model = Sequential()

model.add(BatchNormalization())
model.add(LSTM(units=64, input_shape=(None, 5)))


predict_input = CarregarLances(input_dim)

print(train_x)

quit()

lr = 0.009

SGD_optimizer = SGD(learning_rate=lr, momentum= 0.9)
Adagrad_optimizer = Adagrad(learning_rate=lr)

model.compile(loss='mse', optimizer=Adagrad_optimizer, metrics=['accuracy'],run_eagerly=True)

history = model.fit(train_x, train_y, epochs=20) #,validation_data=(val_x,val_y)




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
        input_layer = CarregarLances(30)
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


