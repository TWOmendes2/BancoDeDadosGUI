# BancoDeDados GUI

Este projeto é uma interface gráfica de usuário (GUI) construída com `ttkbootstrap` e `tkinter` para interagir com um banco de dados MySQL. A aplicação permite ao usuário se conectar a um banco de dados e executar operações SQL básicas, incluindo `INSERT`, `DELETE`, `UPDATE` e `SELECT`.

## Funcionalidades

- **Conexão com o Banco de Dados**: Insira as credenciais do banco de dados (host, usuário, senha e nome do banco) para estabelecer uma conexão.
- **Seleção de Operações SQL**: Escolha entre as operações `INSERT`, `DELETE`, `UPDATE` e `SELECT`.
- **Execução de Operações**: Execute as operações SQL fornecendo os parâmetros necessários para cada operação.
- **Exibição de Resultados**: Veja os resultados das consultas `SELECT` em uma nova janela com uma visão em tabela.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **tkinter**: Biblioteca padrão do Python para interfaces gráficas.
- **ttkbootstrap**: Biblioteca para temas modernos do `tkinter`.
- **mysql-connector-python**: Biblioteca para conectar ao MySQL e executar consultas SQL.

## Como Usar

1. **Clone o Repositório**:
    ```sh
    git clone https://github.com/seu-usuario/bancodedados-gui.git
    cd bancodedados-gui
    ```

2. **Instale as Dependências**:
    ```sh
    pip install ttkbootstrap mysql-connector-python
    ```

3. **Execute a Aplicação**:
    ```sh
    python app.py
    ```

4. **Conecte-se ao Banco de Dados**: Insira o host, usuário, senha e nome do banco de dados na GUI e clique em "Conectar".

5. **Selecione e Execute Operações SQL**: Escolha a operação desejada e insira os parâmetros necessários. Clique em "Executar" para ver os resultados.
