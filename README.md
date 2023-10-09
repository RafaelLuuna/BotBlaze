# Projeto de automação de apostas (em progresso..)

Este projeto é um desafio pessoal que tem como objetivo me proporcionar um primeiro contato com o VS Code, Python, ambientes virtuais e outros conceitos de programação que até então não conhecia. Todos as técnicas/tecnologias usadas nesse projeto foram aprendidas através de muita pesquisa, tentativas e erros.

### Principais aprendizados:
* O que são ambientes virtuais e como trabalhar com eles;
* Sintaxe da linguagem Python;
* A importância da organização no código (Criar funções especializadas facilitam a manutenção e leitura do código);
* Conhecimento básico de IA (Funcionamento dos neurônios, funções de ativação, optimizadores, técnicas de treinamento, etc..);
* Tratamento de listas (Principalmente para trabalhar com IA).

### Funcionamento geral do robô de apostas.
**Atenção: este é um projeto ainda em desenvolvimento, os conteúdos abaixo serão atualizados conforme o projeto for evoluindo.**

Este robô é capaz de apostar automaticamente na plataforma da blaze (no jogo Double) seguindo uma rotina pré definida. Os parâmetros dessa rotina podem ser configurados pelo usuário através do arquivo "config.txt" na pasta de Scripts

O robô funciona através do script "Bot_V2.py" que está na pasta Scripts, ao executar esse arquivo no terminal é aberto um menu para o usuário selecionar o modo de jogo:

- 's' para simulação
- 'j' para jogar (ou modo real)

No modo simulação, após o usuário escolher a opção ele deverá informar um saldo inicial para o robô simular uma carteira com aquele valor, a partir daí o jogo começa normalmente.
