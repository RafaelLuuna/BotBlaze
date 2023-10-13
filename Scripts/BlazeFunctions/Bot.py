import sys
sys.path.append('C:/Users/rafael.luna/Desktop/docs pessoais/Projects/BotBlaze/BotBlaze/Scripts/BlazeFunctions/')

from chromeFunctions import driver_class
from collections import Counter
from termcolor import colored
from colorama import init, Fore, Style
init()

import keras
from keras.models import load_model
from keras.optimizers import Adagrad

import os
import time
import datetime
import Lances as Lances
import IA_Functions


class Carteira:

    arrCarteiras = []

    def __init__(self, Saldo=0, name=f'Carteira{len(arrCarteiras)}'):
        self.Saldo = Saldo
        self.SaldoInicial = Saldo
        self.Name = name
        self.arrCarteiras.append(self)
    
    def AddSaldo(self, Valor):
        self.Saldo += Valor

class Bot:

    arrBots = []


    def __init__(self, ConfigPath, Saldo=0, name=f'Bot{len(arrBots)}'):
        self.Carteira  = Carteira(Saldo, name)
        self.driver = driver_class()
        self.name = name
        self.ConfigPath = ConfigPath
        self.arrBots.append(self)

    def AtualizarVariaveis(self):
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
                        case 'ModelPath':
                            self.ModelPath = valor

        except FileNotFoundError:
            print("Arquivo de configuração não encontrado.")
        except Exception as e:
            print(f"Erro ao atualizar variáveis: {e}")

    def PagarPremio(self):
        LanceBlazeAtual = Lances.Get(1)[0]

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

        print('pagou:',ValorPremio)

    def CalcularAposta(self, Saldo, Meta, Muliplicador):
        ApostaAtual = round((Meta - Saldo)/Muliplicador+0.1,1)
        Carteira_temporaria = Saldo - (ApostaAtual)
        print('[Calculando aposta atual]')
        while(Carteira_temporaria + (ApostaAtual * Muliplicador) <= Meta):
            ApostaAtual = round((Meta - Carteira_temporaria)/Muliplicador+0.1,1)
            Carteira_temporaria = Saldo - (ApostaAtual)
        
        if ApostaAtual < 1:
            ApostaAtual = 1
        return ApostaAtual

    def Apostar(self):
        if self.TotalApostadoBranca > 0:
            self.Carteira.AddSaldo(-self.TotalApostadoBranca)
            if self.Simulacao == False:
                self.driver.incluir_aposta(self.TotalApostadoBranca)
                self.driver.selecionar_cor(0)
                self.driver.apostar(0)
        if self.TotalApostadoVermelha > 0:
            self.Carteira.AddSaldo(-self.TotalApostadoVermelha)
            if self.Simulacao == False:
                self.driver.incluir_aposta(self.TotalApostadoVermelha)
                self.driver.selecionar_cor(1)
                self.driver.apostar(1)
        if self.TotalApostadoPreta > 0:
            self.Carteira.AddSaldo(-self.TotalApostadoPreta)
            if self.Simulacao == False:
                self.driver.incluir_aposta(self.TotalApostadoPreta)
                self.driver.selecionar_cor(2)
                self.driver.apostar(2)

    def TreinarIA(self):
        LancesBlaze = Lances.Get(299, ReturnType='cor')
        train_x, val_x, train_y, val_y = IA_Functions.SepararTreinamento(input=LancesBlaze,input_size=self.LeituraMáximaDeLances, return_lst=['train_x','val_x', 'train_y', 'val_y'])
        
        Adagrad_optimizer = Adagrad(learning_rate=0.0004)
        self.model.compile(loss='mse', optimizer=Adagrad_optimizer, metrics=['accuracy'])
        self.model.fit(train_x, train_y, epochs=10,validation_data=(val_x,val_y))

    def IniciarRotina(self, modo='Live', lista_lances=[]):
        #Modo Live = ao vivo
        #Modo Simulation = carrega o históico (é preciso fornecer uma lista de lances no formato ['roll','color'])
        #-----------------------------------------------[ INICIALIZAÇÃO ]-----------------------------------------------#
        self.AtualizarVariaveis()
        match modo:
            case 'Live':
                UltimoLance = Lances.Get(1)[0]
                if self.Simulacao == False:
                    Holder = True
                    while Holder == True:
                        print(input('Faça login no site da blaze, depois, digite qualquer coisa no terminal para prosseguir: '))
                        Holder = False

            case 'List':
                pass

        ContagemAposta = 0
        NumTotalDeApostas = 0

        self.TotalApostado = 0
        self.TotalApostadoBranca = 0
        self.TotalApostadoVermelha = 0
        self.TotalApostadoPreta = 0
        self.PicoMaximo = self.Carteira.Saldo

        if (self.Simulacao == False):
            self.Carteira.Saldo = round(float(self.driver.get_saldo()))

        SaldoBase = self.Carteira.Saldo
        MetaAtual = SaldoBase + self.ConstMeta
        ApostaAtual = self.CalcularAposta(Saldo=SaldoBase, Meta=MetaAtual, Muliplicador=14)
        SaldoInicialRodada = self.Carteira.Saldo

        data = UltimoLance[2][:10].split('-')
        hora = UltimoLance[2][11:19].split(':')
        data = [int(i) for i in data]
        hora = [int(i) for i in hora]
        TempInicio = datetime.datetime(data[0],data[1],data[2],hora[0],hora[1],hora[2])


        self.model = load_model(self.ModelPath.replace('\\','/'))
        SugestaoIA = self.model.predict([Lances.Get(self.LeituraMáximaDeLances,ReturnType='cor')])[0]
        print('previsão da IA: ',Lances.ConverterCor(SugestaoIA,input_type='IA',output_type='string_ptbr'))
        AcertosIA_temp = 0
        ErrosIA_temp = 0
        self.AcertosIA = 0
        self.ErrosIA = 0
        print(self.Carteira.Saldo)
        #-----------------------------------------------[ ROTINA DO BOT ]-----------------------------------------------#
        while (self.Carteira.Saldo> 0):
            self.AtualizarVariaveis()
            LanceBlazeAtual = Lances.Get(1)[0]
            if (self.Simulacao == False):
                self.Carteira.Saldo = round(float(self.driver.get_saldo()))

            if not(UltimoLance == LanceBlazeAtual):
                UltimoLance = LanceBlazeAtual
                SugestaoIA_txt = Lances.ConverterCor(SugestaoIA,input_type='IA',output_type='string')

                if SugestaoIA_txt == LanceBlazeAtual[1]:
                    self.AcertosIA += 1
                    ErrosIA_temp = 0
                else:
                    self.ErrosIA += 1
                    AcertosIA_temp = 0
                print('[Lances atualizados] Lance blaze atual: ',LanceBlazeAtual)


                ContagemCores = Counter([item[1] for item in Lances.Get(self.LeituraMáximaDeLances)]).most_common()
                CorMaisComum = ContagemCores
                CorMenosComum = [i for i in reversed(ContagemCores)]
                CorMenosComum = CorMenosComum[0]
                CorMaisComum = CorMaisComum[0]

                if(self.TotalApostado > 0):
                    self.PagarPremio()

                
                if(self.Carteira.Saldo > self.PicoMaximo):
                    self.PicoMaximo = self.Carteira.Saldo
                
                print(f'SaldoInicial: {SaldoInicialRodada}, SaldoAtual: {self.Carteira.Saldo}')

                self.LucroPerda = self.Carteira.Saldo - self.Carteira.SaldoInicial
                LucroPerdaRodada = self.Carteira.Saldo - SaldoInicialRodada

                if (LucroPerdaRodada >= 0):
                    ContagemAposta = 0
                    CountPerdas = 0
                    SaldoBase = self.Carteira.Saldo
                else:
                    CountPerdas += 1 
                
                if(self.Carteira.Saldo >= MetaAtual):
                    ContagemAposta = 0
                    SaldoBase = self.Carteira.Saldo
                    MetaAtual = SaldoBase + self.ConstMeta

                if (self.PicoMaximo - self.MargemAposta > self.piso):
                    self.piso = self.PicoMaximo - self.MargemAposta
                    if self.piso < 0:
                        self.piso = 0
                

                if (self.Carteira.Saldo - ApostaAtual < self.piso):
                    while self.Carteira.Saldo - ApostaAtual < self.piso:
                        print(input('Piso atingido, digite qualquer coisa para continuar:'))
                        self.piso = self.Carteira.Saldo - self.MargemAposta

                # AcharTendencia()
                # if(AchouTendencia == True):
                #     AtualizarMeta(SaldoBase,ConstMeta*PesoTendencia)
                # else:
                #     AtualizarMeta(SaldoBase,ConstMeta)


                self.TotalApostado = 0
                self.TotalApostadoBranca = 0
                self.TotalApostadoVermelha = 0
                self.TotalApostadoPreta = 0
                SaldoInicialRodada = self.Carteira.Saldo


                if(self.DobrarMeta == True and ContagemAposta < self.QntLancesParaDobrar):
                    MetaAtual = SaldoBase + self.ConstMeta

                #-----------------------------------------------[ REGRAS DE APOSTA ]-----------------------------------------------#
            
                ApostaAtual = self.CalcularAposta(Saldo=self.Carteira.Saldo, Meta=MetaAtual, Muliplicador=14)

                if(ContagemAposta < self.Limite_Max_Apostas and self.Carteira.Saldo < self.Objetivo_final and self.Pausa == False):

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
                                CorNum = Lances.ConverterCor(LanceBlazeAtual[1])
                                if CorNum == 0:
                                    CorNum = CorMaisComum
                            case 5:
                                SugestaoIA = self.model.predict([Lances.Get(self.LeituraMáximaDeLances,ReturnType='cor')])[0]
                                CorNum = Lances.ConverterCor(SugestaoIA,input_type='IA', output_type='int')

                        #DEFINE O VALOR QUE VAI SER APOSTADO
                        if(not(CorNum == 0) and ErrosIA_temp < 2):
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

                    print('apostou:', self.TotalApostado, '[Branca: ', self.TotalApostadoBranca,' | Vermelha: ', self.TotalApostadoVermelha,' | Preta: ', self.TotalApostadoPreta,']')

                    ContagemAposta = ContagemAposta + 1

                    if self.OpcaoDeProtecao == 5:
                        self.TreinarIA()



                #-----------------------------------------------[ RESUMO E RELATÓRIO ]-----------------------------------------------#
                if len(self.arrBots) == 1:
                    NumTotalDeApostas = NumTotalDeApostas +1
                    print(LanceBlazeAtual)
                    data = LanceBlazeAtual[2][:10].split('-')
                    hora = LanceBlazeAtual[2][11:19].split(':')
                    data = [int(i) for i in data]
                    hora = [int(i) for i in hora]
                    TempFim = datetime.datetime(data[0],data[1],data[2],hora[0],hora[1],hora[2])
                    DeltaTempo = TempFim - TempInicio

                    #os.system('cls')

                    self.PrintLog(LanceBlazeAtual,NumTotalDeApostas,DeltaTempo,ContagemAposta,MetaAtual,CorMaisComum,SugestaoIA, LucroPerdaRodada)
                    # if(AchouTendencia == True):
                    #     PrintLog()
                    #     PrintTendencias()
                    Lances.PrintLances(30)
                    #listaDados = [LanceBlazeAtual[0][0],LanceBlazeAtual[1][0],TempFim,Carteira,MetaAtual,TotalApostadoBranca,TotalApostadoVermelha,TotalApostadoPreta,SugestaoIA['Output']]
                    #ImprimirLanceCSV(listaDados)
                    self.PrintConfig(SaldoBase)
                else:
                    os.system('cls')
                    print([i.Saldo for i in self.Carteira.arrCarteiras])
                
        else:
            print('[-----------------QUEBROU-----------------]')

    def PrintLog(self,LanceBlazeAtual, NumTotalDeApostas, DeltaTempo, ContagemAposta, MetaAtual, CorMaisComum, SugestaoIA, LucroPerdaRodada):
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
        print('lucro / perda no último lance:', colored(round(LucroPerdaRodada,2),Cor))
        match CorMaisComum:
            case 0:
                Cor = 'white'
            case 1:
                Cor = 'red'
            case 2:
                Cor = 'black' 
        if (self.AcertosIA+self.ErrosIA) == 0:
            TaxaAcertoIA = '0%'
        else:
            TaxaAcertoIA = f'{round(self.AcertosIA / (self.AcertosIA+self.ErrosIA) * 100,2)}%'
            
        print('Ultimo numero sorteado:', LanceBlazeAtual[0], ' | Cor mais comum:',Cor, ' | Sugestão IA: ', Lances.ConverterCor(SugestaoIA, input_type='IA', output_type='string_ptbr'), '(Taxa de acerto: ',TaxaAcertoIA,')')
        print('Brancas nos ultimos 20 lances: ',Lances.CountLances(20,[0]),' | A ultima branca foi a ', colored(Lances.LancesDepoisDaBranca(),'black','on_white'),'rodadas')
        print('__________________________________________________________________________')
        print('lances IA: ', Lances.Get(self.LeituraMáximaDeLances,Values=['roll']))

    def PrintConfig(self, SaldoBase):
        print('\n-----------------------------[CONFIGURAÇÕES DO BOT]-----------------------------')

        print('\nSaldo inical: ', self.Carteira.SaldoInicial)
        print('Saldo base atual: ', SaldoBase)
        print('Maior saldo até o momento: ',self.PicoMaximo)
        print('Objetivo: ',self.Objetivo_final)
        
        print('\nConst. da meta atual: ', self.ConstMeta)

        print('\nLeitra maxima de lances: ',self.LeituraMáximaDeLances)

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
        print('Opcao de protecao: ',txtOpcaoProtecao)
        print('Taxa Cor:' , self.TaxaCor)

        print('\nDobrar meta: ',self.DobrarMeta)
        if self.DobrarMeta == True:
            print('Lances dobrados: ', self.QntLancesParaDobrar)

        print('Modo Simulacao: ',self.Simulacao)

        print('Modelo IA: ', self.ModelPath)

        print('\n----------------------------------------------------------------------------------')


BotTeste = Bot('C:/Users/rafael.luna/Desktop/docs pessoais/Projects/BotBlaze/BotBlaze/Scripts/Config.txt', Saldo=1000)
BotTeste.IniciarRotina()

