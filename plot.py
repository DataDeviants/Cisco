import pandas as pd
import matplotlib.pyplot as plt

# data of format id,x,y
df = pd.read_csv("pos.csv")
print(df.head())

# collect data for each id
ids = df['id'].unique()

# filter out the ids that are stationary (don't move)
ids = [id for id in ids if len(df[df['id'] == id]) > 10]

ids = ids[200:201]
for id in ids:
    data = df[df['id'] == id]
    plt.plot(data['x'], data['y'], label=id)

plt.savefig('plot.svg')

