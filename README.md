# Projeto de automação de apostas (em progresso..)

Este projeto é um desafio pessoal que tem como objetivo criar um robô capaz de jogar sozinho no jogo double da Blaze. Todos as técnicas/tecnologias usadas nesse projeto foram aprendidas através de muita pesquisa, esforço e dedicação.

## Principais aprendizados:
* O que são ambientes virtuais e como trabalhar com eles;
* Sintaxe da linguagem Python (esse foi meu primeiro conato com a linguagem);
* A importância da organização no código (Criar funções especializadas facilitam muito a manutenção e leitura do código);
* Conhecimento básico de IA (Funcionamento dos neurônios, funções de ativação, optimizadores, técnicas de treinamento, etc..);
* Trabalhar com as bibliotecas keras e numpy.
* Tratamento de listas e arrays (Principalmente para trabalhar com IA).
* Exercício do pensamento de programação orientada à objetos.

## Funcionamento geral do robô de apostas.
> [!WARNING]
> Este é um projeto de estudo, não me responsabilizo por quaisquer prejuízos consequêntes do uso deste código. Use-o com sabedoria.

O robô é capaz de simular uma rodada ao vivo do jogo Double (https://blaze-4.com/pt/games/double) seguindo uma rotina que está pré-definida no script .\Scripts\BlazeFunctions\Bot.py. 

Dentro deste script há uma classe chamada 'bot_class', esta classe contém todas as variáveis e funções que o robô precisa para funcionar corretamente.

Para usar o robô, basta importar a classe 'bot_class' fornecendo um diretório de um arquivo de configuração e depois atribuir essa classe à uma variável que representará seu bot, por exemplo:

```python
from Scripts.BlazeFunctions.Bot import bot_class

Bot = bot_class('./Config.txt')
```

Agora você pode usar o comando 'Bot.RunRotina()' para executar um ciclo da rotina que está pré-definida no código do bot.

De modo geral, em um ciclo da rotina do bot ele executa as seguintes etapas:
1. Prepara as variáveis para registrar saldo, valor apostado, últimos lances, etc...
2. Aguarda o próximo lance ser sorteado pela Blaze (para evitar de começar a rotina no meio de uma rodada que já está em andamento).
3. Paga os prêmios da rodada de acordo com o total apostado na rodada anterior.
4. Escolhe uma cor para apostar (de acordo com os parâmetros do arquivo 'Config.txt').
5. Por fim, apostar nas cores escolhidas.

O comando 'Bot.RunRotina()' executa essa rotina apenas uma vez, portanto, para que o bot aposte várias vezes em sequência, é preciso usar este comando em conjunto há um loop ou á alguma outra condição que faça ele apostar várias vezes, por exemplo:

```python
#Desse modo a rotina é sempre executada enquanto o saldo da carteira do bot for maior que 0
while Bot.Carteira.Saldo > 0:
    Bot.RunRotina()
```
Outro comando importante é o 'Bot.driver.initialize_browser()', ele abre uma janela do chromedriver já na página do double para você conseguir acompanhar os lances ao vivo. 

Caso eseja usando o robô com a opção de simulação desativada, é obrigatório o uso do comando 'Bot.driver.initialize_browser()' antes do início da sua rotina para que o robô consiga enxergar os campos dentro da página da blaze e realizar as apostas na sua conta.



Um exemplo de código simples para a aplicação desse bot na prática seria:

```python
from Scripts.BlazeFunctions.Bot import bot_class

Bot = bot_class('./Config.txt', Saldo=1000)

Bot.driver.initialize_browser()

while Bot.Carteira.Saldo > 0:
    Bot.RunRotina()
```

## Parâmetros de configuração do robô:
Os parâmetros abaixo são os parâmetros que devem ser definidos no arquivo 'Config.txt'.

Simulacao= [tipo: boolean]
> Quando ativada, o robô não fará nenhuma ação dentro da plataforma da blaze, e os cálculos serão feitos com base na sua carteira simulada. Caso essa opção esteja desativada, além de executar os comandos de aposta dentro da plataforma Blaze, o robô tentará buscar sempre o saldo disponível na sua conta, caso não encontre o campo de saldo será solicitado no prompt que faça o login para prosseguir com a rotina.

Objetivo_final= [tipo: float]
> Meta principal do robô. Ao atingir esse valor, o robô para de apostar imediatamente.

Const_meta= [tipo: float]
> Valor que será usado para definir uma nova meta á cada vitória.

leitura_Maxima_de_lances= [tipo: int]
> Quantidade de lances que serão levados em conta ao fazer análises de padrões (inclusive para IA).

Limite_de_apostas= [tipo: int]
> Quantas vezes o robô irá apostar. Ao atingir esse limite, o robô para de apostar imediatamente.

Margem_de_apostas= [tipo: float]
> Valor da carteira que pode ser usado para apostas.

Piso= [tipo: float]
> Saldo mínimo permitido. Ao atingir esse valor, o robô para de apostar imediatamente.

Protecao_na_cor= [tipo: boolean]
> Define se o robô deve ou não apostar na cor.

Tipo_de_protecao= [tipo: int]
> Define a regra que será usada para decidir a cor.

TaxaCor= [tipo: float]
> Margem extra que será apostada na cor. O valor final apostado na cor é definido por: valor_apostado_na_branca + (valor_apostado_na_branca TaxaCor)

Dobrar_meta= [tipo: boolean]
> Define se a Const_meta será dobrada nos primeiros lances.

Lances_dobrados= [tipo: int]
> Número de lances que serão dobrados.

Pausa= [tipo: boolean]
> Quando habilitada essa opção, o robô para de apostar imediatamente.

ModelPath= [tipo: string]
> Define o caminho do arquivo modelo de IA que será usado.

> [!IMPORTANT]
> Os parâmetros do tipo boolean são configurados com 's' para True e 'n' para False.

> [!IMPORTANT]
> O robô jogará automaticamente enquanto houver saldo disponível na conta do usuário, para impedir o robô de apostar, é preciso ativar a opção 'Pausa' no arquivo de configuração.
