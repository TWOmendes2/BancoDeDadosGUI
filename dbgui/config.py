import json
import os
from pathlib import Path


def load_config():
    required = ('DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_SCHEMA_JSON')
    values = {name: os.environ.get(name, '').strip() for name in required}
    if any(not value for value in values.values()):
        raise ValueError('Configuração incompleta')
    values['DB_PASSWORD'] = os.environ['DB_PASSWORD']
    options = dict(host=values['DB_HOST'], user=values['DB_USER'],
                   password=values['DB_PASSWORD'], database=values['DB_NAME'],
                   port=int(os.environ.get('DB_PORT', '3306')), connection_timeout=5,
                   autocommit=False)
    ca = os.environ.get('DB_SSL_CA')
    if ca:
        if not Path(ca).is_file():
            raise ValueError('Certificado CA ausente')
        options.update(ssl_ca=ca, ssl_verify_cert=True, ssl_verify_identity=True)
    elif values['DB_HOST'] not in ('127.0.0.1', 'localhost', '::1'):
        raise ValueError('Conexão remota exige DB_SSL_CA e verificação TLS')
    return options, json.loads(values['DB_SCHEMA_JSON']), os.environ.get('DB_ALLOW_WRITE') == '1'
