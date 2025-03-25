# data-service/init_tenants.py
from sqlalchemy import text
from db import engine, Base
import models  # Ensure models are imported so they are registered

tenants = ["hospital_a", "hospital_b"]

for tenant in tenants:
    print(f"\n--- Processing tenant: {tenant} ---")
    with engine.begin() as conn:  # engine.begin() starts a transaction and commits on exit
        print(f"Creating schema '{tenant}' (if not exists)...")
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {tenant}"))
        
        print(f"Setting search path to '{tenant}'...")
        conn.execute(text(f"SET search_path TO {tenant}"))
        
        print("Creating tables in this schema...")
        Base.metadata.create_all(bind=conn)
        
        print(f"Listing tables in schema '{tenant}':")
        result = conn.execute(
            text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = :schema"),
            {"schema": tenant}
        )
        tables = result.fetchall()
        if tables:
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("  No tables found!")

print("\nTenant schemas initialized successfully.")
