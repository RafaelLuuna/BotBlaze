import requests
import numpy as np

blaze_api_url = 'https://blaze-4.com/api/roulette_games/history'

def ConverterCor(input, input_type='string', output_type='int'):
    strings = ['white', 'red', 'black']
    numbers = [0,1,2]
    IA_numbers = [[0,0],[1,0],[0,1]]
    
    ColorTypes = {'string':strings,
                   'int':numbers,
                   'IA':IA_numbers
                   }

    Color = '#N/D'

    for i, Value in enumerate(ColorTypes[input_type]):
        if input == Value:
            Color =  ColorTypes[output_type][i]
            
    return Color


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
