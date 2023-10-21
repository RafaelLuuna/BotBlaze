import os
import time
import Scripts.BlazeFunctions.Lances as Lances
from Scripts.BlazeFunctions.Bot import bot_class

Bot = bot_class(Paths='./Paths.txt')
Bot.driver.initialize_browser()
Bot.EsperarLance()


while Bot.Carteira.Saldo > 0:

    Bot.RunCycle(Condicoes=())
    if Bot.Carteira.Saldo > 0:
        Bot.PrintLog()
        Lances.PrintLances(30)
        Bot.PrintConfig()

        Bot.EsperarLance()
        Bot.PagarPremio(Lances.Get(1)[0])