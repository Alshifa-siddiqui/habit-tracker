import click
from src.db import connect_db, create_table, complete_habit, delete_habit
from src.analytics import get_all_habits, get_habits_by_periodicity, get_longest_streak

@click.group()
def cli():
    pass

@cli.command()
@click.argument('name')
@click.argument('periodicity')
def add(name, periodicity):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO habits (name, periodicity) VALUES (?, ?)', (name, periodicity))
    conn.commit()
    click.echo(f"Habit '{name}' with '{periodicity}' periodicity added.")
    conn.close()

@cli.command()
def show():
    habits = get_all_habits()
    for habit in habits:
        click.echo(f"Habit: {habit[0]}, Periodicity: {habit[1]}, Streak: {habit[2]}")

@cli.command()
@click.argument('name')
def complete(name):
    complete_habit(name)

@cli.command()
@click.argument('name')
def delete(name):
    delete_habit(name)
    click.echo(f"Habit '{name}' deleted.")

@cli.command()
@click.argument('periodicity')
def show_by_period(periodicity):
    habits = get_habits_by_periodicity(periodicity)
    if habits:
        for habit in habits:
            click.echo(f"Habit: {habit[0]}")
    else:
        click.echo(f"No habits found for periodicity '{periodicity}'.")

@cli.command()
def longest_streak():
    habit = get_longest_streak()
    if habit and habit[0]:
        click.echo(f"Longest streak is '{habit[0]}' with {habit[1]} completions.")
    else:
        click.echo("No habits tracked yet.")
