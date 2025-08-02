#!/bin/sh
set -e

echo ">>> Loading sample data into the database"
psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -f /sample_data/sample_data.sql

echo ">>> Database seeded successfully!"