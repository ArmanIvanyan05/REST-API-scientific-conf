"""Idempotent PostgreSQL database initialization script.

Usage (PowerShell):
  # requires psycopg2-binary in requirements
  python scripts/init_db.py --host localhost --port 5432 --user postgres --password secret --dbname scientific_conf --owner postgres

This script connects to the server database, creates the target database if missing,
and sets the owner. It is safe to run multiple times.
"""

import argparse
import psycopg2
from psycopg2 import sql


def init_db(pg_host, pg_port, pg_user, pg_password, db_name, db_owner):
    # Connect to default 'postgres' database to run CREATE DATABASE
    conn = psycopg2.connect(
        host=pg_host,
        port=pg_port,
        user=pg_user,
        password=pg_password,
        dbname="postgres",
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Check if db exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cur.fetchone() is not None
    if exists:
        print(f"Database '{db_name}' already exists.")
        # Ensure owner
        cur.execute(
            sql.SQL("ALTER DATABASE {} OWNER TO {};").format(
                sql.Identifier(db_name), sql.Identifier(db_owner)
            )
        )
        print(f"Set owner of '{db_name}' to '{db_owner}'.")
    else:
        # Create database
        cur.execute(
            sql.SQL("CREATE DATABASE {} OWNER {};").format(
                sql.Identifier(db_name), sql.Identifier(db_owner)
            )
        )
        print(f"Created database '{db_name}' with owner '{db_owner}'.")

    cur.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Initialize PostgreSQL database (idempotent)"
    )
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=5432, type=int)
    parser.add_argument("--user", default="postgres")
    parser.add_argument("--password", default="postgres")
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--owner", default=None)
    args = parser.parse_args()

    owner = args.owner or args.user
    init_db(args.host, args.port, args.user, args.password, args.dbname, owner)


if __name__ == "__main__":
    main()
