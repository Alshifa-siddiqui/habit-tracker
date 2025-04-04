import pickle
import os

def create_file(name: str):
    file_name = f'{name}_dates.pkl'
    if os.path.exists(file_name):
        raise ValueError(f"pickle file for {name} already exists.")
    with open(file_name, 'wb') as o:
        pickle.dump([], o)


def save_dates(name: str, date: object):

    file_name = f"{name}_dates.pkl"
    try:
        with open(file_name, 'rb') as file:
            done_dates = pickle.load(file)
    except FileNotFoundError:
        done_dates = []
    if date not in done_dates:
        done_dates.append(date)
    with open(file_name, 'wb') as file:
        pickle.dump(done_dates, file)


def load_dates(name: str):
    file_name = f"{name}_dates.pkl"
    try:
        with open(file_name, 'rb') as file:
            done_dates = pickle.load(file)
        return done_dates
    except FileNotFoundError:
        return []


def delete_dates(name: str):
    file_name = f"{name}_dates.pkl"
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"File {file_name} has been deleted.")
    else:
        print(f"File {file_name} does not exist.")