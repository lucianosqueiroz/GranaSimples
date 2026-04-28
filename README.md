# GranaSimples

Controle financeiro simples, rápido e sem complicação.

## Rodar no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Seed do banco

Por padrão o aplicativo roda em modo produção e cria o banco vazio.
A seed só executa quando o banco está vazio e nunca sobrescreve dados existentes.

### Produção vazia

```powershell
$env:GRANASIMPLES_SEED_MODE="prod"
python app.py
```

Equivalente:

```powershell
GRANASIMPLES_SEED_MODE=prod python app.py
```

### Desenvolvimento e testes

```powershell
$env:GRANASIMPLES_SEED_MODE="dev"
python app.py
```

Equivalente:

```powershell
GRANASIMPLES_SEED_MODE=dev python app.py
```

### Demo comercial

```powershell
$env:GRANASIMPLES_SEED_MODE="demo"
python app.py
```

Equivalente:

```powershell
GRANASIMPLES_SEED_MODE=demo python app.py
```

## Testes

```powershell
python -m pytest
```

O banco SQLite é criado automaticamente em `data/granasimples.db`.
