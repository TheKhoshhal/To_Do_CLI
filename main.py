import datetime
import typer
from rich.console import Console
from rich.table import Table
import pyfiglet as fg
import json
from json import JSONEncoder
import re


# ### TASK Class ###
# class Task:
#     def __init__(
#         self,
#         todo,
#         category,
#         status=None,
#     ):
#         self.todo = todo
#         self.category = category
#         self.status = status if status is not None else 0


console = Console()
app = typer.Typer()


@app.command(short_help="add an item")
def add(task: str, category: str):
    console.print(
        f"[italic]Adding [red]{task}[/] from [cyan]{category}[/] category[/italic]"
    )

    added_todo = [task, category, "0"]

    tasks = []

    tasks_file = open("tasks.txt", "r")
    reading = tasks_file.readline()
    lines = re.split("/", reading)
    for line in lines:
        sub_task = re.split(",", line)
        tasks.append(sub_task)

    todo_array = [added_todo[0], added_todo[1], added_todo[2]]

    tasks.append(todo_array)
    tasks_file.close()

    with open("tasks.txt", "w") as f:
        items = []
        for array in tasks:
            new_array = ",".join(array)
            items.append(new_array)

        new_items = "/".join(items)
        if new_items[0] == "/":
            new_items = new_items[1:]
        f.writelines(new_items)

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
    tasks = []

    tasks_file = open("tasks.txt", "r")
    reading = tasks_file.readline()
    lines = re.split("/", reading)
    for line in lines:
        sub_task = re.split(",", line)
        tasks.append(sub_task)

    if tasks[index - 1][2] == "0":
        tasks[index - 1][2] = "1"
        console.print(f"Completed task [cyan]{index}[/]")
    else:
        console.print(
            f"[white on red]Task number [cyan]{index}[/cyan] already completed[/]"
        )

    tasks_file.close()

    with open("tasks.txt", "w") as f:
        items = []
        for array in tasks:
            new_array = ",".join(array)
            items.append(new_array)

        new_items = "/".join(items)
        if new_items[0] == "/":
            new_items = new_items[1:]
        f.writelines(new_items)

    show()


@app.command()
def open_task(index: int):
    tasks = []

    tasks_file = open("tasks.txt", "r")
    reading = tasks_file.readline()
    lines = re.split("/", reading)
    for line in lines:
        sub_task = re.split(",", line)
        tasks.append(sub_task)

    if tasks[index - 1][2] == "1":
        tasks[index - 1][2] = "0"
        console.print(f"Opened task [cyan]{index}[/]")
    else:
        console.print(
            f"[white on red]Task number [cyan]{index}[/cyan] is already open[/]"
        )

    tasks_file.close()

    with open("tasks.txt", "w") as f:
        items = []
        for array in tasks:
            new_array = ",".join(array)
            items.append(new_array)

        new_items = "/".join(items)
        if new_items[0] == "/":
            new_items = new_items[1:]
        f.writelines(new_items)

    show()


@app.command()
def delete(index: int):
    console.print(f"Deleted item [cyan]{index}[/] from todos")

    tasks = []

    tasks_file = open("tasks.txt", "r")
    reading = tasks_file.readline()
    lines = re.split("/", reading)
    for line in lines:
        sub_task = re.split(",", line)
        tasks.append(sub_task)

    tasks.pop(index - 1)

    tasks_file.close()

    with open("tasks.txt", "w") as f:
        items = []
        for array in tasks:
            new_array = ",".join(array)
            items.append(new_array)

        new_items = "/".join(items)
        if new_items[0] == "/":
            new_items = new_items[1:]
        f.writelines(new_items)

    show()


@app.command(short_help="Clears all tasks")
def clear_all():
    with open("tasks.txt", "w") as f:
        f.writelines("")


@app.command()
def show():
    # tasks = [("Todo1", "none"), ("Todo2", "family")]
    tasks = []

    tasks_file = open("tasks.txt", "r")
    reading = tasks_file.readline()
    lines = re.split("/", reading)
    for line in lines:
        sub_task = re.split(",", line)
        tasks.append(sub_task)

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
        completed = True
        if todo[2][0] == "1":
            completed = True
        elif todo[2][0] == "0":
            completed = False

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


if __name__ == "__main__":
    app()
