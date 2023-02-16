import datapane as dp
import pandas as pd
import altair as alt
import duckdb
import altair as alt
import numpy as np

df = pd.read_csv("./chat_subset.csv")
filtered_chats = df[['text', 'fromUser.displayName', "sent"]].rename(columns={'fromUser.displayName':'name'})

con = duckdb.connect()

# create the table "my_table" from the DataFrame "my_df"
con.execute("CREATE TABLE my_table AS SELECT * FROM filtered_chats")

# insert into the table "my_table" from the DataFrame "my_df"
con.execute("INSERT INTO my_table SELECT * FROM filtered_chats")

def get_sample(params):
    display_name = params['display_name']
    sample = con.execute(f"SELECT * FROM my_table WHERE name = '{display_name}'").df()
    sample.style.set_properties(**{'text-align': 'left'})

    return [alt.Chart(sample).encode(x='day(sent):T', y='count()').mark_bar(opacity='0.8'), dp.Table(sample)]

v = dp.View(
  dp.Text("# Chat analysis app"),
  dp.Function(
      get_sample,
      controls=[
          dp.Choice(
              options=list(filtered_chats['name'].dropna().unique()),
              name='display_name',
          )
      ],
      target=dp.TargetMode.BELOW
  )
)

dp.serve(v)
