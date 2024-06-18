Generic single-database configuration.

# Create revision
alembic revision --autogenerate -m "message"

# Generate .sql files for manually execute SQL command
## Upgrade
alembic upgrade head --sql > alembic/sql/migrations.sql

## Downgrade to previous revision
alembic downgrade current_revision:-1 --sql > alembic/sql/migrations.sql

# Autoupdate database, no need to manually execute SQL command
## WARNING: DO NOT USE BELOW COMMANDS IN IMPORTANT ENVIRONMENT, BUT MAY HAPPEN ANY TIME
alembic upgrade head
alembic downgrade -1