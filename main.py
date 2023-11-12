import datetime
import typer
from rich.console import Console
from rich.table import Table
import pyfiglet as fg
import json
from json import JSONEncoder

console = Console()
app = typer.Typer()


@app.command(short_help="add an item")
def add(task: str, category: str):
    console.print(
        f"[italic]Adding [red]{task}[/] from [cyan]{category}[/] category[/italic]"
    )
    show()


@app.command(short_help="add a category color using hex color")
def category_add(name: str, color: str):
    file = open("categories.json", "r")
    categories = json.load(file)

    if name in categories.keys():
        console.print("[white on red]Color already exists![/]")
    else:
        new_color = {name: color}
        categories.update(new_color)

        with open("categories.json", "w") as f:
            json.dump(categories, f)
        console.print(f"Color [cyan]{color}[/] added succesfully")

    file.close()


@app.command()
def category_del(name: str):
    file = open("categories.json", "r")
    categories = json.load(file)

    if name in categories.keys() and name != "others":
        categories.pop(name)
        # categories.update(new_color)

        with open("categories.json", "w") as f:
            json.dump(categories, f)
        console.print(f"Cateogry [cyan]{name}[/] deleted succesfully!")
    else:
        console.print(
            f"[white on red]Category [yellow]{name}[/yellow] doesn't exists![/]"
        )

    file.close()


@app.command()
def complete(index: int):
    console.print(f"Completed task [cyan]{index}[/]")


@app.command()
def delete(index: int):
    console.print(f"Deleted item [cyan]{index}[/] from todos")


@app.command()
def show():
    completed = True

    tasks = [["Todo1", "none"], ["Todo2", "family"]]

    console.print("\n")

    figlet_text = fg.figlet_format("Todos")
    console.print(f"[yellow]{figlet_text}[/]")

    table = Table()

    table.add_column("#", justify="center", style="white", no_wrap=True)
    table.add_column("task", min_width=20)
    table.add_column("category", min_width=8, justify="center")
    table.add_column("date", justify="center")
    table.add_column("status", justify="center")

    file = open("categories.json")
    categories = json.load(file)

    for index, todo in enumerate(tasks, start=1):
        isDone = "Done ✅" if completed else "Open ❌"
        isDone_color = "green" if isDone == "Done ✅" else "red"

        category_color = (
            categories[todo[1]] if todo[1] in categories else categories["others"]
        )

        table.add_row(
            str(index),
            todo[0],
            f"[{category_color}]{todo[1]}[/]",
            "-",
            f"[{isDone_color}]{isDone}[/]",
        )

    # table.add_row("1", "Todo1", "game")
    # table.add_row("2", "Todo2", "music")

    console.print(table)

    print(datetime.datetime.now().isoformat())


### TASK Class ###
class Task:
    def __init__(
        self,
        todo,
        category,
        date_added=None,
        date_completed=None,
        completed=None,
        index=None,
    ):
        self.todo = todo
        self.category = category
        self.date_added = (
            date_added
            if date_added is not None
            else datetime.datetime.now().isoformat()
        )
        self.date_completed = date_completed if date_completed is not None else None
        self.completed = completed if completed is not None else 1
        self.index = index if index is not None else None

    def __repr__(self) -> str:
        return f"({self.task}, {self.category}, {self.date_added}, {self.date_completed}, {self.status}, {self.position})"


if __name__ == "__main__":
    app()
