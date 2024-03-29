import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from icecream import ic
from chromeFunctions import driver_class
from collections import Counter
from termcolor import colored
from colorama import init, Fore, Style
init()

import keras
from keras.models import load_model
from keras.optimizers import Adagrad


import time
import datetime
import Lances as Lances
import IA_Functions

import json


class Carteira:

    arrCarteiras = []

    def __init__(self, Saldo=0, name=f'Carteira{len(arrCarteiras)}'):
        self.Saldo = Saldo
        self.SaldoInicial = Saldo
        self.Name = name
        self.arrCarteiras.append(self)
    
    def AddSaldo(self, Valor):
        self.Saldo += Valor

class bot_class:


    def __init__(self, Paths, name='Bot'):
        self.driver = driver_class()
        self.name = name
        self.Paths = Paths
        self.UpdateConfig()
        self.Carteira  = Carteira(float(self.GetConfig(['SaldoInicial'])), name)
        self.Cycle = 0
        self.varRotina = {
            'NumTotalDeApostas':0,
            'DeltaTempo':0,
            'ContagemAposta':0,
            'MetaAtual':0,
            'LucroPerdaRodada':0,
            'CorMaisComum':0,
            'AcertosIA':0,
            'ErrosIA':0,
            'LanceBlazeAtual':Lances.Get(1)[0],
            'SugestaoIA':[0,0],
            'ApostaAtual':0,
            'ErrosIA_temp':0,
            'AcertosIA_temp':0,
            'CountPerdas':0,
            'TempInicio':0,
            'SaldoBase':0,
            'SaldoInicialRodada':0
        }

    def EsperarLance(self):
        LanceBlazeAtual = Lances.Get(1)[0]
        UltimoLance = LanceBlazeAtual
        while UltimoLance == LanceBlazeAtual:
            LanceBlazeAtual = Lances.Get(1)[0]

    def EsperarLogin(self):
        #QUANDO NÃO DETECTAR O SALDO, PEDIRÁ PARA FAZER LOGIN
        if self.driver.get_saldo() == 'Saldo não localizado':
            print('[Saldo não detectado, aguardando login na plataforma]')
            while self.driver.get_saldo() == 'Saldo não localizado':
                pass
        print('[Saldo localizado]')

    def SetConfig(self, FilePath, key, value):
        with open(FilePath, 'r') as arquivo:
            Linhas = arquivo.readlines()
            for i, linha in enumerate(Linhas):
                chave, valor = linha.strip().split('=')
                if chave == key:
                    Linhas[i] = key + '=' + value + '\n'
        with open(FilePath, 'w') as arquivo:
            arquivo.writelines(Linhas)
            arquivo.flush()

    def GetConfig(self, Values):
        Output = {}
        if not(type(Values) is list):
            print("Erro: O parâmetro 'Values' precisa ser do tipo 'list'. Foi retornado um dicionário vazio.")
        else:
            try:
                with open(self.ConfigPath,'r') as arquivo:
                    linhas = arquivo.readlines()
                    for linha in linhas:
                        chave, valor = linha.strip().split('=')
                        if chave in Values:
                            Output.update({chave:valor})

            except FileNotFoundError:
                print("Arquivo de configuração não encontrado.")
            except Exception as e:
                print(f"Erro ao atualizar variáveis: {e}")
            if len(Output) == 1:
                Output = next(iter(Output.values()))
        return Output

    def UpdateConfig(self):
        with open(self.Paths, 'r') as arquivo:
            Linhas = arquivo.readlines()
            for linha in Linhas:
                chave, valor = linha.strip().split('=')
                match chave:
                    case 'ConfigPath':
                        self.ConfigPath = valor
                    case 'ModelPath':
                        self.ModelPath = valor
        try:
            with open(self.ConfigPath,'r') as arquivo:
                linhas = arquivo.readlines()
                for linha in linhas:
                    chave, valor = linha.strip().split('=')
                    match chave:
                        case 'Simulacao':
                            if(valor == 's'):
                                self.Simulacao = True
                            elif(valor == 'n'):
                                self.Simulacao = False
                        case 'Objetivo_final':
                            self.Objetivo_final = int(valor)
                        case 'Const_meta':
                            self.ConstMeta = int(valor)
                        case 'leitura_Maxima_de_lances':
                            self.LeituraMáximaDeLances = int(valor)
                        case 'Limite_de_apostas':
                            self.Limite_Max_Apostas = int(valor)
                        case 'Margem_de_apostas':
                            self.MargemAposta = int(valor)
                        case 'Piso':
                            self.piso = int(valor)
                        case 'Protecao_na_cor':
                            if(valor == 's'):
                                self.SalvarNaCor = True
                            elif(valor == 'n'):
                                self.SalvarNaCor = False
                        case 'Tipo_de_protecao':
                            self.OpcaoDeProtecao = int(valor)
                        case 'Dobrar_meta':
                            if(valor == 's'):
                                self.DobrarMeta = True
                            elif(valor == 'n'):
                                self.DobrarMeta = False
                        case 'Lances_dobrados':
                            self.QntLancesParaDobrar = int(valor)
                        case 'TaxaCor':
                            if(valor[:3] == 'ATK'):
                                self.ModoAtaque = True
                                self.TaxaCor = 0
                                self.TaxaBranca_ModoAtaque = float(valor[4:])
                            else:
                                self.ModoAtaque = False
                                self.TaxaCor = float(valor)
                        case 'Pausa':
                            if(valor == 's'):
                                self.Pausa = True
                            elif(valor == 'n'):
                                self.Pausa = False

        except FileNotFoundError:
            print("Arquivo de configuração não encontrado.")
        except Exception as e:
            print(f"Erro ao atualizar variáveis: {e}")

    def PagarPremio(self, LanceBlazeAtual, PrintLog=True):
        
        if PrintLog == True:
            print(f'\nApostado: Branca={self.TotalApostadoBranca} , Vermelha={self.TotalApostadoVermelha} , Preta={self.TotalApostadoPreta}')
            print(f'Blaze sorteou: {LanceBlazeAtual[1]}')

        ValorPremio = 0
        if(LanceBlazeAtual[1] == 'white'):
            ValorPremio = round(self.TotalApostadoBranca * 14, 2)
        if(LanceBlazeAtual[1] == 'red'):
            ValorPremio = round(self.TotalApostadoVermelha * 2, 2)
        if(LanceBlazeAtual[1] == 'black'):
            ValorPremio = round(self.TotalApostadoPreta * 2, 2)
        
        self.Carteira.AddSaldo(ValorPremio)

        self.TotalApostadoBranca = 0
        self.TotalApostadoVermelha = 0
        self.TotalApostadoPreta = 0

        SaldoInicialRodada = self.varRotina['SaldoInicialRodada']

        LucroPerdaRodada = self.Carteira.Saldo - SaldoInicialRodada
        self.varRotina['LucroPerdaRodada'] = LucroPerdaRodada

        if (LucroPerdaRodada > 0):
            self.varRotina['ContagemAposta'] = 0
            self.varRotina['CountPerdas'] = 0
            self.varRotina['SaldoBase'] = self.Carteira.Saldo
        else:
            self.varRotina['CountPerdas'] += 1 
        
        SugestaoIA_txt = Lances.Converter.Cor(self.varRotina['SugestaoIA'],input_type='IA',output_type='string')

        if SugestaoIA_txt == LanceBlazeAtual[1]:
            self.varRotina['AcertosIA'] += 1
            self.varRotina['AcertosIA_temp'] += 1
            self.varRotina['ErrosIA_temp'] = 0
        else:
            self.varRotina['ErrosIA'] += 1
            self.varRotina['ErrosIA_temp'] += 1
            self.varRotina['AcertosIA_temp'] = 0
        if PrintLog == True:
            print('Pagou:',ValorPremio)

    def CalcularAposta(self, Saldo, Meta, Muliplicador, PrintLog=True):
        ApostaAtual = round((Meta - Saldo)/Muliplicador+0.1,1)
        Carteira_temporaria = Saldo - (ApostaAtual)
        if PrintLog == True:
            print('[Calculando aposta atual]')
        while(Carteira_temporaria + (ApostaAtual * Muliplicador) <= Meta):
            ApostaAtual = round((Meta - Carteira_temporaria)/Muliplicador+0.1,1)
            Carteira_temporaria = Saldo - (ApostaAtual)
        
        if ApostaAtual < 1:
            ApostaAtual = 1
        return ApostaAtual

    def Apostar(self):
        if self.Simulacao == False:
            if self.TotalApostadoBranca > 0:
                    self.driver.apostar(0,self.TotalApostadoBranca)
            if self.TotalApostadoVermelha > 0:
                    self.driver.apostar(1,self.TotalApostadoVermelha)
            if self.TotalApostadoPreta > 0:
                    self.driver.apostar(2,self.TotalApostadoPreta)
        self.Carteira.AddSaldo(-self.TotalApostado)


    def TreinarIA(self, num_lances, epochs=10, learning_rate=0.01):
        LancesBlaze = Lances.Get(num_lances, ReturnType='cor')
        train_x, train_y = IA_Functions.SepararTreinamento(input=LancesBlaze,input_size=self.LeituraMáximaDeLances, return_lst=['train_x', 'train_y'])
        
        Adagrad_optimizer = Adagrad(learning_rate=learning_rate)
        self.model.compile(loss='mse', optimizer=Adagrad_optimizer, metrics=['accuracy'])
        self.model.fit(train_x, train_y, epochs=epochs)

        self.model.save(self.ModelPath)

    def RunCycle(self, LanceBlazeAtual=Lances.Get(1)[0], Condicoes=True, PrintLog=True, IA_list=[]):
        #-----------------------------------------------[ INICIALIZAÇÃO ]-----------------------------------------------#
        self.UpdateConfig()

        self.varRotina['LanceBlazeAtual'] = LanceBlazeAtual
        if PrintLog == True:
            print('----------------------------------------------------------------------------------')
            print('[Lances atualizados] Lance blaze atual: ',LanceBlazeAtual)

        #QUANDO NÃO DETECTAR O SALDO, PEDIRÁ PARA FAZER LOGIN
        if self.Simulacao == False:
            if self.driver.get_saldo() == 'Saldo não localizado':
                while self.driver.get_saldo() == 'Saldo não localizado':
                    print(input('Faça login no site da blaze, depois, pressione a tecla [enter] no terminal para prosseguir: '))
            self.Carteira.Saldo = round(float(self.driver.get_saldo()))

        if self.Cycle == 0:
            if self.Simulacao == False:
                self.Carteira.SaldoInicial = self.Carteira.Saldo
            
            self.varRotina['LanceBlazeAtual'] = LanceBlazeAtual
            
            data = LanceBlazeAtual[2][:10].split('-')
            hora = LanceBlazeAtual[2][11:19].split(':')
            data = [int(i) for i in data]
            hora = [int(i) for i in hora]
            TempInicio = datetime.datetime(data[0],data[1],data[2],hora[0],hora[1],hora[2])
            
            ContagemAposta = 0
            NumTotalDeApostas = 0
            CountPerdas = 0
            ApostaAtual = 0

            self.TotalApostado = 0
            self.TotalApostadoBranca = 0
            self.TotalApostadoVermelha = 0
            self.TotalApostadoPreta = 0
            self.PicoMaximo = self.Carteira.Saldo



            SaldoBase = self.Carteira.Saldo
            MetaAtual = SaldoBase + self.ConstMeta
            SaldoInicialRodada = self.Carteira.Saldo
            LucroPerdaRodada = 0


            AcertosIA = 0
            ErrosIA = 0
            AcertosIA_temp = 0
            ErrosIA_temp = 0
            self.model = load_model(self.ModelPath.replace('\\','/'))
            self.Cycle += 1

            if PrintLog == True:
                print('[First cycle complete]')
        else:
            NumTotalDeApostas = self.varRotina['NumTotalDeApostas']
            DeltaTempo = self.varRotina['DeltaTempo']
            ContagemAposta = self.varRotina['ContagemAposta']
            MetaAtual = self.varRotina['MetaAtual']
            LucroPerdaRodada = self.varRotina['LucroPerdaRodada']
            CorMaisComum = self.varRotina['CorMaisComum']
            AcertosIA = self.varRotina['AcertosIA']
            ErrosIA = self.varRotina['ErrosIA']
            SugestaoIA = self.varRotina['SugestaoIA']
            ApostaAtual = self.varRotina['ApostaAtual']
            ErrosIA_temp = self.varRotina['ErrosIA_temp']
            AcertosIA_temp = self.varRotina['AcertosIA_temp']
            CountPerdas = self.varRotina['CountPerdas']
            TempInicio = self.varRotina['TempInicio']
            SaldoBase = self.varRotina['SaldoBase']
            SaldoInicialRodada = self.varRotina['SaldoInicialRodada']


        if len(IA_list) == 0:
            IA_list = [Lances.Get(self.LeituraMáximaDeLances,ReturnType='cor')]

        if self.OpcaoDeProtecao == 5 or self.OpcaoDeProtecao == 6:
            SugestaoIA = self.model.predict(IA_list)[0]
        
        #-----------------------------------------------[ ROTINA DO BOT ]-----------------------------------------------#
        if self.Carteira.Saldo > 0:

            


            ContagemCores = Counter([item[1] for item in Lances.Get(self.LeituraMáximaDeLances)]).most_common()
            CorMaisComum = ContagemCores
            CorMenosComum = [i for i in reversed(ContagemCores)]
            CorMenosComum = CorMenosComum[0]
            CorMaisComum = CorMaisComum[0]


            SaldoInicialRodada = self.Carteira.Saldo
            
            if(self.Carteira.Saldo > self.PicoMaximo):
                self.PicoMaximo = self.Carteira.Saldo
            
            
            if(self.Carteira.Saldo >= MetaAtual):
                ContagemAposta = 0
                SaldoBase = self.Carteira.Saldo
                MetaAtual = SaldoBase + self.ConstMeta

            if (self.PicoMaximo - self.MargemAposta > self.piso):
                self.piso = self.PicoMaximo - self.MargemAposta
                if self.piso < 0:
                    self.piso = 0
            


            # AcharTendencia()
            # if(AchouTendencia == True):
            #     AtualizarMeta(SaldoBase,ConstMeta*PesoTendencia)
            # else:
            #     AtualizarMeta(SaldoBase,ConstMeta)


            self.TotalApostado = 0
            self.TotalApostadoBranca = 0
            self.TotalApostadoVermelha = 0
            self.TotalApostadoPreta = 0


            if(self.DobrarMeta == True and ContagemAposta < self.QntLancesParaDobrar):
                MetaAtual = SaldoBase + self.ConstMeta

            #-----------------------------------------------[ REGRAS DE APOSTA ]-----------------------------------------------#
            if self.ModoAtaque == False:
                ApostaAtual = self.CalcularAposta(Saldo=self.Carteira.Saldo, Meta=MetaAtual, Muliplicador=14)



            if(self.Carteira.Saldo < self.Objetivo_final and self.Pausa == False and self.Carteira.Saldo - ApostaAtual > self.piso and Condicoes == True):
                self.TotalApostadoBranca = ApostaAtual
                if(self.SalvarNaCor == True):
                    #DEFINE A OPÇÃO SELECIONADA
                    CorNum = 0
                    match self.OpcaoDeProtecao:
                        case 1:
                            CorNum = CorMaisComum
                        case 2:
                            CorNum = CorMenosComum
                        case 3:
                            if(Lances.LancesDepoisDaBranca()<5):
                                CorNum = CorMaisComum
                            else:
                                CorNum = CorMenosComum
                        case 4:
                            CorNum = Lances.Converter.Cor(LanceBlazeAtual[1])
                            if CorNum == 0:
                                CorNum = CorMaisComum
                        case 5:
                            CorNum = Lances.Converter.Cor(SugestaoIA,input_type='IA', output_type='int')
                        case 6:
                            CorNum = Lances.Converter.Cor(SugestaoIA,input_type='IA', output_type='int')
                            if CorNum == 1:
                                CorNum = 2
                            elif CorNum == 2:
                                CorNum = 1

                    #DEFINE O VALOR QUE VAI SER APOSTADO
                    if(not(CorNum == 0)):
                        if(self.ModoAtaque == True):
                            ApostaCor = self.ConstMeta
                            self.TotalApostadoBranca = ApostaCor * self.TaxaBranca_ModoAtaque                                
                        else:
                            if(ApostaAtual + (ApostaAtual*self.TaxaCor) < 5):
                                ApostaCor = 5
                            else:
                                ApostaCor = ApostaAtual + (ApostaAtual*self.TaxaCor)
                    
                        match CorNum:
                            case 1:
                                self.TotalApostadoVermelha = ApostaCor
                            case 2:
                                self.TotalApostadoPreta = ApostaCor
                
                self.TotalApostado = self.TotalApostadoBranca + self.TotalApostadoVermelha + self.TotalApostadoPreta
                self.Apostar()

                if PrintLog == True:
                    print('apostou:', self.TotalApostado, '[Branca: ', self.TotalApostadoBranca,' | Vermelha: ', self.TotalApostadoVermelha,' | Preta: ', self.TotalApostadoPreta,']')
                    print(f'SaldoInicial: {SaldoInicialRodada}, SaldoAtual: {self.Carteira.Saldo}')

                ContagemAposta = ContagemAposta + 1


            self.LucroPerda = self.Carteira.Saldo - self.Carteira.SaldoInicial


            #-----------------------------------------------[ RESUMO E RELATÓRIO ]-----------------------------------------------#
            NumTotalDeApostas = NumTotalDeApostas +1


            data = LanceBlazeAtual[2][:10].split('-')
            hora = LanceBlazeAtual[2][11:19].split(':')
            data = [int(i) for i in data]
            hora = [int(i) for i in hora]
            TempFim = datetime.datetime(data[0],data[1],data[2],hora[0],hora[1],hora[2])
            DeltaTempo = TempFim - TempInicio

            self.varRotina = {
                'NumTotalDeApostas':NumTotalDeApostas,
                'DeltaTempo':DeltaTempo,
                'ContagemAposta':ContagemAposta,
                'MetaAtual':MetaAtual,
                'LucroPerdaRodada':LucroPerdaRodada,
                'CorMaisComum':CorMaisComum,
                'AcertosIA':AcertosIA,
                'ErrosIA':ErrosIA,
                'LanceBlazeAtual':LanceBlazeAtual,
                'SugestaoIA':SugestaoIA,
                'ApostaAtual':ApostaAtual,
                'ErrosIA_temp':ErrosIA_temp,
                'AcertosIA_temp':AcertosIA_temp,
                'CountPerdas':CountPerdas,
                'TempInicio':TempInicio,
                'SaldoBase':SaldoBase,
                'SaldoInicialRodada':SaldoInicialRodada
            }
        else:
            if PrintLog == True:
                print('[-----------------QUEBROU-----------------]')

    def PrintLog(self):
        NumTotalDeApostas = self.varRotina['NumTotalDeApostas']
        DeltaTempo = self.varRotina['DeltaTempo']
        ContagemAposta = self.varRotina['ContagemAposta']
        MetaAtual = self.varRotina['MetaAtual']
        LucroPerdaRodada = self.varRotina['LucroPerdaRodada']
        CorMaisComum = self.varRotina['CorMaisComum']
        AcertosIA = self.varRotina['AcertosIA']
        ErrosIA = self.varRotina['ErrosIA']
        LanceBlazeAtual = self.varRotina['LanceBlazeAtual']
        SugestaoIA = self.varRotina['SugestaoIA']

        CorSaldo = 'green'
        if(self.Carteira.Saldo < self.Carteira.SaldoInicial):
            CorSaldo = 'red'
        print('__________________________________________________________________________')
        print('#',NumTotalDeApostas,' | Tempo de jogo:', DeltaTempo)
        print('Num. apostas: ', ContagemAposta)
        print('Saldo atual:', colored(self.Carteira.Saldo,CorSaldo))
        print('Valor apostado:', self.TotalApostado, colored('[Branca: ','black','on_white'),self.TotalApostadoBranca,colored(' | Vermelha: ','white','on_red'),self.TotalApostadoVermelha,colored(' | Preta: ','white','on_black'),self.TotalApostadoPreta,colored(']','white','on_black'))
        print('Meta atual:', colored(MetaAtual,'blue'),' | Piso: ', self.piso)
        if(LucroPerdaRodada>0):
            Cor = 'green'
        else:
            Cor = 'red'
        print('lucro / perda no último lance:', colored(round(LucroPerdaRodada,2),Cor), end="")
        if(self.LucroPerda>0):
            Cor = 'green'
        else:
            Cor = 'red'
        print(' | lucro / perda geral:', colored(round(self.LucroPerda,2),Cor))
        if (AcertosIA+ErrosIA) == 0:
            TaxaAcertoIA = '0%'
        else:
            TaxaAcertoIA = f'{round(AcertosIA / (AcertosIA+ErrosIA) * 100,2)}%'
            
        print('Ultimo numero sorteado:', LanceBlazeAtual[0], ' | Cor mais comum:',CorMaisComum, ' | Sugestão IA: ', Lances.Converter.Cor(SugestaoIA, input_type='IA', output_type='string_ptbr'), '(Taxa de acerto: ',TaxaAcertoIA,')')
        print('Brancas nos ultimos 20 lances: ',Lances.CountLances(20,[0]),' | A ultima branca foi a ', colored(Lances.LancesDepoisDaBranca(),'black','on_white'),'rodadas')
        print('__________________________________________________________________________')
        print('lances IA: ', Lances.Get(self.LeituraMáximaDeLances,Values=['roll']))

    def PrintConfig(self):
        SaldoBase = self.varRotina['SaldoBase']

        print('\n-----------------------------[CONFIGURAÇÕES DO BOT]-----------------------------')

        print('\nSaldo inical: ', self.Carteira.SaldoInicial)
        print('Saldo base atual: ', SaldoBase)
        print('Maior saldo até o momento: ',self.PicoMaximo)
        print('Objetivo: ',self.Objetivo_final)
        
        print('\nConst. da meta atual: ', self.ConstMeta)

        print('\nLeitura maxima de lances: ',self.LeituraMáximaDeLances)

        print('\nLimite maximo de apostas:',self.Limite_Max_Apostas)
        print('Margem para apostas: ',self.MargemAposta)

        print('\nProtecao na cor: ',self.SalvarNaCor )
        match self.OpcaoDeProtecao:
            case 1:
                txtOpcaoProtecao = '1 - Apostar na cor mais frequente'
            case 2:
                txtOpcaoProtecao = '2 - Apostar na cor menos frequente'
            case 3:
                txtOpcaoProtecao = '3 - Apostar na mais frequente apeneas nas 5 primeiras rodadas, depois disso, apostar na menos frequente'
            case 4:
                txtOpcaoProtecao = '4 - Repetir a última cor'
            case 5:
                txtOpcaoProtecao = '5 - Sugestão da IA'
            case 6:
                txtOpcaoProtecao = '6 - Sugestão da IA invertida'
        print('Opcao de protecao: ',txtOpcaoProtecao)
        print('Taxa Cor:' , self.TaxaCor)

        print('\nDobrar meta: ',self.DobrarMeta)
        if self.DobrarMeta == True:
            print('Lances dobrados: ', self.QntLancesParaDobrar)

        print('Modo Simulacao: ',self.Simulacao)

        print('Modelo IA: ', self.ModelPath)

        print('\n----------------------------------------------------------------------------------')
