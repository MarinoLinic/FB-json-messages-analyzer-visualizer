import pandas as pd
import plotly.graph_objs as go
import json
import os
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

### Message count by hour
def plot_hourly_message_counts(grouped):
    # Create a new DataFrame with hour and count columns
    hour_counts = pd.DataFrame({'hour': [], 'sender_name': [], 'count': []})
    for name, group in grouped:
        hour_grouped = group['timestamp_ms'].apply(lambda x: pd.to_datetime(x, unit='ms').hour).value_counts().reset_index()
        hour_grouped.columns = ['hour', 'count']
        hour_grouped['sender_name'] = name
        hour_counts = pd.concat([hour_counts, hour_grouped], ignore_index=True)

    # Pivot the table
    pivot = hour_counts.pivot(index='hour', columns='sender_name', values='count').fillna(0)

    # Create the stacked bar chart
    data = []
    for user in pivot.columns:
        data.append(go.Bar(x=pivot.index, y=pivot[user], name=user))

    layout = go.Layout(
      barmode='stack',
      title='Hourly Message Counts by User',
      xaxis=dict(title='Hour (0-23)', type='category', categoryorder='array', categoryarray=[str(i) for i in range(24)]),
      yaxis=dict(title='Message Count')
    )

    fig = go.Figure(data=data, layout=layout)

    fig.write_image("Stats/Hourly_Messages.png", scale=10)
    fig.write_image("Stats/Hourly_Messages.svg", scale=1)



### Daily messages
# Plotly 
def plot_daily_messages(grouped_df):
    data = []
    for sender, group in grouped_df:
        # Convert timestamp_ms to datetime object and set it as the index
        group['timestamp'] = pd.to_datetime(group['timestamp_ms'], unit='ms')
        group = group.set_index('timestamp')
        
        # Resample by day and count number of messages
        daily_counts = group.resample('D').count()['content']
        data.append(go.Bar(x=daily_counts.index.date, y=daily_counts.values, name=sender))
        
    layout = go.Layout(title='Daily Messages by User', xaxis=dict(title='Date'), yaxis=dict(title='Number of Messages'), barmode='stack')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
        width=2500, 
        height=800, 
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    fig.write_image("Stats/Daily_Messages.png", scale=5)
    fig.write_image("Stats/Daily_Messages.svg", scale=1)

# Matplotlib
# def plot_daily_messages(grouped_df):
#     fig, ax = plt.subplots()
#     bottom = None  # Starting value for bottom of bar chart

#     for sender, group in grouped_df:
#         # Convert timestamp_ms to datetime object and set it as the index
#         group['timestamp'] = pd.to_datetime(group['timestamp_ms'], unit='ms')
#         group = group.set_index('timestamp')
        
#         # Resample by day and count number of messages
#         daily_counts = group.resample('D').count()['content']
        
#         # Plot bar chart with cumulative y-values
#         if bottom is None:
#             ax.bar(daily_counts.index.date, daily_counts.values, label=sender)
#             bottom = daily_counts.values
#         else:
#             ax.bar(daily_counts.index.date, daily_counts.values, bottom=bottom, label=sender)
#             bottom += daily_counts.values
            
#     ax.set_title('Daily Messages by User')
#     ax.set_xlabel('Date')
#     ax.set_ylabel('Number of Messages')
#     ax.legend()

#     fig.savefig("Stats/Daily_Messages.png", dpi=1000)
#     fig.savefig("Stats/Daily_Messages.svg", format='svg')



### Message percentage
def plot_message_counts(grouped_df):

    # Count the number of messages sent by each participant
    counts = grouped_df.size().sort_values(ascending=False)[:10]

    # Calculate the percentage of messages sent by each participant and round to 1 decimal place
    percentages = counts / counts.sum() * 100
    percentages = percentages.round(1)

    # Create a pie chart using Plotly
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', 'royalblue']

    fig = go.Figure(data=[go.Pie(
            labels=percentages.index,
            values=percentages.values,
            hoverinfo='label+percent+text',
            text=counts,
            textinfo='label+percent+text',
            textfont_size=15,
            marker=dict(colors=colors, line=dict(color='#000000', width=2)),
        )])

    fig.update_layout(
        title={
            'text': "Percentage of Messages Sent by User",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    fig.write_image("Stats/Percentage_Messages.png", scale=10)
    fig.write_image("Stats/Percentage_Messages.svg", scale=1)
