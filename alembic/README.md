# Generic single-database configuration.

## Create revision
- alembic revision --autogenerate -m "message"

### Upgrade (Generate .sql files for manually execute SQL command)
- alembic upgrade head --sql > alembic/sql/migrations.sql

### Downgrade (Generate .sql files for manually execute SQL command)
- alembic downgrade current_revision:-1 --sql > alembic/sql/migrations.sql

## Autoupdate database. WARNING: Do not use for production environment, bug may happen
- alembic upgrade head
- alembic downgrade -1