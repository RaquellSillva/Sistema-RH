# Calculadora de Folha de Ponto

## Descrição do Projeto
Este projeto é um sistema web para calcular automaticamente a folha de ponto de funcionários. Ele facilita o fechamento de folha de pagamento, realizando o cálculo de horas trabalhadas, horas extras e descontos. Esse sistema é voltado para empresas que desejam agilizar o processo e garantir precisão nos pagamentos dos colaboradores.

## Funcionalidades
- Cálculo automático de horas trabalhadas.
- Cálculo de horas extras.
- Aplicação de descontos e benefícios.
- Geração de relatórios em PDF com os resultados.
- Tela de login para acesso de usuários cadastrados.
- Opção de cadastro de novos usuários (fixo, sem banco de dados).

## Tecnologias Utilizadas
- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS
- **Integração**: Azure 

## Como usar
- **Login**
- Como não há banco de dados, utilize as seguintes credenciais para acessar o sistema:

  - **Usuário: admin**
  - **Senha: senha123**

1. Acesse a tela de login e faça o login com seu usuário acima.
2. Na página inicial, insira os dados de jornada de trabalho, horas extras e descontos.
3. Clique em Calcular para gerar a folha de ponto.
4. Acesse o relatório em PDF na opção correspondente para fazer o download.

## Estrutura do Projeto
```
Sistema-RH/calculadora/
├── app.py                 # Arquivo principal do servidor Flask
├── templates/             # Páginas HTML do projeto
├── static/                # Arquivos de CSS e JavaScript
├── requirements.txt       # Arquivo com as dependências do projeto
└── README.md              # Documentação do projeto
```



