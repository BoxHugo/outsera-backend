# Projeto Golden Raspeberry Api

Este projeto tem como objetivo resolver o desafio técnico **Golden Raspberry Awards.** que possibilita a leitura da lista de indicados e vencedores
da categoria Pior Filme do Golden Raspberry Awards.

No diretório */docs/challenge/* segue os insumos para o desafio.


## Linguagem/frameworks/serviços

- Python 3.10.12;
- fastapi 0.115.12;
- sqlite;

## Premissas

O projeto foi criado no ambiente ubuntu wsl2.

### Crie um arquivo .env (com o mesmo nome)

                API_VERSION="/v1"
                API_KEY="a1b2c3d4"
                HOST_API="127.0.0.1"
                PORT_API=8080
                PROJECT_NAME="Golden Raspeberry Api"
                FILEPATH="app/infra/bucket"


## Instalação

Na raiz do projeto:

        python3 -m venv venv

        source venv/bin/activate

        pip3 install requirements.txt


## Execução local



## Debugger

No diretório */.vscode/launch.json* está pré-configurado o modo debugger para o vscode.