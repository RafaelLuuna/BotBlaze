import os
import time
import Scripts.BlazeFunctions.Lances as Lances
from Scripts.BlazeFunctions.Bot import bot_class

Bot = bot_class(ConfigPath='./Config.txt', Saldo=1000)
Bot.driver.initialize_browser()
Bot.EsperarLance()


while Bot.Carteira.Saldo > 0:
    Bot.RunCycle()
    if Bot.Carteira.Saldo > 0:
        if Bot.OpcaoDeProtecao == 5:
            Bot.TreinarIA()
        Bot.PrintLog()
        Lances.PrintLances(30)
        Bot.PrintConfig()

        Bot.EsperarLance()
        Bot.varRotina['LanceBlazeAtual'] = Lances.Get(1)[0]
        Bot.PagarPremio()