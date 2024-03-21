import pandas as pd
import matplotlib.pyplot as plt

# data of format id,x,y
df = pd.read_csv("pos.csv")
print(df.head())

# collect data for each id
ids = df['id'].unique()

# filter out the ids that are stationary (don't move)
ids = [id for id in ids if len(df[df['id'] == id]) > 10]


#ids = ids[200:250]
for id in ids:
    data = df[df['id'] == id]
    datax = data['x'].rolling(window=30).mean()
    datay = data['y'].rolling(window=30).mean()
    
    # scale x and y by 10
    datax = datax * 10
    datay = datay * 10
    plt.plot(datax, datay, label=id)

plt.imshow(plt.imread('floor1.png'))
plt.savefig('plot.png', dpi=300)
