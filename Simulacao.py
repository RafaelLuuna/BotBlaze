import os
import random
import Scripts.BlazeFunctions.Lances as Lances
from Scripts.BlazeFunctions.Bot import bot_class

from icecream import ic


gen = 0

resultados = []



for gen in range(0,100):

    Bot = ''

    Bot = bot_class('./Paths.txt', name=f'bot{gen}')

    leituraMaxima = 20

    NumeroDeLances = 30 + int(random.random()*50)

    LancesBlaze_dict = Lances.Get(NumeroDeLances, ReturnType='dict')
    LancesBlaze = [[],[],[]]
    for lance in LancesBlaze_dict:
        LancesBlaze[0].append(Lances.Converter.DictToList(lance))
        LancesBlaze[1].append(Lances.Converter.Cor(Lances.Converter.DictToList(lance,Values=['color'])[0]))
        LancesBlaze[2].append(Lances.Converter.DictToList(lance, Values=['roll', 'color']))



    for i, lance in enumerate(LancesBlaze[0][:-1]):
        min_i = i-leituraMaxima
        if min_i < 0:
            min_i = 0

        print(f'\n[GERAÇÃO: {gen}]')
        Bot.RunCycle(LanceBlazeAtual=lance, Condicoes=(Bot.varRotina['ErrosIA_temp'] < 2))

        print('\n')
        print(f'Sugestão da IA foi: {Lances.Converter.Cor(Bot.varRotina["SugestaoIA"], input_type="IA", output_type="string_ptbr")}')
        print(f'A IA errou {Bot.varRotina["ErrosIA_temp"]} vezes consecutivas')

        if Bot.Carteira.Saldo - Bot.varRotina['ApostaAtual']< 0:
            break
        Bot.PagarPremio(LancesBlaze[0][i + 1])

        if Bot.Carteira.Saldo - Bot.varRotina['ApostaAtual'] <=Bot.piso:
            break
        
        h = '\n\n\n-------------------------[Saldo do bot atual]-------------------------'
        ic(h)
        ic(Bot.varRotina['NumTotalDeApostas'], NumeroDeLances)
        ic(Bot.varRotina['ErrosIA_temp'],Bot.varRotina['AcertosIA_temp'])
        ic(Bot.Carteira.Saldo, Bot.varRotina['LucroPerdaRodada'])

        h = '\n-------------------------[Registros]-------------------------'
        ic(h)
        ic(resultados)
    

    resultados.append({'name':Bot.name, 'PicoMaximo':Bot.PicoMaximo, 'NumLances':Bot.varRotina['NumTotalDeApostas'], 'SaldoFinal':Bot.Carteira.Saldo})


ic(resultados)