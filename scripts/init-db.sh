#!/bin/bash
set -e

echo "Starting database initialization script..."

# エラーハンドリング関数
handle_error() {
    echo "Error occurred in script at line: $1"
    echo "Exiting..."
}

# エラートラップを設定
trap 'handle_error $LINENO' ERR

# 環境変数の確認
echo "Checking environment variables..."
: "${POSTGRES_USER:?POSTGRES_USER is not set}"
: "${POSTGRES_DB:?POSTGRES_DB is not set}"
: "${APP_USER_PASSWORD:?APP_USER_PASSWORD is not set}"

echo "Creating app_user and granting privileges..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$\$
    BEGIN
        CREATE USER app_user WITH PASSWORD '${APP_USER_PASSWORD}';
        RAISE NOTICE 'User app_user created successfully';
    EXCEPTION
        WHEN duplicate_object THEN
            RAISE NOTICE 'User app_user already exists. Skipping creation.';
    END
    \$\$;

    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO app_user;
    
    \c ${POSTGRES_DB}
    
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;
EOSQL

echo "Executing SQL files..."
for file in /docker-entrypoint-initdb.d/sql/*.sql
do
    echo "Executing $file..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$file"
done

echo "Database initialization completed successfully."
