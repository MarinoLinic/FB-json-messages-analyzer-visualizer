import pandas as pd
import json
import os
from functions import plot_message_counts, plot_daily_messages, plot_hourly_message_counts

# Load the JSON file
with open('messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract messages and participants
messages = data['messages']
participants = {p['name'] for p in data['participants']}

# Initialize an empty list to store all messages for every user
messages_list = []

# Loop through the messages and add them to the list
for message in messages:
    sender = message['sender_name']
    timestamp = pd.to_datetime(message['timestamp_ms'], unit='ms')  # Convert to datetime format
    content = message.get('content', '')
    messages_list.append({'sender_name': sender, 'timestamp_ms': timestamp, 'content': content})

# Create a DataFrame from the list of messages
df = pd.DataFrame(messages_list)

# Group messages by sender
grouped = df.groupby('sender_name')

### Text Stats

# User stats
with open('user_stats.txt', 'w', encoding='utf-8') as f:
    for name, group in grouped:
        message_count = len(group)
        f.write(f"{name} sent {message_count} messages\n")
        
        # Find the day with the most messages
        day_counts = group.groupby(group['timestamp_ms'].dt.date).size()
        max_day = day_counts.idxmax()
        max_day_count = day_counts.max()
        f.write(f"Most active day: {max_day} ({max_day_count} messages)\n")
        
        # Find the hour with the most messages
        hour_counts = group.groupby(group['timestamp_ms'].dt.hour).size()
        max_hour = hour_counts.idxmax()
        max_hour_count = hour_counts.max()
        f.write(f"Most active hour: {max_hour}:00 ({max_hour_count} messages)\n")
        
        # Find the longest message
        longest_message = group.loc[group['content'].str.len().idxmax()]
        longest_message_word_count = len(longest_message['content'].split())
        longest_message_time = pd.to_datetime(longest_message['timestamp_ms'], unit='ms').strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"Longest message: {longest_message_word_count} words (sent on {longest_message_time})\n")

        
        # Count the total number of words and characters sent by each participant
        word_counts = group['content'].str.split().str.len().fillna(0)
        total_words = word_counts.sum()
        char_counts = group['content'].str.len().fillna(0)
        total_chars = char_counts.sum()
        f.write(f"Total words sent by {name}: {total_words}\n")
        f.write(f"Total characters sent by {name}: {total_chars}\n")
        
        # Add a divider after each user
        f.write("------------------------------\n")





### Graphs

if not os.path.exists("Stats"):
        os.makedirs("Stats")

plot_message_counts(grouped)
plot_daily_messages(grouped)
plot_hourly_message_counts(grouped)