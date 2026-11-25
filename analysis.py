import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sales.db"
CHARTS_DIR = BASE_DIR / "charts"


def load_sales() -> pd.DataFrame:
    """Load sales data directly from SQLite."""
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}. Place sales.db in the project folder."
        )

    query = """
        SELECT
            sale_id,
            sale_date,
            product,
            category,
            quantity,
            unit_price
        FROM sales
    """
    with sqlite3.connect(DB_PATH) as connection:
        data = pd.read_sql_query(query, connection)

    data["sale_date"] = pd.to_datetime(data["sale_date"], errors="coerce")
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")
    data = data.dropna(subset=["sale_date", "product", "category", "quantity", "unit_price"])
    data["revenue"] = data["quantity"] * data["unit_price"]
    return data


def calculate_metrics(data: pd.DataFrame) -> dict:
    """Calculate metrics from the loaded sales data."""
    if data.empty:
        raise ValueError("The sales table contains no usable rows.")

    data["month"] = data["sale_date"].dt.to_period("M").astype(str)
    monthly = data.groupby("month", sort=True)["revenue"].sum()
    category = data.groupby("category", sort=False)["revenue"].sum().sort_values(ascending=False)
    products = data.groupby("product", sort=False)["revenue"].sum().sort_values(ascending=False)

    return {
        "total_revenue": data["revenue"].sum(),
        "total_quantity": data["quantity"].sum(),
        "average_check": data["revenue"].mean(),
        "monthly": monthly,
        "category": category,
        "products": products,
        "best_month": monthly.idxmax(),
        "best_category": category.idxmax(),
    }


def style_chart(title: str, xlabel: str, ylabel: str) -> None:
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()


def create_charts(metrics: dict) -> None:
    """Create all charts from calculated metrics."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    plt.figure(figsize=(10, 6))
    metrics["monthly"].plot(kind="bar", color="#4C78A8")
    style_chart("Выручка по месяцам", "Месяц", "Выручка")
    plt.savefig(CHARTS_DIR / "monthly_revenue.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 6))
    metrics["category"].plot(kind="bar", color="#F2A93B")
    style_chart("Выручка по категориям", "Категория", "Выручка")
    plt.savefig(CHARTS_DIR / "revenue_by_category.png", dpi=150)
    plt.close()

    top_products = metrics["products"].head(10)
    plt.figure(figsize=(10, 6))
    top_products.sort_values().plot(kind="barh", color="#59A14F")
    style_chart("Топ-10 товаров по выручке", "Выручка", "Товар")
    plt.savefig(CHARTS_DIR / "top_products.png", dpi=150, bbox_inches="tight")
    plt.close()


def format_number(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ")


def print_results(metrics: dict) -> None:
    print("Результаты анализа продаж")
    print(f"Общая выручка: {format_number(metrics['total_revenue'])}")
    print(f"Продано единиц: {format_number(metrics['total_quantity'])}")
    print(f"Средняя выручка с продажи: {format_number(metrics['average_check'])}")
    print(f"Лучший месяц: {metrics['best_month']}")
    print(f"Лучшая категория: {metrics['best_category']}")
    print(f"Графики сохранены в: {CHARTS_DIR}")


def main() -> None:
    data = load_sales()
    metrics = calculate_metrics(data)
    create_charts(metrics)
    print_results(metrics)


if __name__ == "__main__":
    main()
