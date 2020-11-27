#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 -U "postgres" -d "postgres" <<-EOSQL
	CREATE USER "$USER_DB" WITH PASSWORD '$PASSWORD';
	CREATE DATABASE "$DATABASE" OWNER "$USER_DB";
EOSQL
