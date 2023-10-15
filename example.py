import os
import time
import Scripts.BlazeFunctions.Lances as Lances
from Scripts.BlazeFunctions.Bot import bot_class

from termcolor import colored
from colorama import init, Fore, Style
init()

def PrintCabecalho():
    os.system('cls')
    print(colored("*Dica: Pressione 'ctrl + c' a qualquer momento para encerrar o aplicativo",'yellow'))
    print('')
    print('                         [BOT BLAZE 2023]                         ')
    print('')
    print('__________________________________________________________________')

ConfigPath = './Config.txt'
SaldoInicial = 1000
Start = False
while Start == False:
    with open(ConfigPath, 'r') as arquivo:
        Linhas = arquivo.readlines()
        for linha in Linhas:
            chave, valor = linha.strip().split('=')
            if chave == 'Simulacao':
                match valor:
                    case 's':
                        GameMode = 'Simulação'
                    case 'n':
                        GameMode = 'Modo real'
    PrintCabecalho()
    print('\n[Configuração atual do bot]\n')
    print(f'config_path: {ConfigPath}')
    print(f'game_mode: {GameMode}')
    if GameMode == 'Simulação':
        print(f'saldo_inicial: {SaldoInicial}')
    print('\n\n[Lista de comandos]\n')
    print('> jogar')
    print('> game mode')
    print('> settings')
    print('> quit')
    print('\n\n\n')


    Comando = input('Digite um comando: ')

    if Comando == 'settings':
        inSetting = True
        while inSetting == True:
            PrintCabecalho()
            print('\n\n[Lista de comandos]\n')
            print('> config_path')
            if GameMode == 'Simulação':
                print('> alterar saldo')
            print('> return')
            print('\n\n\n')
            Comando = input('Digite um comando: ')
            match Comando:
                case 'config_path':
                    input_txt = ''
                    while input_txt == '':
                        input_txt = input('Digite o caminho do arquivo de configuração: ')
                        if input_txt == '':
                            print('\n   Erro: o caminho do arquivo de configuração não pode ser vazio\n')
                        else:
                            ConfigPath = input_txt
                    Comando = 'pass'
                    inSetting = False
                case 'alterar saldo':
                    if GameMode == 'Simulação':
                        SaldoInicial = float(input('Digite o valor que deseja: '))
                        Comando = 'pass'
                        inSetting = False
                case 'return':
                    Comando = 'pass'
                    inSetting = False
                case _:
                    print('\n    Erro: comando inválido\n')
                    time.sleep(1)
            
            
    
    match Comando:
        case 'jogar':
            Start = True
        case 'game mode':
            newValue = ''
            while newValue == '':
                os.system('cls')
                print('\nEscolha um modo de jogo:\n\n1 - Simulação\n2 - Modo real (necessário logar na sua conta da Blaze)\n')
                opcao = input('Escolha uma opção: ')
                match opcao:
                    case '1':
                        newValue = 'Simulacao=s\n'
                    case '2':
                        newValue = 'Simulacao=n\n'
                    case _:
                        print('\n    Erro: opção inválida\n')

            with open(ConfigPath, 'r') as arquivo:
                Linhas = arquivo.readlines()
                for i, linha in enumerate(Linhas):
                    chave, valor = linha.strip().split('=')
                    if chave == 'Simulacao':
                        Linhas[i] = newValue
            with open(ConfigPath, 'w') as arquivo:
                arquivo.writelines(Linhas)
                arquivo.flush
        case 'quit':
            quit()
        case 'pass':
            pass
        case _:
            print('\n    Erro: comando inválido\n')
            time.sleep(1)
            

match GameMode:
    case 'Modo real':
        Bot = bot_class(ConfigPath=ConfigPath)
        Bot.driver.initialize_browser()
        Bot.EsperarLogin()
        Bot.EsperarLance()
        if Bot.Carteira.Saldo <=0:
            print('\n    Erro: saldo zerado, por favor, entre em uma conta que possua algum saldo disponível para jogar')
            time.sleep(1)
    case "Simulação":
        Bot = bot_class(ConfigPath=ConfigPath, Saldo=SaldoInicial)
        Bot.driver.initialize_browser()
        Bot.EsperarLance()


while Bot.Carteira.Saldo > 0:
    Bot.RunCycle(LanceBlazeAtual=Lances.Get(1)[0])
    if Bot.Carteira.Saldo > 0:
        if Bot.OpcaoDeProtecao == 5:
            Bot.TreinarIA(num_lances=40, epochs=10, learning_rate=0.04)
        Bot.PrintLog()
        Lances.PrintLances(30)
        Bot.PrintConfig()

        Bot.EsperarLance()
        Bot.varRotina['LanceBlazeAtual'] = Lances.Get(1)[0]
        Bot.PagarPremio()
