
from chromeFunctions import driver_class
from collections import Counter
import Lances

class Carteira:

    arrCarteiras = []

    def __init__(self, Saldo=0, name=f'Carteira{len(arrCarteiras)}'):
        self.Saldo = Saldo
        self.SaldoInicial = Saldo
        self.Name = name
        self.arrCarteiras.append(self)
    
    def AddSaldo(self, Valor):
        self.Saldo += Valor

    def SetSaldo(self, Valor):
        self.Saldo = Valor

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
        LanceBlazeAtual = Lances.Get(1)

        ValorPremio = 0
        if(LanceBlazeAtual[1] == [0]):
            ValorPremio = round(self.TotalApostadoBranca * 14, 2)
        if(LanceBlazeAtual[1] == [1]):
            ValorPremio = round(self.TotalApostadoVermelha * 2, 2)
        if(LanceBlazeAtual[1] == [2]):
            ValorPremio = round(self.TotalApostadoPreta * 2, 2)
        Carteira = round(Carteira + ValorPremio, 2)

        self.TotalApostadoBranca = 0
        self.TotalApostadoVermelha = 0
        self.TotalApostadoPreta = 0

        print('pagou:',ValorPremio)

    def IniciarRotina(self, Modo='Live', NumLances=[]):
        #Modo Live = ao vivo
        #Modo Simulation = carrega o históico (é preciso fornecer uma lista de lances no formato ['roll','color'])
        #-----------------------------------------------[ INICIALIZAÇÃO ]-----------------------------------------------#
        self.AtualizarVariaveis()
        UltimoLance = Lances.Get(1)
        self.driver.initialize_browser()
        while (self.Carteira.Saldo> 0):
        #-----------------------------------------------[ ROTINA DO BOT ]-----------------------------------------------#
            self.AtualizarVariaveis()
            LanceBlazeAtual = Lances.Get(1)
            ContagemAposta = 0
            SaldoBase = self.Carteira.Saldo
            MetaAtual = SaldoBase + self.ConstMeta

            if not(UltimoLance == LanceBlazeAtual):
                UltimoLance = LanceBlazeAtual
                print('[Lances atualizados] Lance blaze atual: ',LanceBlazeAtual)

                self.SaldoInicialRodada = self.Carteira.Saldo
                
                # if self.OpcaoDeProtecao == 5:
                #     PredictIA()

                if (self.Simulacao == False):
                    self.Carteira.SetSaldo = round(float(self.driver.get_saldo()))

                CorMaisComum = Counter([item[1] for item in Lances.Get(self.LeituraMáximaDeLances)]).most_common()
                CorMenosComum = CorMenosComum[len(CorMaisComum)][0]
                CorMaisComum = CorMaisComum[0][0]

                if(self.TotalApostado > 0):
                    self.PagarPremio()


                if(self.Carteira.Saldo > self.PicoMaximo):
                    self.PicoMaximo = self.Carteira.Saldo

                self.LucroPerda = self.Carteira.SaldoInicial - self.Carteira.Saldo
                self.LucroPerdaRodada = self.SaldoInicialRodada - self.Carteira.Saldo


                if (self.LucroPerdaRodada >= 0):
                    ContagemAposta = 0
                    CountPerdas = 0
                    SaldoBase = Carteira
                else:
                    CountPerdas = CountPerdas + 1 
                
                if(self.Carteira.Saldo >= MetaAtual):
                    ContagemAposta = 0
                    SaldoBase = self.Carteira.Saldo
                    MetaAtual = SaldoBase + self.ConstMeta

                if (self.PicoMaximo - self.MargemAposta > piso):
                    self.piso = self.PicoMaximo - self.MargemAposta
                    if self.piso < 0:
                        self.piso = 0
                

                if (self.Carteira.Saldo - ApostaAtual < piso):
                    while self.Carteira.Saldo - ApostaAtual < piso:
                        print(input('Piso atingido, digite qualquer coisa para continuar:'))
                        piso = self.Carteira.Saldo - self.MargemAposta


                
                #-----------------------------------------------[ REGRAS DE APOSTA ]-----------------------------------------------#
                self.TotalApostado = 0
                self.TotalApostadoBranca = 0
                self.TotalApostadoVermelha = 0
                self.TotalApostadoPreta = 0

                # AcharTendencia()
                # if(AchouTendencia == True):
                #     AtualizarMeta(SaldoBase,ConstMeta*PesoTendencia)
                # else:
                #     AtualizarMeta(SaldoBase,ConstMeta)

                if(self.DobrarMeta == True and ContagemAposta < self.QntLancesParaDobrar):
                    MetaAtual = SaldoBase + self.ConstMeta

                ApostaAtual = round((MetaAtual - self.Carteira.Saldo)/14+0.1,1)
                Carteira_temporaria = self.Carteira.Saldo - (ApostaAtual*2)
                print('[Calculando aposta atual]')
                while(Carteira_temporaria + (ApostaAtual * 14) <= self.MetaAtual):
                    ApostaAtual = round((MetaAtual - Carteira_temporaria)/14+0.1,1)
                    Carteira_temporaria = Carteira - (ApostaAtual*2) - (ApostaAtual*TaxaCor)

                
                if(ContagemAposta < Limite_Max_Apostas and Carteira < Objetivo_final and Pausa == False):

                    if(ModoAtaque == False):
                        IncluirAposta(ApostaAtual,0)
                        Apostar(0)

                    print('apostou:',TotalApostado, '[Branca: ',TotalApostadoBranca,' | Vermelha: ',TotalApostadoVermelha,' | Preta: ',TotalApostadoPreta,']')

                    if(SalvarNaCor == True):
                        CorNum = 0
                        match OpcaoDeProtecao:
                            case 1:
                                CorNum = CorMaisComum
                            case 2:
                                CorNum = CorMenosComum
                            case 3:
                                if(len(LancesDepoisDaBranca)<5):
                                    CorNum = CorMaisComum
                                else:
                                    CorNum = CorMenosComum
                            case 4:
                                CorNum = LanceBlazeAtual[1][0]
                                if CorNum == 0:
                                    CorNum = CorMaisComum
                            case 5:
                                CorNum = SugestaoIA['cor']

                        if(not(CorNum == 0) and ErrosIA_temp < 2):
                            if(ModoAtaque == True):

                                AtualizarMeta(Carteira, ConstMeta)
                                ApostaCor = ConstMeta

                                IncluirAposta(ConstMeta * TaxaBranca_ModoAtaque,0)
                                Apostar(0)
                                
                            else:
                                if(ApostaAtual + (ApostaAtual*TaxaCor) < 5):
                                    ApostaCor = 5
                                else:
                                    ApostaCor = ApostaAtual + (ApostaAtual*TaxaCor)
                                    
                            IncluirAposta(ApostaCor,CorNum)
                            Apostar(CorNum)
                            print('apostou:',TotalApostado, '[Branca: ',TotalApostadoBranca,' | Vermelha: ',TotalApostadoVermelha,' | Preta: ',TotalApostadoPreta,']')



                    ContagemAposta = ContagemAposta + 1

                #-----------------------------------------------[ RESUMO E RELATÓRIO ]-----------------------------------------------#

                NumTotalDeApostas = NumTotalDeApostas +1

                TempFim = datetime.datetime(int(str(LanceBlazeAtual[2])[2:6]),int(str(LanceBlazeAtual[2])[7:9]),int(str(LanceBlazeAtual[2])[10:12]),int(str(LanceBlazeAtual[2])[13:15]),int(str(LanceBlazeAtual[2])[16:18]),int(str(LanceBlazeAtual[2])[19:21]))
                DeltaTempo = TempFim - TempInicio

                TreinarIA(10)

                os.system('cls')

                PrintLog()
                # if(AchouTendencia == True):
                #     PrintLog()
                #     PrintTendencias()
                PrintLances(ListagemDeLances_Limite)
                listaDados = [LanceBlazeAtual[0][0],LanceBlazeAtual[1][0],TempFim,Carteira,MetaAtual,TotalApostadoBranca,TotalApostadoVermelha,TotalApostadoPreta,SugestaoIA['Output']]
                ImprimirLanceCSV(listaDados)
                PrintConfig()
                
        else:
            print('[-----------------QUEBROU-----------------]')



BotTeste = Bot('C:/Users/rafael.luna/Desktop/docs pessoais/Projects/BotBlaze/BotBlaze/Scripts/Config.txt', Saldo=1000)
BotTeste.IniciarRotina()