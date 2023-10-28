import os
import random
import json
import Scripts.BlazeFunctions.Lances as Lances
from Scripts.BlazeFunctions.Bot import bot_class

from icecream import ic


gen = 0

resultados = []


for gen in range(0,100):

    Bot = ''

    Bot = bot_class('./Paths.txt', name=f'bot{gen}')


    leituraMaxima = 6

    NumeroDeLances = 50 + int(random.random()*50)

    LancesBlaze_dict = Lances.Get(NumeroDeLances, ReturnType='dict')
    LancesBlaze = [[],[],[]]
    for lance in LancesBlaze_dict:
        LancesBlaze[0].append(Lances.Converter.DictToList(lance))
        LancesBlaze[1].append(Lances.Converter.Cor(Lances.Converter.DictToList(lance,Values=['color'])[0]))
        LancesBlaze[2].append(Lances.Converter.DictToList(lance, Values=['roll', 'color']))
    

    bot_log = {
        'name':Bot.name,
        'PicoMaximo':0,
        'NumLances':0,
        'SaldoFinal':0,
        'lances':[]
        }

    log_list = []

    for i, lance in enumerate(LancesBlaze[0][:-1]):
        if i > leituraMaxima:
            log = {
                '#':0,
                'Saldo_Start':0,
                'ApostaBranca':0,
                'ApostaVermelha':0,
                'ApostaPreta':0,
                'SugestaoIA':'',
                'CorSorteada':'',
                'Saldo_End':0
                }
            min_i = i-leituraMaxima

            IA_list = LancesBlaze



            log['#'] = Bot.varRotina['NumTotalDeApostas']
            log['Saldo_Start'] = Bot.Carteira.Saldo

            Bot.RunCycle(LanceBlazeAtual=lance, IA_list=[LancesBlaze[1][min_i:i]])

            log['ApostaBranca'] = Bot.TotalApostadoBranca
            log['ApostaVermelha'] = Bot.TotalApostadoVermelha
            log['ApostaPreta'] = Bot.TotalApostadoPreta
            log['SugestaoIA'] = Lances.Converter.Cor(Bot.varRotina['SugestaoIA'],input_type='IA',output_type='string_ptbr')
            log['CorSorteada'] = LancesBlaze[0][i + 1][1]

            if Bot.Carteira.Saldo - Bot.varRotina['ApostaAtual']< 0:
                break
            Bot.PagarPremio(LancesBlaze[0][i + 1], PrintLog=False)

            log['Saldo_End'] = Bot.Carteira.Saldo

            log_list.append(log)
            bot_log['lances'] = log_list

            if Bot.Carteira.Saldo - Bot.varRotina['ApostaAtual'] <=Bot.piso:
                break
            
            # SugestaoIA = Lances.Converter.Cor(Bot.varRotina['SugestaoIA'],input_type='IA',output_type='string_ptbr')
            # h = '\n\n\n-------------------------[Saldo do bot atual]-------------------------'
            # ic(h)
            # LancesCarregados = NumeroDeLances - leituraMaxima
            # ic(min_i)
            # ic(Bot.name)
            # ic(Bot.varRotina['NumTotalDeApostas'], LancesCarregados )
            # ic(SugestaoIA)
            # ic(Bot.Carteira.Saldo, Bot.varRotina['LucroPerdaRodada'])

    bot_log['NumLances'] = Bot.varRotina['NumTotalDeApostas']
    bot_log['PicoMaximo'] = Bot.PicoMaximo
    bot_log['SaldoFinal'] = Bot.Carteira.Saldo

    resultados.append(bot_log)


json_object = json.dumps(resultados, indent=4)
with open('Report.json', 'w') as arquivo:
    arquivo.write(json_object)