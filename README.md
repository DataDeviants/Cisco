# About
This repository consists of three not (yet) fully compatible parts:

- Data streaming from the CISCO Spaces API and plotting (`load.py, plot.py`)
- Management of datastreams and preprocessing using Apache Kafka, which could be expanded to perform analysis itself (`src/kafka`)
- A mock application to simulated pedestrian data on a city plan (`city/`)

After finding the data quality and amount of interesting events to be lacking in the Firehose API data, we opted for the third approach.

Additionally, we explored the use of ML Solutions, in particular Autoencoders, using code from this repository: https://github.com/LU15W1R7H/abm-dynamics-viz
