import requests
import numpy as np

from collections import Counter
from termcolor import colored
from colorama import init, Fore, Style
init()

blaze_api_url = 'https://blaze-4.com/api/roulette_games/history'


def Get(NumLances, ReturnType='var', Values=['roll', 'color', 'created_at']):
    global blaze_api_url
    UltimosLances = []
    if NumLances < 300:
        result_json = (requests.get(blaze_api_url)).json()
        resultados = reversed(result_json['records'])
        for resultado in resultados:
            match ReturnType:
                case 'cor':
                    UltimosLances.append(ConverterCor(resultado['color']))
                case 'var':
                    Lance = []
                    for Value in Values:
                        Lance.append(resultado[Value])
                    UltimosLances.append(Lance)

    else:
        total_pages = int(NumLances / 300) + 1
        for page in reversed(range(1, total_pages+1)):
            result_json = (requests.get(blaze_api_url + '?page=' + str(page))).json()
            resultados = reversed(result_json['records'])
            print('page :',page)
            for resultado in resultados:
                match ReturnType:
                    case 'cor':
                        UltimosLances.append(ConverterCor(resultado['color']))
                    case 'var':
                        Lance = []
                        for Value in Values:
                            Lance.append(resultado[Value])
                        UltimosLances.append(Lance) 
    UltimosLances = UltimosLances[len(UltimosLances)-NumLances:]
    return UltimosLances

def ConverterCor(input, input_type='string', output_type='int'):
    strings = ['white', 'red', 'black']
    strings_ptbr = ['branco', 'vermelho', 'preto']
    numbers = [0,1,2]
    IA_numbers = [[0,0],[1,0],[0,1]]
    
    ColorTypes = {'string':strings,
                  'string_ptbr':strings_ptbr,
                   'int':numbers,
                   'IA':IA_numbers
                   }

    Color = '#N/D'

    for i, Value in enumerate(ColorTypes[input_type]):
        input_temp = input
        Value_temp = Value
        if input_type == 'IA':
            input_temp = np.argmax(input) + 1
            Value_temp = Value.index(max(Value)) + 1
                    
        if input_temp == Value_temp:
            Color =  ColorTypes[output_type][i]
            
    return Color

def PrintLances(num_lances):
        lst = Get(num_lances, ReturnType='var', Values=['roll', 'color'])
        for lance in lst:
            cor = ConverterCor(lance[1])
            match cor:
                case 0:
                    cor_txt = 'black'
                    bg_txt = 'white'
                case 1:
                    cor_txt = 'white'
                    bg_txt = 'red'
                case 2:
                    cor_txt = 'white'
                    bg_txt = 'black'
            print(colored(f'[{lance[0]}]',cor_txt,f'on_{bg_txt}'), end='')
        print('')

def LancesDepoisDaBranca():
    ListaDeLances = reversed(Get(200))
    UltimaBranca = 0
    for i, Value in enumerate(ListaDeLances):
        if Value[0] == 0:
            UltimaBranca = i
            return UltimaBranca

def CountLances(num_lances, colors=[0,1,2]):
    lances = Get(num_lances,ReturnType='cor')
    contagem = 0
    for lance in lances:
        if lance in colors:
            contagem += 1

    return contagem


