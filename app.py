import flet as ft
import os

from granasimples.core.database import init_db
from granasimples.core.seed import seed_database
from granasimples.ui.app_view import GranaSimplesApp


def main(page: ft.Page) -> None:
    init_db()
    seed_database(os.getenv("GRANASIMPLES_SEED_MODE", "prod"))
    GranaSimplesApp(page).build()


if __name__ == "__main__":
    ft.app(target=main)
