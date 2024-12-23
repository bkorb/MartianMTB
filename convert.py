import pandas as pd
import sqlite3
import pickle
import re

def to_float(entry):
    matches = re.match(r"(\d+\.*\d*)", entry)
    if matches:
        return float(matches.group(1))
    else:
        return float('nan')
    
def difficulty_to_int(diff):
    return ['Easy', 'Easy/Intermediate', 'Intermediate', 'Intermediate/Difficult', 'Difficult', 'Very Difficult'].index(diff)

with open('routes.pkl', 'rb') as f:
    routes = pickle.load(f)

for route in routes:
    details = route['details']
    route['length'] = to_float(details['length'])
    route['ascent'] = to_float(details['ascent'])
    route['descent'] = to_float(details['descent'])
    city_state = route['location']
    route['city'] = city_state.split(',')[0].strip()
    route['state'] = city_state.split(',')[1].strip()
    route['difficulty'] = difficulty_to_int(route['difficulty'])
    route.pop('details')
    route.pop('location')

df = pd.DataFrame(routes)
conn = sqlite3.connect('routes.db')
df.to_sql('routes', conn, if_exists='replace', index=False)
conn.close()