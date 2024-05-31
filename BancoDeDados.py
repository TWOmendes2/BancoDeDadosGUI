import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Função para conectar ao banco de dados
def conectar():
    global conexao, cursor
    host = entrada_host.get()
    user = entrada_user.get()
    password = entrada_password.get()
    database = entrada_database.get()

    try:
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )
        cursor = conexao.cursor()
        messagebox.showinfo("Sucesso", "Conectado ao banco de dados com sucesso")
        frame_conexao.pack_forget()
        frame_operacoes.pack(pady=20)

    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")

# Função para selecionar a operação SQL
def selecionar_operacao(operacao):
    global operacao_selecionada
    operacao_selecionada = operacao
    frame_operacoes.pack_forget()
    frame_parametros.pack(pady=20)
    label_operacao.config(text=f"Operação selecionada: {operacao}")
    if operacao == "SELECT":
        entrada_parametros.pack_forget()
        label_parametros.pack_forget()
    else:
        entrada_parametros.pack(side='left', padx=5, fill='x', expand=True)
        label_parametros.pack(side='left', padx=5)

# Função para executar a operação SQL
def executar_operacao():
    global cursor, conexao
    parametros = entrada_parametros.get()
    tabela_nome = tabela.get()

    try:
        if operacao_selecionada == "INSERT":
            cursor.execute(f"INSERT INTO {tabela_nome} VALUES ({parametros})")
        elif operacao_selecionada == "DELETE":
            cursor.execute(f"DELETE FROM {tabela_nome} WHERE {parametros}")
        elif operacao_selecionada == "UPDATE":
            cursor.execute(f"UPDATE {tabela_nome} SET {parametros}")
        elif operacao_selecionada == "SELECT":
            cursor.execute(f"SELECT * FROM {tabela_nome}")
            resultado = cursor.fetchall()
            exibir_resultado(resultado)
            return

        conexao.commit()
        cursor.execute(f"SELECT * FROM {tabela_nome}")
        resultado = cursor.fetchall()
        messagebox.showinfo("Tabela Atualizada", f"Resultado: {resultado}")

    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao executar operação: {err}")

# Função para exibir o resultado da consulta em uma janela secundária
def exibir_resultado(resultado):
    janela_resultado = tk.Toplevel(banco_dados)
    janela_resultado.title("Resultado da Consulta")
    janela_resultado.geometry("600x400")

    tree = ttk.Treeview(janela_resultado)
    tree.pack(fill="both", expand=True)

    # Configurando colunas
    tree["columns"] = list(range(len(resultado[0])))
    for i in range(len(resultado[0])):
        tree.column(i, anchor="center", stretch=tk.YES)
        tree.heading(i, text=f"Coluna {i+1}")

    # Inserindo linhas
    for row in resultado:
        tree.insert("", tk.END, values=row)

# Inicializando o estilo ttkbootstrap com o tema "solar"
style = Style(theme="solar")

# Criando a janela principal
banco_dados = style.master
banco_dados.title("BancoDeDados")
banco_dados.geometry("600x600")

# Frame para entrada das credenciais do banco de dados
frame_conexao = ttk.Frame(banco_dados, padding=10)
frame_conexao.pack(pady=20)
ttk.Label(frame_conexao, text="Host: ").grid(row=0, column=0, padx=5, pady=5)
entrada_host = ttk.Entry(frame_conexao)
entrada_host.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_conexao, text="User: ").grid(row=1, column=0, padx=5, pady=5)
entrada_user = ttk.Entry(frame_conexao)
entrada_user.grid(row=1, column=1, padx=5, pady=5)
ttk.Label(frame_conexao, text="Password: ").grid(row=2, column=0, padx=5, pady=5)
entrada_password = ttk.Entry(frame_conexao, show="*")
entrada_password.grid(row=2, column=1, padx=5, pady=5)
ttk.Label(frame_conexao, text="Database: ").grid(row=3, column=0, padx=5, pady=5)
entrada_database = ttk.Entry(frame_conexao)
entrada_database.grid(row=3, column=1, padx=5, pady=5)
ttk.Button(frame_conexao, text="Conectar", bootstyle=SUCCESS, command=conectar).grid(row=4, columnspan=2, pady=10)

# Frame para seleção da operação SQL
frame_operacoes = ttk.Frame(banco_dados, padding=10)
ttk.Label(frame_operacoes, text="Selecione a operação:").pack(pady=10)
ttk.Button(frame_operacoes, text="INSERT", bootstyle=PRIMARY, command=lambda: selecionar_operacao("INSERT")).pack(pady=5)
ttk.Button(frame_operacoes, text="DELETE", bootstyle=PRIMARY, command=lambda: selecionar_operacao("DELETE")).pack(pady=5)
ttk.Button(frame_operacoes, text="UPDATE", bootstyle=PRIMARY, command=lambda: selecionar_operacao("UPDATE")).pack(pady=5)
ttk.Button(frame_operacoes, text="SELECT", bootstyle=PRIMARY, command=lambda: selecionar_operacao("SELECT")).pack(pady=5)

# Frame para inserção dos parâmetros da operação
frame_parametros = ttk.Frame(banco_dados, padding=10)
label_operacao = ttk.Label(frame_parametros, text="Operação selecionada:")
label_operacao.pack(pady=10)
ttk.Label(frame_parametros, text="Tabela: ").pack(side='left', padx=5)
tabela = ttk.Entry(frame_parametros)
tabela.pack(side='left', padx=5)
label_parametros = ttk.Label(frame_parametros, text="Parâmetros: ")
label_parametros.pack(side='left', padx=5)
entrada_parametros = ttk.Entry(frame_parametros)
entrada_parametros.pack(side='left', padx=5, fill='x', expand=True)
ttk.Button(frame_parametros, text="Executar", bootstyle=SUCCESS, command=executar_operacao).pack(pady=10)

# Loop principal da aplicação
banco_dados.mainloop()
