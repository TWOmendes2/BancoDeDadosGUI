BancoDeDados GUI
Este projeto é uma interface gráfica de usuário (GUI) construída com ttkbootstrap e tkinter para interagir com um banco de dados MySQL. A aplicação permite ao usuário se conectar a um banco de dados e executar operações SQL básicas, incluindo INSERT, DELETE, UPDATE e SELECT.

Funcionalidades
Conexão com o Banco de Dados: Insira as credenciais do banco de dados (host, usuário, senha e nome do banco) para estabelecer uma conexão.
Seleção de Operações SQL: Escolha entre as operações INSERT, DELETE, UPDATE e SELECT.
Execução de Operações: Execute as operações SQL fornecendo os parâmetros necessários para cada operação.
Exibição de Resultados: Veja os resultados das consultas SELECT em uma nova janela com uma visão em tabela.
Estrutura do Código
Conexão ao Banco de Dados: A função conectar estabelece uma conexão com o banco de dados MySQL usando as credenciais fornecidas.
Seleção de Operações: A função selecionar_operacao permite ao usuário escolher a operação SQL desejada.
Execução de Operações: A função executar_operacao executa a operação SQL selecionada e exibe os resultados ou mensagens de erro.
Exibição de Resultados: A função exibir_resultado exibe os resultados das consultas SELECT em uma janela secundária usando um Treeview.
Tecnologias Utilizadas
Python: Linguagem de programação principal.
tkinter: Biblioteca padrão do Python para interfaces gráficas.
ttkbootstrap: Biblioteca para temas modernos do tkinter.
mysql-connector-python: Biblioteca para conectar ao MySQL e executar consultas SQL.
Como Usar
Clone o Repositório:

sh
Copiar código
git clone https://github.com/seu-usuario/bancodedados-gui.git
cd bancodedados-gui
Instale as Dependências:

sh
Copiar código
pip install ttkbootstrap mysql-connector-python
Execute a Aplicação:

sh
Copiar código
python app.py
Conecte-se ao Banco de Dados: Insira o host, usuário, senha e nome do banco de dados na GUI e clique em "Conectar".

Selecione e Execute Operações SQL: Escolha a operação desejada e insira os parâmetros necessários. Clique em "Executar" para ver os resultados.
