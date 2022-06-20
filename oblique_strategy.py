from webbrowser import get
import tinydb
import click 
import random
from tinydb import where

'''
oblique strategies
random quotes to inspire

arguments
--random / -r 
generate a random quote

--save / -s <QUOTE>
save a quote to the database

--list / -l
list all quotes

--empty / -e
empty the database

--bulk / -b <filename>
load a file of quotes

'''
@click.command()
@click.option('--random', '-r', is_flag=True, help='generate a random quote')
@click.option('--save', '-s', help='save a quote to the database')  
@click.option('--list', '-l', is_flag=True, help='list all quotes')
@click.option('--empty', '-e', is_flag=True, help='empty the database') 
@click.option('--bulk', '-b', help='load a file of quotes')
@click.option('--custom', '-c', is_flag=True, help='generate a custom quote')

def oblique_strategy(random, save, list, empty, bulk, custom):

    if random:
        print(random_quote())
    elif save:
        save_quote(save)
        print("ok")
    elif list:
        print(list_quotes())
    elif empty:
        db = get_db()
        db.truncate()
        print("ok")
    elif bulk: 
        with open(bulk) as f:
            for line in f:
                save_quote(line.strip(), False)
        print("ok")
    elif custom:
        print(custom_wisdom())
    else:
        print("no arguments")

def get_db():
    return tinydb.TinyDB('oblique_strategy.json')

def random_quote(db=get_db()):
    quotes = db.search(where('custom') == False)
    return random.choice(quotes)['quote'].replace("\\n", "\n")   

def custom_wisdom(db=get_db()):
    
    quotes = db.search(where('custom') == True)
    return random.choice(quotes)['quote']

def save_quote(quote, custom=True, db=get_db()):
    db.insert({'quote': quote, 'custom': custom}) 

def list_quotes(db=get_db()):
    quotes = db.all()
    return "\n".join([q['quote'] for q in quotes])

if __name__ == "__main__":
    oblique_strategy() 