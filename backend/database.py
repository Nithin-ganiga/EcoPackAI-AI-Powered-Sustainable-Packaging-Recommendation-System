"""This file contains all MySQL operations used by the API, including connection helpers, material queries, autocomplete lookups, and search logging so database access stays isolated and maintainable."""

from typing import Any, Dict, List, Optional
import mysql.connector
from mysql.connector import Error

from config import config


MATERIAL_COLUMNS = (
    "packaging_material, material_type, industry, strength, weight_capacity_kg, "
    "biodegradability_score, co2_emission_score, recyclability_percent, packaging_cost_inr, "
    "co2_impact_index, cost_efficiency_index, material_suitability_score, sustainability_tier"
)


def get_connection() -> Optional[mysql.connector.MySQLConnection]:
    try:
        return mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT,
        )
    except Error:
        return None


def test_connection() -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        return conn.is_connected()
    finally:
        conn.close()


def _rows_to_dicts(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [dict(row) for row in rows]


def get_materials_by_product(product_name: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    if not conn:
        return []

    sql = (
        "SELECT "
        "packaging_material, material_type, industry, strength, weight_capacity_kg, "
        "biodegradability_score, co2_emission_score, recyclability_percent, packaging_cost_inr, "
        "co2_impact_index, cost_efficiency_index, material_suitability_score, sustainability_tier "
        "FROM ("
        "  SELECT "
        f"    {MATERIAL_COLUMNS}, "
        "    ROW_NUMBER() OVER ("
        "      PARTITION BY packaging_material, material_type "
        "      ORDER BY material_suitability_score DESC"
        "    ) AS rn "
        "  FROM materials "
        "  WHERE LOWER(packaged_item) LIKE LOWER(%s)"
        ") ranked "
        "WHERE rn = 1 "
        "ORDER BY material_suitability_score DESC "
        "LIMIT 100"
    )
    search_term = f"%{product_name}%"

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (search_term,))
        rows = cursor.fetchall()
        return _rows_to_dicts(rows)
    except Error as exc:
        print(f"[db] get_materials_by_product failed: {exc}")
        return []
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def get_all_unique_materials() -> List[Dict[str, Any]]:
    conn = get_connection()
    if not conn:
        return []

    sql = (
        "SELECT "
        "packaging_material, material_type, industry, strength, weight_capacity_kg, "
        "biodegradability_score, co2_emission_score, recyclability_percent, packaging_cost_inr, "
        "co2_impact_index, cost_efficiency_index, material_suitability_score, sustainability_tier "
        "FROM ("
        "  SELECT "
        f"    {MATERIAL_COLUMNS}, "
        "    ROW_NUMBER() OVER ("
        "      PARTITION BY packaging_material, material_type "
        "      ORDER BY material_suitability_score DESC"
        "    ) AS rn "
        "  FROM materials"
        ") ranked "
        "WHERE rn = 1 "
        "ORDER BY material_suitability_score DESC "
        "LIMIT 100"
    )

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()
        return _rows_to_dicts(rows)
    except Error as exc:
        print(f"[db] get_all_unique_materials failed: {exc}")
        return []
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def get_autocomplete_suggestions(query: str) -> List[str]:
    conn = get_connection()
    if not conn:
        return []

    sql = (
        "SELECT DISTINCT packaged_item "
        "FROM materials "
        "WHERE LOWER(packaged_item) LIKE LOWER(%s) "
        "LIMIT 8"
    )
    search_term = f"%{query}%"

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (search_term,))
        rows = cursor.fetchall()
        return [row[0] for row in rows if row and row[0]]
    except Error:
        return []
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def create_search_logs_table() -> bool:
    conn = get_connection()
    if not conn:
        return False

    sql = (
        "CREATE TABLE IF NOT EXISTS search_logs ("
        "id INT AUTO_INCREMENT PRIMARY KEY,"
        "product_name VARCHAR(200),"
        "weight_grams FLOAT,"
        "fragility VARCHAR(20),"
        "top_result VARCHAR(200),"
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ")"
    )

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return True
    except Error:
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def save_search_log(product_name: str, weight_grams: float, fragility: str, top_result: str) -> bool:
    conn = get_connection()
    if not conn:
        return False

    sql = (
        "INSERT INTO search_logs (product_name, weight_grams, fragility, top_result) "
        "VALUES (%s, %s, %s, %s)"
    )

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (product_name, weight_grams, fragility, top_result))
        conn.commit()
        return True
    except Error:
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()
