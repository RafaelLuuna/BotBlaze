import os
import sys
import time
from icecream import ic
import Scripts.BlazeFunctions.Lances as Lances
from Scripts.BlazeFunctions.Bot import bot_class

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.stderr = open(os.path.join(script_dir,'errorLog.log'), 'w+')


from termcolor import colored
from colorama import init, Fore, Style
init()

def Write(FilePath, VarName, NewValue):
    with open(FilePath, 'r') as arquivo:
        Linhas = arquivo.readlines()
        for i, linha in enumerate(Linhas):
            chave, valor = linha.strip().split('=')
            if chave == VarName:
                Linhas[i] = VarName + '=' + NewValue + '\n'
    with open(FilePath, 'w') as arquivo:
        arquivo.writelines(Linhas)
        arquivo.flush()

def PrintCabecalho():
    os.system('cls')
    print(colored("*Dica: Pressione 'ctrl + c' a qualquer momento para encerrar o aplicativo",'yellow'))
    print('')
    print('                         [BOT BLAZE 2023]                         ')
    print('')
    print('__________________________________________________________________')

Paths = os.path.join(script_dir,'Paths.txt')
Bot_temp = bot_class(Paths=Paths)
Bot_temp.RunCycle()

Start = False
while Start == False:
    Bot_temp.UpdateConfig()
    Bot_temp.Carteira.Saldo = Bot_temp.GetConfig(['SaldoInicial'])
    Bot_temp.Carteira.SaldoInicial = Bot_temp.GetConfig(['SaldoInicial'])
    

    match Bot_temp.GetConfig(['Simulacao']):
        case 's':
            GameMode = 'Simulação'
        case 'n':
            GameMode = 'Modo real'

                
    PrintCabecalho()
    print('\n[Configuração atual do bot]\n')
    print(f'config_path: {Bot_temp.ConfigPath}')
    print(f'game_mode: {GameMode}')
    if GameMode == 'Simulação':
        print(f'saldo_inicial: {Bot_temp.GetConfig(["SaldoInicial"])}')
    print('\n\n[Lista de comandos]\n')
    print('> jogar')
    print('> game mode')
    print('> print config')
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
                            try:
                                test = open(input_txt, 'r')
                                Write(Paths, 'ConfigPath', input_txt)
                            except Exception as e:
                                print(f'\n   Erro ao abrir diretório: {e}\n')
                                time.sleep(1)
                                
                    Comando = 'pass'
                    inSetting = False
                case 'alterar saldo':
                    if GameMode == 'Simulação':
                        Write(Bot_temp.ConfigPath, 'SaldoInicial', input('Digite o valor que deseja: '))
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
                        newValue = 's'
                    case '2':
                        newValue = 'n'
                    case _:
                        print('\n    Erro: opção inválida\n')
            Write(Bot_temp.ConfigPath, 'Simulacao', newValue)
        case 'print config':
            print('\n\n\n')
            PrintCabecalho()
            Bot_temp.PrintConfig()
            print(input('\nDigite qualquer coisa para continuar: '))
        case 'quit':
            quit()
        case 'pass':
            pass
        case _:
            print('\n    Erro: comando inválido\n')
            time.sleep(1)
            

match GameMode:
    case 'Modo real':
        Bot = bot_class(Paths=Paths)
        Bot.driver.initialize_browser()
        Bot.EsperarLogin()
        Bot.EsperarLance()
        if Bot.Carteira.Saldo <=0:
            print('\n    Erro: saldo zerado, por favor, entre em uma conta que possua algum saldo disponível para jogar')
            time.sleep(1)
    case "Simulação":
        Bot = bot_class(Paths=Paths)
        Bot.driver.initialize_browser()
        Bot.EsperarLance()


while Bot.Carteira.Saldo > 0:
    Bot.RunCycle()
    if Bot.Carteira.Saldo > 0:
        if Bot.varRotina['ErrosIA_temp'] > 0:
            Bot.SetConfig(Bot.ConfigPath, key='Tipo_de_protecao', value='6')
        if Bot.varRotina['AcertosIA_temp'] > 0:
            Bot.SetConfig(Bot.ConfigPath, key='Tipo_de_protecao', value='5')

        if Lances.CountLances(10,[0]) > 0:
            Bot.SetConfig(Bot.ConfigPath, key='TaxaCor', value='ATK-0.5')
        else:
            Bot.SetConfig(Bot.ConfigPath, key='TaxaCor', value='ATK-0.1')

        Bot.PrintLog()
        Bot.PrintConfig()
        Bot.EsperarLance()
        Bot.PagarPremio(Lances.Get(1)[0])

sys.stderr.close()
sys.stderr = sys.__stderr__
