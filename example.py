import os
import Scripts.BlazeFunctions.Lances as Lances
from Scripts.BlazeFunctions.Bot import bot_class


Bot = bot_class('./Config.txt', Saldo=1000)

Bot.driver.initialize_browser()


while Bot.Carteira.Saldo > 0:
    Bot.RunRotina()
    if Bot.OpcaoDeProtecao == 5:
        Bot.TreinarIA()
    os.system('cls')
    Bot.PrintLog()
    Lances.PrintLances(30)
    Bot.PrintConfig()
