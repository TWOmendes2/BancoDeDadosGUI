import json
import tkinter as tk
from tkinter import ttk, messagebox
from .repository import Repository
from .config import load_config


def main():
    root = tk.Tk()
    root.title('BancoDeDadosGUI v2')
    connection = None
    try:
        import mysql.connector
        options, schema, allow_write = load_config()
        connection = mysql.connector.connect(**options)
        repo = Repository(connection, schema, allow_write)
    except Exception:
        if connection is not None:
            connection.close()
        messagebox.showerror('Conexão indisponível', 'Confira ambiente, permissões e TLS. Detalhes sensíveis foram omitidos.')
        root.destroy()
        return

    table = tk.StringVar(value=next(iter(repo.schema)))
    operation = tk.StringVar(value='SELECT')
    ttk.Label(root, text='Escrita habilitada' if allow_write else 'Somente leitura').pack()
    ttk.Combobox(root, textvariable=table, values=list(repo.schema), state='readonly').pack(fill='x')
    ttk.Combobox(root, textvariable=operation, values=('SELECT', 'INSERT', 'UPDATE', 'DELETE') if allow_write else ('SELECT',), state='readonly').pack(fill='x')
    ttk.Label(root, text='Valores JSON (ex.: {"nome":"Cliente Sintético"})').pack()
    values = ttk.Entry(root, width=80); values.insert(0, '{}'); values.pack(fill='x')
    ttk.Label(root, text='Filtro de igualdade JSON (obrigatório para UPDATE/DELETE)').pack()
    filters = ttk.Entry(root, width=80); filters.insert(0, '{}'); filters.pack(fill='x')
    result = ttk.Treeview(root, show='headings')
    status = tk.StringVar(value='Máximo de 100 registros por consulta.')

    def execute():
        try:
            selected = table.get()
            where = json.loads(filters.get())
            if operation.get() == 'SELECT':
                rows = repo.select(selected, where)
                result.delete(*result.get_children())
                result['columns'] = repo.schema[selected]
                for column in repo.schema[selected]:
                    result.heading(column, text=column)
                for row in rows:
                    result.insert('', 'end', values=row)
                status.set(f'{len(rows)} registros exibidos (limite 100).')
                return
            data = json.loads(values.get())
            if not messagebox.askyesno('Confirmar alteração', 'Aplicar a operação ao banco configurado? Confira tabela e filtro.'):
                return
            if operation.get() == 'INSERT':
                count = repo.insert(selected, data)
            elif operation.get() == 'UPDATE':
                count = repo.update(selected, data, where)
            else:
                count = repo.delete(selected, where)
            result.delete(*result.get_children())
            status.set(f'Operação concluída: {count} registros afetados.')
        except (ValueError, PermissionError):
            status.set('Entrada inválida: confira tabela, campos, JSON e filtro obrigatório.')
        except Exception:
            status.set('Operação falhou. Nenhum detalhe do banco foi exibido; confira a conexão.')

    ttk.Button(root, text='Executar', command=execute).pack()
    ttk.Label(root, textvariable=status).pack()
    result.pack(fill='both', expand=True)

    def close():
        try:
            connection.close()
        finally:
            root.destroy()

    root.protocol('WM_DELETE_WINDOW', close)
    root.mainloop()
