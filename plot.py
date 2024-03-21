import pandas as pd
import matplotlib.pyplot as plt

# data of format id,x,y
df = pd.read_csv("pos.csv")
print(df.head())

df = df[df['floorNumber'] == 1]
length = 228.30688
width = 346.92673
height = 13.0
offsetX = 14.67
offsetY = 21.18
imageWidth = 4162
imageHeight = 2739

df = df[df['confidence'] > 100]

# collect data for each id
ids = df['id'].unique()

# filter out the ids that are stationary (don't move)
ids = [id for id in ids if len(df[df['id'] == id]) > 10]

plt.imshow(plt.imread('floor1.png'))

#ids = ids[200:220]
for id in ids:
    data = df[df['id'] == id]
    datax = data['x'].rolling(window=1).mean()
    datay = data['y'].rolling(window=1).mean()
    
    datax = (datax + offsetX) / (width + 2 * offsetX) * imageWidth
    datay = (datay + offsetY) / (length + 2 * offsetY) * imageHeight
    plt.plot(datax, datay, label=id)

plt.savefig('plot.png')

