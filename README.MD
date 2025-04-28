# Projeto Golden Raspeberry Api

Este projeto tem como objetivo resolver o desafio técnico **Golden Raspberry Awards.** que possibilita a leitura da lista de indicados e vencedores
da categoria Pior Filme do Golden Raspberry Awards.

No diretório */docs/challenge/* segue os insumos para o desafio.


## Linguagem/frameworks/serviços

- Python 3.10.12;
- fastapi 0.115.12;
- sqlite 3.37.2;
- pytest 8.3.5

## Premissas

O projeto foi criado no ambiente ubuntu wsl2. O arquivo que é consumido está no diretório */app/infra/bucket/input*, depois que o arquivo for consumido, será movido para a pasta */processed*

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

        python3 main.py

## Tests

        pytest

## Debugger

No diretório */.vscode/launch.json* está pré-configurado o modo debugger para o vscode.

## Postman

cURL

        curl --location '127.0.0.1:8080/v1/intervals' \
        --header 'x-api-key: a1b2c3d4'