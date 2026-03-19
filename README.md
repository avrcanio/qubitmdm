# QubitMDM

Custom EMM backend based on Android Management API (AMAPI), built with Django + DRF.

## Docker-only quick start

1. Copy env template:

```bash
cp .env.example .env
```

2. Ensure `postgis` container is up and create DB once:

```bash
docker exec ce55603ca88f psql -U postgres -d postgres -c "CREATE DATABASE qubitmdm;"
```

3. Build and start app:

```bash
docker compose up -d --build
```

4. Run migrations:

```bash
docker compose exec web python manage.py migrate
```

5. Create superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

6. Optional tests:

```bash
docker compose exec web python manage.py test
```

## Notes

- Default `.env.example` is configured for container-to-container DB access (`DB_HOST=postgis`).
- If you run Django directly on host (not recommended in this workflow), use `DB_HOST=127.0.0.1`.
