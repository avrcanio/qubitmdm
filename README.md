# QubitMDM

Custom EMM backend based on Android Management API (AMAPI), built with Django + DRF.

## Quick start

1. Copy env template:

```bash
cp .env.example .env
```

2. Ensure `postgis` container is up (`127.0.0.1:5432`) and create DB:

```bash
docker exec ce55603ca88f psql -U postgres -d postgres -c "CREATE DATABASE qubitmdm;"
```

3. Install deps and migrate:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

4. Run app:

```bash
python manage.py runserver
```

## Docker mode

Set `.env` with `DB_HOST=host.docker.internal` and run:

```bash
docker compose up --build
```
