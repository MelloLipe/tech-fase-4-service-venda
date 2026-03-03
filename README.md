# Servico de Vendas de Veiculos

Microsservico responsavel pela listagem e venda de veiculos, com banco de dados isolado. Faz parte da plataforma de revenda de veiculos automotores.

## Arquitetura

O projeto segue **Clean Architecture** com as seguintes camadas:

```
app/
├── config/          # Configuracoes da aplicacao
├── domain/
│   ├── entities/    # Entidades de dominio (VeiculoVenda, Venda)
│   └── repositories/ # Interfaces dos repositorios (ABC)
├── application/
│   ├── dtos/        # Data Transfer Objects (Pydantic)
│   └── usecases/    # Casos de uso da aplicacao
└── infrastructure/
    ├── controllers/ # Endpoints FastAPI
    └── persistence/ # Implementacao dos repositorios (InMemory)
```

## Funcionalidades

- **Listagem de veiculos a venda** - Ordenada por preco (mais barato primeiro)
- **Listagem de veiculos vendidos** - Ordenada por preco (mais barato primeiro)
- **Efetuar venda de veiculo** - CPF do comprador e data da venda
- **Sincronizacao de veiculos** - Recebe dados do servico principal via HTTP
- **Atualizacao de status de pagamento** - Recebe notificacao do servico principal

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | `/veiculos/a-venda` | Lista veiculos disponiveis (ordenados por preco) |
| GET | `/veiculos/vendidos` | Lista veiculos vendidos (ordenados por preco) |
| POST | `/veiculos/comprar` | Efetua a venda de um veiculo |
| POST | `/veiculos/sync` | Sincroniza veiculo do servico principal |
| PUT | `/veiculos/{id}/status-pagamento` | Atualiza status do pagamento |
| GET | `/veiculos/{id}` | Busca veiculo por ID |
| GET | `/health` | Health check |

## Como usar localmente

### Pre-requisitos
- Python 3.11+
- pip

### Instalacao

```bash
pip install -r requirements.txt
```

### Executar

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

A API estara disponivel em `http://localhost:8001`

Documentacao Swagger: `http://localhost:8001/docs`

### Com Docker

```bash
docker-compose up --build
```

## Como testar

### Executar testes

```bash
pytest tests/ -v
```

### Executar testes com cobertura

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

A cobertura atual e de **94%** (minimo exigido: 80%).

## Comunicacao entre servicos

Este servico se comunica com o **Servico Principal** (porta 8000) via HTTP:

- Ao efetuar uma venda, registra o pagamento no servico principal
- Recebe atualizacoes de status de pagamento do servico principal
- Recebe sincronizacao de veiculos cadastrados no servico principal

### Variavel de ambiente

```
MAIN_SERVICE_URL=http://localhost:8000
```

## CI/CD

- **CI**: Testes automatizados com cobertura minima de 80% em toda PR para `main`
- **CD**: Deploy automatizado ao fazer merge na branch `main`
