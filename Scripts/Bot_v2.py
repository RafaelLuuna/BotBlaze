#-----------------------------------------------[ IMPORTS ]-----------------------------------------------#

import requests
import json
import time
import random
import datetime
import os
import sys
import shutil
from collections import Counter
import numpy as np

import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.optimizers import Adagrad



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from termcolor import colored
from colorama import init, Fore, Style
init()

script_dir = os.path.dirname(os.path.abspath(__file__))
TimeRecord = str(time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
sys.stderr = open(os.path.join(script_dir,'/erros/errorLog'+TimeRecord+'.log'), 'w')

Config_path = os.path.join(script_dir,'Config.txt')


os.system('cls')
print(colored("*Dica: Pressione 'ctrl + c' a qualquer momento para encerrar o aplicativo",'yellow'))
print('')
print('                         [BOT BLAZE 2023]                         ')
print('')
print('_______________________Configuraçoes do bot_______________________')



print('')

Objetivo_final = 0
ConstMeta = 0
LeituraMáximaDeLances = 0
Limite_Max_Apostas = 0
MargemAposta = 0
SalvarNaCor = False
ModoAtaque = False
TaxaBranca_ModoAtaque = 0
OpcaoDeProtecao = 0
DobrarMeta = False
QntLancesParaDobrar = 0
TaxaCor = 0
Pausa = False


Comando = input('Deseja fazer uma simulaçao ao vivo ou jogar agora? ( s - simulação | j - jogar ):')

if(Comando == 's'):
    Simulacao = True
    Saldo_Simulacao = int(input('Qual sera o saldo inicial?:'))
    print('[Iniciando carteira simulada]')
elif(Comando == 'j'):
    Simulacao = False
else:
    print('[ --- Comando inválido --- ]')
    quit()



def CarregarTendencias(_ValorInicial,_0_Num_1_Collor):
    ListaDeTendencias = []
    x = _ValorInicial
    ListaDeTendencias.append({'tend':[x,x+1,x+2],'peso':1*CountBrancas})
    ListaDeTendencias.append({'tend':[x,x,x],'peso':2})

    return ListaDeTendencias
#__________________________________________________________________#





#____________________________NOTAS DE MELHORIAS________________________#

# 1. Simular carteira virtual para detectar quando estiver pagando.

# 2. diminuir constante de meta quando a banca estiver alta. Aumentar apenas no início do jogo (Até as 5 primeiras).

# 3. 
















#-----------------------------------------------[ PREPARAÇÃO DE AMBIENTE ]-----------------------------------------------#

import BlazeFunctions.Lances as Lances

LancesBlaze = Lances.Get(10)
LanceBlazeAtual = LancesBlaze[0]
UltimoLance = LanceBlazeAtual

from BlazeFunctions.chromeFunctions import driver_class

driver = driver_class()

driver.initialize_browser()


quit()

if(Simulacao == False):
    if(input('Digite "ok" para continuar: ') == 'ok'):
        print('Iniciando apostas')

def GetSaldo():
    if (Simulacao == False):
        div_element = driver.find_element(By.CLASS_NAME, 'currency')
        return div_element.text[3:].replace(".","").replace(",",".")
    else:
        return Saldo_Simulacao

#-----------------------------------------------[ VARIÁVEIS ]-----------------------------------------------#


TempInicio = datetime.datetime(int(str(LanceBlazeAtual[2])[2:6]),int(str(LanceBlazeAtual[2])[7:9]),int(str(LanceBlazeAtual[2])[10:12]),int(str(LanceBlazeAtual[2])[13:15]),int(str(LanceBlazeAtual[2])[16:18]),int(str(LanceBlazeAtual[2])[19:21]))
SaldoInicial = round(float(GetSaldo()))
Carteira = SaldoInicial
CountBrancas = 0
MetaAtual = 0


TotalApostado = 0
TotalApostadoBranca = 0
TotalApostadoVermelha = 0
TotalApostadoPreta = 0

SugestaoIA = {'cor':0, 'Output':[[0,0]]}
AcertosIA = 0
ErrosIA = 0
AcertosIA_temp = 0
ErrosIA_temp = 0


ContagemAposta = 0

PicoMaximo = 0
piso = 0

ListagemDeLances = []
ListagemDeLances_Limite = []

LancesDepoisDaBranca = []

TendenciasEncontradas = []

ModelPath = ''

#-----------------------------------------------[ FUNÇÕES ]-----------------------------------------------#

def ConfigurarDiretoNoPrompt():
    print()
    # Objetivo_1 = int(input('Digite o objetivo 1: '))
    # Objetivo_2 = int(input('Digite o objetivo 2: '))
    # Objetivo_3 = int(input('Digite o objetivo 3: '))
    # Objetivo_final= int(input('Digite o objetivo final: '))

    # print('')

    # ConstMeta_0 = int(input('No começo, a meta vai aumentar de: '))
    # ConstMeta_1 = int(input('Depois do objetivo 1, a meta vai aumentar de: '))
    # ConstMeta_2 = int(input('Depois do objetivo 2, a meta vai aumentar de: '))
    # ConstMeta_3 = int(input('No ultimo objetivo, a meta vai aumentar de: '))

    # print('')

    # LeituraMáximaDeLances = int(input('Quantos lances o bot precisa analisar?: '))

    # print('')

    # Limite_Max_Apostas = int(input('Quantas vezes o bot vai apostar antes de parar?: '))

    # print('')

    # MargemAposta = int(input('Margem para apostas: '))

    # print('')

    # Comando = input('Deseja proteçao na cor? (s / n): ')
    # if(Comando == 's'):
    #     SalvarNaCor = True
    #     print('------------- Opçoes de mecânica de proteção -------------')
    #     print('1 - Apostar na cor mais frequente')
    #     print('2 - Apostar na cor menos frequente')
    #     print('3 - Apostar na mais frequente apeneas nas 5 primeiras rodadas, depois disso, apostar na menos frequente')
    #     print('4 - Repetir a última cor')
    #     print('')
    #     OpcaoDeProtecao = int(input('Escolha uma opçao: '))
    #     if not(OpcaoDeProtecao == 1 or OpcaoDeProtecao == 2 or OpcaoDeProtecao == 3 or OpcaoDeProtecao == 4):
    #         print('[ --- Comando invalido --- ]')
    #         time.sleep(2)
    #         quit()
    # elif(Comando == 'n'):
    #     SalvarNaCor = False
    # else:
    #     print('[ --- Comando invalido --- ]')
    #     time.sleep(2)
    #     quit()

    # print('')

    # Comando = input('Deseja dobrar a meta nos primeiros lances? (s / n): ')
    # if(Comando == 's'):
    #     DobrarMeta = True
    #     QntLancesParaDobrar = int(input('Digite a quantidade de lances que deseja dobrar : '))
    # elif(Comando == 'n'):
    #     DobrarMeta = False
    # else:
    #     print('[ --- Comando invalido --- ]')
    #     time.sleep(2)
    #     quit()

    # print('')

Cor = 0


def AtualizarVariaveis():
    global Objetivo_final
    global ConstMeta
    global LeituraMáximaDeLances
    global Limite_Max_Apostas
    global MargemAposta
    global piso
    global SalvarNaCor
    global ModoAtaque
    global OpcaoDeProtecao
    global DobrarMeta
    global QntLancesParaDobrar
    global TaxaCor
    global Pausa
    global TaxaBranca_ModoAtaque

    global model
    global ModelPath

    try:
        with open(Config_path,'r') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                chave, valor = linha.strip().split('=')
                match chave:
                    case 'Objetivo_final':
                        Objetivo_final = int(valor)
                    case 'Const_meta':
                        ConstMeta = int(valor)
                    case 'leitura_Maxima_de_lances':
                        LeituraMáximaDeLances = int(valor)
                    case 'Limite_de_apostas':
                        Limite_Max_Apostas = int(valor)
                    case 'Margem_de_apostas':
                        MargemAposta = int(valor)
                    case 'Piso':
                        piso = int(valor)
                    case 'Protecao_na_cor':
                        if(valor == 's'):
                            SalvarNaCor = True
                        elif(valor == 'n'):
                            SalvarNaCor = False
                    case 'Tipo_de_protecao':
                        OpcaoDeProtecao = int(valor)
                    case 'Dobrar_meta':
                        if(valor == 's'):
                            DobrarMeta = True
                        elif(valor == 'n'):
                            DobrarMeta = False
                    case 'Lances_dobrados':
                        QntLancesParaDobrar = int(valor)
                    case 'TaxaCor':
                        if(valor[:3] == 'ATK'):
                            ModoAtaque = True
                            TaxaCor = 0
                            TaxaBranca_ModoAtaque = float(valor[4:])
                        else:
                            ModoAtaque = False
                            TaxaCor = float(valor)
                    case 'Pausa':
                        if(valor == 's'):
                            Pausa = True
                        elif(valor == 'n'):
                            Pausa = False
                    case 'ModelPath':
                        ModelPath = valor

    except FileNotFoundError:
        print("Arquivo de configuração não encontrado.")
    except Exception as e:
        print(f"Erro ao atualizar variáveis: {e}")

#test

def CarregarLances_IA(NumLances, ReturnType):
    UltimosLances = []
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
    UltimosLances = UltimosLances[len(UltimosLances)-NumLances:]
    return UltimosLances


def AtualizarLances():
    global LancesBlaze
    global LanceBlazeAtual
    global LancesDepoisDaBranca
    global LanceBlazeAtual
    global ListagemDeLances
    global ListagemDeLances_Limite
    global CountBrancas
    global LeituraMáximaDeLances
    global SugestaoIA
    global AcertosIA
    global AcertosIA_temp
    global ErrosIA
    global ErrosIA_temp

    LancesBlaze = requests.get('https://blaze-1.com/api/roulette_games/recent').json()
    LanceBlazeAtual = [[LancesBlaze[0]['roll']],[LancesBlaze[0]['color']],[LancesBlaze[0]['created_at']]]

    if(LanceBlazeAtual[1][0] == SugestaoIA['cor'] and not(LanceBlazeAtual[0] == [0])):
        ErrosIA_temp = 0
        AcertosIA += 1
        AcertosIA_temp += 1
    else:
        AcertosIA_temp = 0
        ErrosIA += 1
        ErrosIA_temp += 1

    if (LanceBlazeAtual[0] == [0]):
        LancesDepoisDaBranca.clear()
    else:
        LancesDepoisDaBranca.append(LanceBlazeAtual)
    
    ListagemDeLances.append(LanceBlazeAtual)

    MaxLen = len(ListagemDeLances) 
    MinLen = MaxLen - 20
    if(MinLen < 0):
        MinLen = 0
    CountBrancas = ContarBrancas(MinLen,MaxLen)
    
    ListagemDeLances_Limite.clear()
    for i in range(MinLen,MaxLen):
        TextCollor = ''
        if (ListagemDeLances[i][1] == [0]):
            TextCollor = 'white'
        if (ListagemDeLances[i][1] == [1]):
            TextCollor = 'red'
        if (ListagemDeLances[i][1] == [2]):
            TextCollor = 'black'
        tend = False
        
        ListagemDeLances_Limite.append([int(str(ListagemDeLances[i][0])[1:-1]),TextCollor,tend])


def ContarBrancas(_Start,_End):
    x = 0
    for i in range(_Start,_End):
        if(ListagemDeLances[i][0] == [0]):
            x = x + 1
    return x

def IncluirAposta(Valor,Cor):
    global TotalApostado
    global TotalApostadoBranca
    global TotalApostadoVermelha
    global TotalApostadoPreta

    if (Simulacao == False):
        try:
            input_element = driver.find_element(By.CLASS_NAME, 'input-field')
            if(Valor > 0):
                input_element.send_keys(Valor)
            else:
                input_element.send_keys(1)
        except:
            print("####ERRO: Não foi possível incluír o valor da aposta")
    

    match Cor:
        case 0:
            if (Simulacao == False):
                try:
                    click_button = driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[2]')
                    click_button.click()
                except NoSuchElementException:
                    print("")
            TotalApostadoBranca = round(TotalApostadoBranca + Valor, 2)
        case 1:
            if (Simulacao == False):
                try:
                    click_button = driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[1]')
                    click_button.click()
                except NoSuchElementException:
                    print("")
            TotalApostadoVermelha = round(TotalApostadoVermelha + Valor, 2)
        case 2:
            if (Simulacao == False):
                try:
                    click_button = driver.find_element(By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[3]')
                    click_button.click()
                except NoSuchElementException:
                    print("")
            TotalApostadoPreta = round(TotalApostadoPreta + Valor, 2)
    TotalApostado = round(TotalApostado + Valor, 2)

    
def Apostar(Cor):
    global LucroPerda
    global Carteira
    global TotalApostado
    global TotalApostadoBranca
    global TotalApostadoVermelha
    global TotalApostadoPreta
    if(Simulacao == False):
        try:
            wait = WebDriverWait(driver, 10)
            click_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="roulette-controller"]/div[1]/div[3]/button')))
            click_button.click()
            Carteira = round(float(GetSaldo()))
        except:
            print("###ERRO: Não foi possível clicar no botão de aposta")
    else:
        match Cor:
            case 0:
                Carteira = round(Carteira - TotalApostadoBranca,2)
            case 1:
                Carteira = round(Carteira - TotalApostadoVermelha,2)
            case 2:
                Carteira = round(Carteira - TotalApostadoPreta,2)
    


def PagarPremio():
    global Carteira
    global TotalApostadoBranca
    global TotalApostadoVermelha
    global TotalApostadoPreta
    global LanceBlazeAtual
    ValorPremio = 0
    if(LanceBlazeAtual[1] == [0]):
        ValorPremio = round(TotalApostadoBranca * 14, 2)
    if(LanceBlazeAtual[1] == [1]):
        ValorPremio = round(TotalApostadoVermelha * 2, 2)
    if(LanceBlazeAtual[1] == [2]):
        ValorPremio = round(TotalApostadoPreta * 2, 2)
    Carteira = round(Carteira + ValorPremio, 2)

    print('pagou:',ValorPremio)

def AtualizarMeta(_Carteira,_Constante):
    global MetaAtual
    MetaAtual = round(_Carteira + _Constante)

AchouTendencia = False
PesoTendencia = 0

# def PrevisaoDePerda(_SaldoInicial,_MetaAtual):
#     global Limite_Max_Apostas
#     global ContagemAposta
#     _Carteira = _SaldoInicial
#     _PerdaPotencial = 0
#     for i in range(Limite_Max_Apostas - ContagemAposta):
#         _ApostaAtual = 0
#         while(_Carteira-_ApostaAtual+(_ApostaAtual*14) <= _MetaAtual):
#             _ApostaAtual = _ApostaAtual + ConstAposta #NÃO USO MAIS A CONSTAPOSTA, FAÇO A DIVISÃO
#         _PerdaPotencial = _PerdaPotencial+_ApostaAtual
#         _Carteira = _Carteira - _ApostaAtual
#     return _PerdaPotencial

# def AcharTendencia():
    # global ListagemDeLances_Limite
    # global TendenciasEncontradas
    # global AchouTendencia
    # global PesoTendencia
    # tempLancesDepoisDaBranca = []
    # TendenciasEncontradas.clear()
    # AchouTendencia = False
    # PesoTendencia = 0

    # for i in range(0,len(ListagemDeLances_Limite)):
    #     if 0 in [item[0] for item in ListagemDeLances_Limite]:
    #         tempLancesDepoisDaBranca.append(-10)
    #     else:
    #         tempLancesDepoisDaBranca.append(ListagemDeLances_Limite[i][0])

    # for i in range(0, len(tempLancesDepoisDaBranca)):
    #     subsequenceList = CarregarTendencias(tempLancesDepoisDaBranca[i],0)
    #     for subsequence in subsequenceList:
    #         sub_len = len(subsequence['tend'])

    #         if (tempLancesDepoisDaBranca[i:i+sub_len] == subsequence['tend']):
                
    #             AchouTendencia = True

    #             TendenciasEncontradas.append(subsequence['tend'])
    #             for iLance in range(i,i+sub_len):
    #                 ListagemDeLances_Limite[iLance][2] = True
    #                 PesoTendencia = subsequence['peso']


csv_path = os.path.join(script_dir,'LogApostas.csv')
# csv_record_path = os.path.join(script_dir,"LogsApostas\\")

# shutil.copy(csv_path,csv_record_path)

try:
    os.remove(csv_path)
except FileNotFoundError:
    print('')

with open(csv_path, 'a+') as csv_file:
    csv_titles = 'Num_sorteado;Cor;Data;Saldo_atual;Meta;Total_apostado_branca;Total_apostado_vermelha;Total_apostado_preta;Sugestão_IA'
    csv_file.write(csv_titles)

def ImprimirLanceCSV(ListaDados):
    global LanceBlazeAtual
    global csv_file
    global Carteira
    global MetaAtual
    global TotalApostado
    global AchouTendencia
    global ContagemAposta
    global TendenciasEncontradas
    AtualizarVariaveis()
    with open(csv_path, 'a+') as csv_file:
        sorted = ''
        for item in ListaDados:
            sorted += str(item) + ';'
        csv_file.write('\n' + sorted )

AtualizarVariaveis()

NumTotalDeApostas = 0
CountPerdas = 0
ApostaAtual = 0

LucroPerda = 0

SaldoBase = Carteira
AtualizarMeta(Carteira,ConstMeta)

if(Carteira > PicoMaximo):
    PicoMaximo = Carteira

#-----------------------------------------------[ PRINTS ]-----------------------------------------------#

def PrintConfig():

    print('')
    print('-----------------------------[CONFIGURAÇÕES DO BOT]-----------------------------')

    print('Saldo inical: ', SaldoInicial)
    print('Saldo base atual: ', SaldoBase)
    print('Maior saldo até o momento: ',PicoMaximo)
    print('Objetivo: ',Objetivo_final)

    print('')
    
    print('Const. da meta atual: ', ConstMeta)

    print('')

    print('Leitra maxima de lances: ',LeituraMáximaDeLances)

    print('')

    print('Limite maximo de apostas:',Limite_Max_Apostas)
    print('Margem para apostas: ',MargemAposta)

    print('')

    print('Protecao na cor: ',SalvarNaCor )
    match OpcaoDeProtecao:
        case 1:
            txtOpcaoProtecao = '1 - Apostar na cor mais frequente'
        case 2:
            txtOpcaoProtecao = '2 - Apostar na cor menos frequente'
        case 3:
            txtOpcaoProtecao = '3 - Apostar na mais frequente apeneas nas 5 primeiras rodadas, depois disso, apostar na menos frequente'
        case 4:
            txtOpcaoProtecao = '4 - Repetir a última cor'
        case 5:
            txtOpcaoProtecao = '5 - Sugestão da IA'
    print('Opcao de protecao: ',txtOpcaoProtecao)
    print('Taxa Cor:' , TaxaCor)

    print('')

    print('Dobrar meta: ',DobrarMeta)
    if(DobrarMeta == True):
        print('Lances dobrados: ', QntLancesParaDobrar)

    print('Modo Simulacao: ',Simulacao)

    print('Modelo IA: ', ModelPath)

    print('----------------------------------------------------------------------------------')


def PrintLog():
    CorSaldo = 'green'
    if(Carteira < SaldoInicial):
        CorSaldo = 'red'
    # os.system('cls')
    print('__________________________________________________________________________')
    print('#',NumTotalDeApostas,' | Tempo de jogo:', DeltaTempo)
    print('Num. apostas: ', ContagemAposta)
    print('Saldo atual:', colored(Carteira,CorSaldo))
    print('Valor apostado:', -TotalApostado, colored('[Branca: ','black','on_white'),TotalApostadoBranca,colored(' | Vermelha: ','white','on_red'),TotalApostadoVermelha,colored(' | Preta: ','white','on_black'),TotalApostadoPreta,colored(']','white','on_black'))
    print('Meta atual:', colored(MetaAtual,'blue'),' | Piso: ', piso)
    if(LucroPerda>0):
        Cor = 'green'
    else:
        Cor = 'red'
    print('lucro / perda no último lance:', colored(round(LucroPerda,2),Cor))
    match CorMaisComum:
        case 0:
            Cor = 'white'
        case 1:
            Cor = 'red'
        case 2:
            Cor = 'black' 
    print('Ultimo numero sorteado:', LanceBlazeAtual[0], ' | Cor mais comum:',Cor, ' | Sugestão IA: ', SugestaoIA['Output'], '(Taxa de acerto: ', round(AcertosIA / (AcertosIA+ErrosIA) * 100,2),'%)')
    print('Brancas nos ultimos 20 lances: ',CountBrancas,' | A ultima branca foi a ', colored(len(LancesDepoisDaBranca),'black','on_white'),'rodadas')
    print('__________________________________________________________________________')
    input_layer = np.array(CarregarLances_IA(LeituraMáximaDeLances,'cor')).reshape(-1,LeituraMáximaDeLances)
    print('lances IA: ', )

def PrintLances(lst):
        for item in lst:
            if(item[2] == True):
                print(colored('['+str(item[0])+']','black','on_green'), end='')
            else:
                Collor = 'white'
                if(item[1] == 'white'):
                    Collor = 'black'
                print(colored('['+str(item[0])+']',Collor,'on_'+item[1]), end='')
            
        print('')

def PrintTendencias():
    print('Tendencias encontradas:')
    print(TendenciasEncontradas)

def PredictIA():
    global SugestaoIA
    global LeituraMáximaDeLances
    global model
    model = load_model(ModelPath)
    model.save('backup.keras')
    input_layer = CarregarLances_IA(LeituraMáximaDeLances,'cor')
    # input_size = 5
    # input_layer_final = []
    # for i in range(1,int(round(LeituraMáximaDeLances/input_size,0))+1):
    #     input_layer_final.append(input_layer[(i-1)*input_size:i*input_size])
    # input_layer_final = [np.array(input).reshape(-1,5) for input in input_layer_final]
    input_layer = np.array(input_layer).reshape(-1,LeituraMáximaDeLances)
    SugestaoIA['Output'] = model.predict(input_layer)
    SugestaoIA['cor'] = np.argmax(np.array(model.predict(input_layer)))+1

#-----------------------------------------------[ ROTINA DO BOT ]-----------------------------------------------#

def TreinarIA(NumLances):
    global model
    global ModelPath
    global LeituraMáximaDeLances
    input_test = CarregarLances_IA(NumLances,'cor')
    LancesBlaze_treinamento = [input_test[i:i + LeituraMáximaDeLances] for i in range(0,len(input_test)-LeituraMáximaDeLances+1)]
    resultados_treinamento = []
    for i in LancesBlaze_treinamento[1:]:
        match i[LeituraMáximaDeLances-1]:
            case 0:
                resultados_treinamento.append([0,0])
            case 1:
                resultados_treinamento.append([1,0])
            case 2:
                resultados_treinamento.append([0,1])

    resultados_treinamento = np.array(resultados_treinamento)
    LancesBlaze_treinamento = np.array(LancesBlaze_treinamento[:-1])

    lr = 0.05
    Adagrad_optimizer = Adagrad(learning_rate=lr)

    model.compile(loss='mse', optimizer=Adagrad_optimizer, metrics=['accuracy'])
    model.fit(LancesBlaze_treinamento, resultados_treinamento, epochs=70)

    model.save(ModelPath)

print('[preparando para carregar modelo]')

if(OpcaoDeProtecao == 5):
    model = load_model(ModelPath)
    print('[modelo carregado]')
    model.save('backup.keras')

print('[iniciando rotina]')

while (Carteira - ApostaAtual > 0):
    #-----------------------------------------------[ INICIALIZAÇÃO ]-----------------------------------------------#
    LancesBlaze = requests.get('https://blaze-1.com/api/roulette_games/recent').json()
    LanceBlazeAtual = [[LancesBlaze[0]['roll']],[LancesBlaze[0]['color']],[LancesBlaze[0]['created_at']]]
    AtualizarVariaveis()
    if not(UltimoLance == LanceBlazeAtual):
        AtualizarLances()

        if OpcaoDeProtecao == 5:
            PredictIA()

        UltimoLance = LanceBlazeAtual
        print('[Lances atualizados][Lance blaze atual: ',LanceBlazeAtual[0],LanceBlazeAtual[1],']')
        if (Simulacao == False):
            Carteira = round(float(GetSaldo()))

        CorMaisComum = Counter([item[1] for item in ListagemDeLances_Limite[len(ListagemDeLances_Limite)-LeituraMáximaDeLances:]]).most_common(1)[0][0]

        print('Cor mais comum: ', CorMaisComum)
        match CorMaisComum:
            case 'white':
                CorMaisComum = 0
                CorMenosComum = 0
            case 'red':
                CorMaisComum = 1
                CorMenosComum = 2
            case 'black':
                CorMaisComum = 2
                CorMenosComum = 1

        print([item[1] for item in ListagemDeLances_Limite[len(ListagemDeLances_Limite)-LeituraMáximaDeLances:]])

        print('comecou com:',Carteira)

        if(TotalApostado > 0):
            PagarPremio()

        if (Simulacao == False):
            Carteira = round(float(GetSaldo()))
        if(Carteira > PicoMaximo):
            PicoMaximo = Carteira

        LucroPerda = 0
        match LanceBlazeAtual[1][0]:
            case 0:
                LucroPerda += TotalApostadoBranca * 14
            case 1:
                LucroPerda += TotalApostadoVermelha * 2
            case 2:
                LucroPerda += TotalApostadoPreta * 2
        LucroPerda -= TotalApostado


        if (LanceBlazeAtual[0] == [0]):
            ContagemAposta = 0
            if(TotalApostadoBranca > 0):
                CountPerdas = 0
                SaldoBase = Carteira
            else:
                CountPerdas = CountPerdas + 1 
        
        if(Carteira >= MetaAtual):
            ContagemAposta = 0
            SaldoBase = Carteira
            AtualizarMeta(SaldoBase,ConstMeta)

        if (PicoMaximo - MargemAposta > piso):
            piso = PicoMaximo - MargemAposta
            if piso < 0:
                piso = 0
        

        if (Carteira - ApostaAtual < piso):
            while Carteira - ApostaAtual < piso:
                input_var = input('Piso atingido, digite qualquer coisa para continuar:')
                piso = Carteira - MargemAposta


        
        #-----------------------------------------------[ REGRAS DE APOSTA ]-----------------------------------------------#
        TotalApostado = 0
        TotalApostadoBranca = 0
        TotalApostadoVermelha = 0
        TotalApostadoPreta = 0

        # AcharTendencia()
        # if(AchouTendencia == True):
        #     AtualizarMeta(SaldoBase,ConstMeta*PesoTendencia)
        # else:
        #     AtualizarMeta(SaldoBase,ConstMeta)

        if(DobrarMeta == True and ContagemAposta < QntLancesParaDobrar):
            AtualizarMeta(SaldoBase,ConstMeta*2)

        ApostaAtual = round((MetaAtual - Carteira)/14+0.1,1)
        Carteira_temporaria = Carteira - (ApostaAtual*2)
        print('[Calculando aposta atual]')
        while(Carteira_temporaria + (ApostaAtual * 14) <= MetaAtual):
            ApostaAtual = round((MetaAtual - Carteira_temporaria)/14+0.1,1)
            Carteira_temporaria = Carteira - (ApostaAtual*2) - (ApostaAtual*TaxaCor)

        
        if(ContagemAposta < Limite_Max_Apostas and Carteira < Objetivo_final and Pausa == False):

            if(ModoAtaque == False):
                IncluirAposta(ApostaAtual,0)
                Apostar(0)

            print('apostou:',TotalApostado, '[Branca: ',TotalApostadoBranca,' | Vermelha: ',TotalApostadoVermelha,' | Preta: ',TotalApostadoPreta,']')

            if(SalvarNaCor == True):
                CorNum = 0
                match OpcaoDeProtecao:
                    case 1:
                        CorNum = CorMaisComum
                    case 2:
                        CorNum = CorMenosComum
                    case 3:
                        if(len(LancesDepoisDaBranca)<5):
                            CorNum = CorMaisComum
                        else:
                            CorNum = CorMenosComum
                    case 4:
                        CorNum = LanceBlazeAtual[1][0]
                        if CorNum == 0:
                            CorNum = CorMaisComum
                    case 5:
                        CorNum = SugestaoIA['cor']

                if(not(CorNum == 0) and ErrosIA_temp < 2):
                    if(ModoAtaque == True):

                        AtualizarMeta(Carteira, ConstMeta)
                        ApostaCor = ConstMeta

                        IncluirAposta(ConstMeta * TaxaBranca_ModoAtaque,0)
                        Apostar(0)
                        
                    else:
                        if(ApostaAtual + (ApostaAtual*TaxaCor) < 5):
                            ApostaCor = 5
                        else:
                            ApostaCor = ApostaAtual + (ApostaAtual*TaxaCor)
                            
                    IncluirAposta(ApostaCor,CorNum)
                    Apostar(CorNum)
                    print('apostou:',TotalApostado, '[Branca: ',TotalApostadoBranca,' | Vermelha: ',TotalApostadoVermelha,' | Preta: ',TotalApostadoPreta,']')



            ContagemAposta = ContagemAposta + 1

        #-----------------------------------------------[ RESUMO E RELATÓRIO ]-----------------------------------------------#

        NumTotalDeApostas = NumTotalDeApostas +1

        TempFim = datetime.datetime(int(str(LanceBlazeAtual[2])[2:6]),int(str(LanceBlazeAtual[2])[7:9]),int(str(LanceBlazeAtual[2])[10:12]),int(str(LanceBlazeAtual[2])[13:15]),int(str(LanceBlazeAtual[2])[16:18]),int(str(LanceBlazeAtual[2])[19:21]))
        DeltaTempo = TempFim - TempInicio

        TreinarIA(10)

        os.system('cls')

        PrintLog()
        # if(AchouTendencia == True):
        #     PrintLog()
        #     PrintTendencias()
        PrintLances(ListagemDeLances_Limite)
        listaDados = [LanceBlazeAtual[0][0],LanceBlazeAtual[1][0],TempFim,Carteira,MetaAtual,TotalApostadoBranca,TotalApostadoVermelha,TotalApostadoPreta,SugestaoIA['Output']]
        ImprimirLanceCSV(listaDados)
        PrintConfig()
        
else:
    print('[-----------------QUEBROU-----------------]')


print('[ RESUMO ]')
print('__________________________________________________________________________')
print(' | Numero total de apostas:',NumTotalDeApostas,' | Tempo de jogo:', DeltaTempo,' | Saldo Inicial:',SaldoInicial,' | Saldo Final:',Carteira, " | Maior Saldo:", PicoMaximo)

driver.quit()

sys.stderr.close()
sys.stderr = sys.__stderr__

