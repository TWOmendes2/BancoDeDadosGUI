# BancoDeDadosGUI v2

Cliente didático MySQL com interface Tkinter, consultas parametrizadas e lista explícita
de tabelas/colunas permitidas. A v2 substitui a entrada livre de SQL por operações
estruturadas; a implementação antiga permanece no histórico Git.

## Preparação

Python 3.11+ com Tkinter e `pip install -r requirements.txt`. Configure variáveis do
ambiente conforme `.env.example` (não há carregamento automático de .env).
Use usuário MySQL com privilégios mínimos em um banco de demonstração.

`DB_SCHEMA_JSON` é um objeto de tabelas e colunas autorizadas, por exemplo
`{"clients":["id","name"]}`. Não cria tabelas. O esquema já deve existir no banco.
Para teste local, crie `clients(id INT PRIMARY KEY, name VARCHAR(255))` em um banco vazio.
Conexões remotas exigem `DB_SSL_CA` com CA confiável, verificando certificado e hostname.
Escrita exige `DB_ALLOW_WRITE=1`; por padrão a interface é somente leitura.

```sh
python BancoDeDados.py
python -m unittest discover -s tests -v
```

## Uso

Selecione tabela e operação. Informe valores JSON como `{"id":1,"name":"Cliente Sintético"}`
e filtros por igualdade como `{"id":1}`. UPDATE/DELETE sem filtros são rejeitados.
JSON não aceita expressões SQL, joins ou operadores arbitrários. Uma condição pode
atingir várias linhas: confira o filtro; a interface pede confirmação antes da escrita.
SELECT limita a 100 registros na UI (máximo 500 na API), com resultados vazios tratados.

## Arquitetura e segurança

`config.py` valida ambiente/TLS; `repository.py` valida identificadores contra allowlist,
passa valores separados via placeholders `%s`, fecha cursores e faz rollback em falhas;
`ui.py` apresenta dados e mensagens genéricas sem registrar credenciais/erros SQL.
Allowlist não substitui grants do banco. Não há suporte a bancos de terceiros sem autorização.

## Testes e limites

Suíte offline executa CRUD em SQLite em memória por um adaptador de placeholders,
testa payload de SQL injection como dado literal, filtros obrigatórios, colunas inválidas,
somente leitura, rollback, fechamento de cursor e configuração TLS. Um mock verifica
o formato `%s` do driver MySQL. Isso não substitui integração com MySQL real, que deve
ser homologada em banco descartável; a UI e TLS remoto não foram exercitados aqui.

Versão 2.0.0 proposta. O contrato de entrada muda deliberadamente para remover SQL livre.
