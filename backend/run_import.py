"""This file creates the materials table and imports CSV rows into MySQL so the recommendation engine has real catalog data available before API requests are processed."""

import csv
from pathlib import Path

from database import get_connection


DEFAULT_CSV = Path(__file__).resolve().parent / "materials.csv"


def create_materials_table() -> None:
    conn = get_connection()
    if not conn:
        raise RuntimeError("Unable to connect to MySQL. Check .env settings.")

    ddl = (
        "CREATE TABLE IF NOT EXISTS materials ("
        "id INT AUTO_INCREMENT PRIMARY KEY,"
        "packaged_item VARCHAR(255),"
        "packaging_material VARCHAR(255),"
        "material_type VARCHAR(100),"
        "industry VARCHAR(100),"
        "strength VARCHAR(20),"
        "weight_capacity_kg FLOAT,"
        "biodegradability_score INT,"
        "co2_emission_score INT,"
        "recyclability_percent INT,"
        "packaging_cost_inr FLOAT,"
        "co2_impact_index FLOAT,"
        "cost_efficiency_index FLOAT,"
        "material_suitability_score FLOAT,"
        "sustainability_tier VARCHAR(30)"
        ")"
    )

    cursor = conn.cursor()
    cursor.execute(ddl)
    conn.commit()
    cursor.close()
    conn.close()


def import_csv(csv_path: Path) -> int:
    conn = get_connection()
    if not conn:
        raise RuntimeError("Unable to connect to MySQL. Check .env settings.")

    insert_sql = (
        "INSERT INTO materials ("
        "packaged_item, packaging_material, material_type, industry, strength, weight_capacity_kg, "
        "biodegradability_score, co2_emission_score, recyclability_percent, packaging_cost_inr, "
        "co2_impact_index, cost_efficiency_index, material_suitability_score, sustainability_tier"
        ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    count = 0
    cursor = conn.cursor()

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            values = (
                row.get("packaged_item", ""),
                row.get("packaging_material", ""),
                row.get("material_type", ""),
                row.get("industry", ""),
                row.get("strength", "Low"),
                float(row.get("weight_capacity_kg", 0) or 0),
                int(float(row.get("biodegradability_score", 0) or 0)),
                int(float(row.get("co2_emission_score", 0) or 0)),
                int(float(row.get("recyclability_percent", 0) or 0)),
                float(row.get("packaging_cost_inr", 0) or 0),
                float(row.get("co2_impact_index", 0) or 0),
                float(row.get("cost_efficiency_index", 0) or 0),
                float(row.get("material_suitability_score", 0) or 0),
                row.get("sustainability_tier", "Average"),
            )
            cursor.execute(insert_sql, values)
            count += 1

    conn.commit()
    cursor.close()
    conn.close()
    return count


if __name__ == "__main__":
    create_materials_table()
    if DEFAULT_CSV.exists():
        rows = import_csv(DEFAULT_CSV)
        print(f"Imported {rows} rows from {DEFAULT_CSV.name}")
    else:
        print("materials.csv not found in backend folder. Table is ready for import.")
