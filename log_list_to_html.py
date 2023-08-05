import pandas as pd
import webbrowser
from datetime import datetime, timedelta
import argparse


def highlight(val):
    if val == "up":
        color = "green"
    elif val == "down":
        color = "red"
    else:
        color = "white"
    return f"background-color: {color}"
    
def get_parser():
    parser = argparse.ArgumentParser(description='parameters to ')
    parser.add_argument('--days', default=5, type=int, help='Display logs for the last n-days from the current date (default value = 5)')
    args = parser.parse_args()
    return args

args = get_parser()

df = pd.read_csv('ping_log.csv')
# index sorting
df_sorted = df.sort_index(ascending=False)
cur_date = datetime.now()
days_delta = timedelta(days=args.days)
delta = (cur_date - days_delta).strftime('%Y-%m-%d')
df_sorted = df_sorted[(df_sorted['Date'] <= datetime.now().strftime('%Y-%m-%d')) & (df_sorted['Date'] >= delta)]

# applying the highlight function to a table
df_sorted.style.applymap(highlight)

html = df_sorted.style.applymap(highlight).render()

# writing to a file
with open('logs.html', 'w') as f:
    # adding styles for table design
    f.write('<style>table {font-size: 200%; \
            margin: auto; \
            text-align: center; \
            border-collapse: collapse;} \
            th, td { \
            border: 2px solid black; \
            padding: 15px; \
            } \
            body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; \
            }</style>')
    f.write(html)

# opening a file in the default browser
webbrowser.open('logs.html')
