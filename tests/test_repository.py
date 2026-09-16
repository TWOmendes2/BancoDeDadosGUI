import sqlite3
import unittest
from unittest.mock import Mock, patch
from dbgui.repository import Repository
from dbgui.config import load_config


class Cursor:
    def __init__(self, connection):
        self.cursor = connection.cursor()
    def execute(self, query, params):
        self.cursor.execute(query.replace('%s', '?'), params)
    def fetchall(self):
        return self.cursor.fetchall()
    @property
    def rowcount(self):
        return self.cursor.rowcount
    def close(self):
        self.cursor.close()


class Connection:
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT)')
    def cursor(self):
        return Cursor(self.db)
    def commit(self):
        self.db.commit()
    def rollback(self):
        self.db.rollback()


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.connection = Connection()
        self.repo = Repository(self.connection, {'clients': ['id', 'name']}, True)
    def tearDown(self):
        self.connection.db.close()
    def test_crud_and_injection_is_literal_data(self):
        attack = "x'); DROP TABLE clients; --"
        self.repo.insert('clients', {'id': 1, 'name': attack})
        self.assertEqual(self.repo.select('clients'), [(1, attack)])
        self.repo.update('clients', {'name': 'Synthetic'}, {'id': 1})
        self.assertEqual(self.repo.select('clients', {'name': attack}), [])
        self.assertEqual(self.repo.delete('clients', {'id': 1}), 1)
        self.assertEqual(self.repo.select('clients'), [])
    def test_identifiers_and_filters_are_restricted(self):
        for table in ('clients; DROP TABLE clients', 'other'):
            with self.assertRaises(ValueError): self.repo.select(table)
        with self.assertRaises(ValueError): self.repo.select('clients', {'id OR 1=1': 1})
        with self.assertRaises(ValueError): self.repo.update('clients', {'name': 'x'}, {})
        with self.assertRaises(ValueError): self.repo.delete('clients', {})
        with self.assertRaises(ValueError): self.repo.select('clients', limit=501)
        with self.assertRaises(ValueError): self.repo.insert('clients', {'name': {'sql': 'bad'}})
    def test_null_filter_and_read_only(self):
        self.repo.insert('clients', {'id': 1, 'name': None})
        self.assertEqual(len(self.repo.select('clients', {'name': None})), 1)
        readonly = Repository(self.connection, {'clients': ['id', 'name']})
        with self.assertRaises(PermissionError): readonly.delete('clients', {'id': 1})
    def test_rollback_and_cursor_close_on_failure(self):
        connection = Mock()
        connection.cursor.return_value.execute.side_effect = RuntimeError('synthetic')
        repo = Repository(connection, {'clients': ['id']}, True)
        with self.assertRaises(RuntimeError): repo.insert('clients', {'id': 1})
        connection.rollback.assert_called_once()
        connection.commit.assert_not_called()
        connection.cursor.return_value.close.assert_called_once()
    def test_mysql_placeholder_and_values_separate(self):
        connection = Mock()
        repo = Repository(connection, {'clients': ['id', 'name']}, True)
        repo.update('clients', {'name': "' OR 1=1 --"}, {'id': 7})
        connection.cursor.return_value.execute.assert_called_once_with(
            'UPDATE `clients` SET `name` = %s WHERE `id` = %s', ("' OR 1=1 --", 7))
    def test_remote_requires_tls(self):
        env = dict(DB_HOST='db.example.invalid', DB_USER='synthetic', DB_PASSWORD='synthetic',
                   DB_NAME='demo', DB_SCHEMA_JSON='{"clients":["id"]}')
        with patch.dict('os.environ', env, clear=True), self.assertRaises(ValueError):
            load_config()
