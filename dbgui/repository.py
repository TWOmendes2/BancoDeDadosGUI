import math
import re


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,63}', value):
        raise ValueError('Identificador inválido')
    return '`' + value + '`'


class Repository:
    def __init__(self, connection, schema, allow_write=False):
        if not isinstance(schema, dict) or not schema:
            raise ValueError('Defina a lista de tabelas e colunas permitidas')
        self.schema = {}
        for table, columns in schema.items():
            identifier(table)
            if not isinstance(columns, list) or not columns or len(set(columns)) != len(columns):
                raise ValueError('Colunas inválidas')
            for column in columns:
                identifier(column)
            self.schema[table] = tuple(columns)
        self.connection = connection
        self.allow_write = allow_write

    def _fields(self, table, values, required=False):
        if table not in self.schema or not isinstance(values, dict) or (required and not values):
            raise ValueError('Tabela ou campos inválidos')
        for key, value in values.items():
            if key not in self.schema[table]:
                raise ValueError('Coluna não permitida')
            if value is not None and type(value) not in (str, int, float, bool):
                raise ValueError('Valor deve ser escalar')
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError('Número não finito')
            if isinstance(value, str) and len(value) > 10000:
                raise ValueError('Valor muito longo')

    def _where(self, table, filters, required=False):
        self._fields(table, filters, required)
        clauses, params = [], []
        for key, value in filters.items():
            if value is None:
                clauses.append(identifier(key) + ' IS NULL')
            else:
                clauses.append(identifier(key) + ' = %s')
                params.append(value)
        return (' WHERE ' + ' AND '.join(clauses) if clauses else ''), params

    def _execute(self, query, params, write=False):
        if write and not self.allow_write:
            raise PermissionError('Conexão em modo somente leitura')
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, tuple(params))
            if write:
                self.connection.commit()
                return cursor.rowcount
            return cursor.fetchall()
        except Exception:
            if write:
                self.connection.rollback()
            raise
        finally:
            cursor.close()

    def select(self, table, filters=None, limit=100):
        if type(limit) is not int or not 1 <= limit <= 500:
            raise ValueError('Limite deve estar entre 1 e 500')
        where, params = self._where(table, {} if filters is None else filters)
        columns = ', '.join(identifier(column) for column in self.schema[table])
        return self._execute(f'SELECT {columns} FROM {identifier(table)}{where} LIMIT %s', params + [limit])

    def insert(self, table, values):
        self._fields(table, values, required=True)
        columns = ', '.join(identifier(column) for column in values)
        placeholders = ', '.join('%s' for _ in values)
        return self._execute(f'INSERT INTO {identifier(table)} ({columns}) VALUES ({placeholders})', list(values.values()), True)

    def update(self, table, values, filters):
        self._fields(table, values, required=True)
        where, params = self._where(table, filters, required=True)
        assignments = ', '.join(identifier(column) + ' = %s' for column in values)
        return self._execute(f'UPDATE {identifier(table)} SET {assignments}{where}', list(values.values()) + params, True)

    def delete(self, table, filters):
        where, params = self._where(table, filters, required=True)
        return self._execute(f'DELETE FROM {identifier(table)}{where}', params, True)
