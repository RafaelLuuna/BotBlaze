import requests
import numpy as np

def ConverterCor(Value):
    match Value:
        case 'white':
            return 0
        case 'red':
            return 1
        case 'black':
            return 2

def GetLances(NumLances, ReturnType='var', Values=['roll', 'color', 'created_at']):
    UltimosLances = []
    if NumLances < 300:
        result_json = (requests.get("https://blaze-1.com/api/roulette_games/history")).json()
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
            result_json = (requests.get("https://blaze-1.com/api/roulette_games/history?page=" + str(page))).json()
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