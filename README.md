# 🚇 Metro Ticketing System
A Python command-line application that simulates a metro ticketing system with shortest-path route calculation, fare computation, journey instructions, CSV-based persistence, and network visualization.

## Features
- View available stations
- Purchase tickets
- Shortest path calculation (BFS)
- Fare calculation
- Journey instructions with line changes
- Persistent ticket storage (CSV)
- Network graph visualization

## Installation
```bash
git clone https://github.com/brokenCart/metro_ticketing_system_cli.git
cd metro_ticketing_system_cli
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Project Structure
```
.
├── data
│   ├── lines.csv
│   ├── stations.csv
│   └── tickets.csv
├── main.py
├── metro.py
├── README.md
└── requirements.txt
```
> The `data/` directory contains sample datasets required to run the application.
`data/tickets.csv` stores records of purchased tickets.
