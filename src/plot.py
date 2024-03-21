import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("res/pos.csv")
print(df.head())

df = df[df['floorNumber'] == 1]
length = 228.30688
width = 346.92673
height = 13.0
offsetX = 14.67
offsetY = 21.18
imageWidth = 4162
imageHeight = 2739

df = df[df['confidence'] < 100]

# collect data for each id
ids = df['id'].unique()


#ids = ids[200:220]
for id in ids:
  data = df[df['id'] == id]
  datax = data['x'].rolling(window=5).mean()
  datay = data['y'].rolling(window=5).mean()
  
  datax = (datax + offsetX) / (width + 2 * offsetX) * imageWidth
  datay = (datay + offsetY) / (length + 2 * offsetY) * imageHeight
  plt.plot(datax, datay, label=id)

plt.imshow(plt.imread('res/floor1.png'))
plt.savefig('plot.png', dpi=300)
