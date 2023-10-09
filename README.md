# Projeto de automação de apostas (em progresso..)

Este projeto é um desafio pessoal que tem como objetivo me proporcionar um primeiro contato com o VS Code, Python, ambientes virtuais e outros conceitos de programação que até então não conhecia. Todos as técnicas/tecnologias usadas nesse projeto foram aprendidas através de muita pesquisa, tentativas e erros.

## Principais aprendizados:
* O que são ambientes virtuais e como trabalhar com eles;
* Sintaxe da linguagem Python;
* A importância da organização no código (Criar funções especializadas facilitam a manutenção e leitura do código);
* Conhecimento básico de IA (Funcionamento dos neurônios, funções de ativação, optimizadores, técnicas de treinamento, etc..);
* Tratamento de listas (Principalmente para trabalhar com IA).

## Funcionamento geral do robô de apostas.
<sup>Atenção: este é um projeto ainda em desenvolvimento, os conteúdos abaixo serão atualizados conforme o projeto evoluir.</sup>

Este robô é capaz de apostar automaticamente na plataforma da blaze (no jogo Double) seguindo uma rotina pré definida. Os parâmetros dessa rotina podem ser configurados pelo usuário através do arquivo "config.txt" na pasta de Scripts

O robô atualmente está funcionando através do script "Bot_V2.py" que está na pasta Scripts. Ao executar esse arquivo no terminal, será exibido um menu para o usuário selecionar qual modo de jogo deseja:

* 's' para simulação
* 'j' para jogar com o saldo real da sua conta Blaze.

No modo simulação, é necessário informar um saldo inicial, esse saldo será usado como ponto de partida para o robô começar as apostas, a partir daí o jogo segue normalmente.

Já na segunda opção, após abrir a janela do Chrome, o usuário deverá logar com sua conta no site da Blaze, após logado, basta digitar 'ok' no prompt e o robô começará a jogar.

<sup>Nota: o robô jogará automaticamente enquanto houver saldo disponível na conta do usuário, para impedir o robô de apostar, é preciso definir a variável pausa=s no arquivo de configuração.</sup>

##Parâmetros de configuração do robô:
Objetivo_final= >Define qual a meta principal do robô. Ao atingir esse valor, o robô para de apostar imediatamente.
Const_meta= >
leitura_Maxima_de_lances=5
Limite_de_apostas=200
Margem_de_apostas=15000
Piso=0
Protecao_na_cor=s
Tipo_de_protecao=5
TaxaCor=1
Dobrar_meta=n
Lances_dobrados=20
Pausa=n
ModelPath=C:\Users\rafael.luna\Desktop\docs pessoais\Projects\BotBlaze\BotBlaze\IA\Models\model_dense_input5_output2.keras
