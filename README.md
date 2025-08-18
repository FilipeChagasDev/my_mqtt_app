# My MQTT App
Projeto de prática de estudo -- plataforma para consumir dados de sensores IoT multi-tenant via MQTT com segurança

## Instruções de desenvolvimento

### Variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example` e preencha-o com os valores corretos das variáveis de ambiente.

### Testes locais

Para testar localmente o projeto, execute o script `test.ps1`. Ele executará o contêiner nas configurações do arquivo `compose.dev.yaml`, expondo o banco de dados à rede pública e adicionando o `pgweb`.

Com o contêiner de teste em execução, acesse `localhost:8082` no navegador para visualizar o banco de dados.

Para simular um sensor enviando dados, execute `python sensors/script.py`.

### Atualizações de banco de dados

Ao modificar a estrutura do banco de dados no arquivo `models.py` do listener, dê os seguintes comandos:

1. Entrar no diretório mqtt_listener 
```sh
cd mqtt_listener
```

2. Gerar script de migrações
```sh
alembic revision --autogenerate -m "descrição"
```

3. Aplicar migrações
```sh
alembic upgrade head
```

