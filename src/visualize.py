import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

records = {}

with open("outputs/flight_metrics.jsonl") as f:
    for line in f:
        key, value = line.strip().split("\t")
        carrier, metric = json.loads(key)
        records.setdefault(carrier, {})[metric] = json.loads(value)

df = pd.DataFrame.from_dict(records, orient="index").fillna(0)
df.index.name = "Airline"

df["Average_Departure_Delay"] = (
    df["departure_delay"] / df["recorded_departures"]
)

df["On_Time_Percentage"] = (
    df["on_time"] / df["recorded_departures"] * 100
)

df["Missing_Departure_Percentage"] = (
    df["missing_departure"] / df["total_flights"] * 100
)

df.to_csv("outputs/airline_summary.csv")

charts = [
    ("total_flights", "Total Flights by Airline", "Flights", "flight_volume.png"),
    ("Average_Departure_Delay", "Average Departure Delay", "Minutes", "departure_delay.png"),
    ("On_Time_Percentage", "On-Time Departure Percentage", "Percentage", "punctuality.png"),
    ("Missing_Departure_Percentage", "Missing Departure Percentage", "Percentage", "missing_departures.png")
]

for column, title, ylabel, filename in charts:
    plt.figure(figsize=(12, 6))
    df[column].sort_values(ascending=False).plot(kind="bar", color="steelblue")
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Airline")
    plt.tight_layout()
    plt.savefig("outputs/" + filename, dpi=150)
    plt.close()

print(df.round(2).to_string())
print("\nAnalysis completed successfully!")
