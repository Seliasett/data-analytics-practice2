import sqlite3
from datetime import date
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "sales.db"


def main() -> None:
    rows = [
        ("2026-01-08", "Ноутбук Pro", "Электроника", 3, 420000),
        ("2026-01-19", "Смарт-часы", "Электроника", 8, 95000),
        ("2026-02-03", "Куртка Sport", "Одежда", 12, 48000),
        ("2026-02-15", "Кофемашина", "Бытовая техника", 5, 110000),
        ("2026-03-02", "Наушники", "Электроника", 15, 35000),
        ("2026-03-21", "Кроссовки", "Одежда", 20, 30000),
        ("2026-04-10", "Пылесос", "Бытовая техника", 7, 90000),
        ("2026-04-28", "Рюкзак", "Аксессуары", 18, 18000),
        ("2026-05-06", "Планшет", "Электроника", 6, 160000),
        ("2026-05-24", "Часы Classic", "Аксессуары", 9, 55000),
        ("2026-06-07", "Холодильник", "Бытовая техника", 4, 250000),
        ("2026-06-26", "Футболка", "Одежда", 25, 12000),
        ("2026-07-05", "Телевизор", "Электроника", 5, 220000),
        ("2026-07-18", "Кофеварка", "Бытовая техника", 10, 65000),
        ("2026-08-09", "Книга Python", "Книги", 30, 8000),
        ("2026-08-22", "Кроссовки Lite", "Одежда", 14, 28000),
    ]

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY,
                sale_date TEXT NOT NULL,
                product TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL
            )
        """)
        connection.execute("DELETE FROM sales")
        connection.executemany(
            """
            INSERT INTO sales
                (sale_date, product, category, quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )
        connection.commit()

    print(f"База данных обновлена: {DB_PATH}")


if __name__ == "__main__":
    main()
