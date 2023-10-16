import os
import Scripts.BlazeFunctions.Lances as Lances
from Scripts.BlazeFunctions.Bot import bot_class

Bot = bot_class('./Config.txt', Saldo=1000)

LancesBlaze = Lances.Get(10)

for i, lance in enumerate(LancesBlaze[:-1]):
    Bot.RunCycle(lance)
    if Bot.Carteira.Saldo < 0:
        break
    Bot.varRotina['LanceBlazeAtual'] = LancesBlaze[i + 1]
    Bot.PagarPremio()



Bot.PrintLog()
Bot.PrintConfig()
