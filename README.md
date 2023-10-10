# Projeto de automação de apostas (em progresso..)

Este projeto é um desafio pessoal que tem como objetivo criar um robô capaz de jogar sozinho no jogo double da Blaze. Todos as técnicas/tecnologias usadas nesse projeto foram aprendidas através de muita pesquisa, tentativas e erros.

## Principais aprendizados:
* O que são ambientes virtuais e como trabalhar com eles;
* Sintaxe da linguagem Python;
* A importância da organização no código (Criar funções especializadas facilitam a manutenção e leitura do código);
* Conhecimento básico de IA (Funcionamento dos neurônios, funções de ativação, optimizadores, técnicas de treinamento, etc..);
* Tratamento de listas (Principalmente para trabalhar com IA).

## Funcionamento geral do robô de apostas.
> [!WARNING]
> Este é um projeto ainda em desenvolvimento, os conteúdos abaixo serão atualizados conforme o projeto evoluir.

Este robô é capaz de apostar automaticamente na plataforma da blaze (no jogo Double) seguindo uma rotina pré definida. Os parâmetros dessa rotina podem ser configurados pelo usuário através do arquivo "config.txt" na pasta de Scripts

O robô atualmente está funcionando através do script "Bot_V2.py" que está na pasta Scripts. Ao executar esse arquivo no terminal, será exibido um menu para o usuário selecionar qual modo de jogo deseja:

* 's' para simulação
* 'j' para jogar com o saldo real da sua conta Blaze.

No modo simulação, é necessário informar um saldo inicial, esse saldo será usado como ponto de partida para o robô começar as apostas, a partir daí o jogo segue normalmente.

Já na segunda opção, após abrir a janela do Chrome, o usuário deverá logar com sua conta no site da Blaze, após logado, basta digitar 'ok' no prompt e o robô começará a jogar.

> [!NOTE]
> O robô jogará automaticamente enquanto houver saldo disponível na conta do usuário, para impedir o robô de apostar, é preciso definir a variável pausa=s no arquivo de configuração.

## Parâmetros de configuração do robô:

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


## Mais detalhes sobre o código

O código funciona majoritariamente no script "Bot_V2.py", dentro desse script há diversas funções como 'incluiraposta', 'pagarpremio', 'getsaldo', etc.. todas elas são utilizadas dentro da rotina do robô para calcular o valor que será apostado, qual cor será apostado, e carregar informações sobre os lances anteriores para o robô tomar as decisões (muitas dessas funções serão colocadas em Scripts separados futuramente, isso vai facilitar a leitura e manutenção do código
