# Metro Ticketing System CLI

A command-line metro ticketing system built in Python that models multi-line metro networks, calculates optimal routes, and provides interactive network visualization and ticket management.

## Description

The Metro Ticketing System CLI is a Python application designed to simulate metro network operations. It manages multi-line rail systems by constructing an adjacency graph of stations and lines, computing shortest paths between stations using Breadth-First Search (BFS), and determining distance-based fares.

The system supports persistent ticket storage, detailed journey breakdown with transfer instructions at interchange stations, and multi-edge graph rendering using NetworkX and Matplotlib to visually display the station network map.

## Key Features

- **Multi-Line Station Network**: Models interconnected metro lines with shared interchange stations.
- **Shortest Path Routing**: Employs Breadth-First Search (BFS) to find optimal travel routes between any two stations.
- **Ticket Generation and Persistence**: Generates unique ticket identifiers with distance-based pricing and persists purchase records to CSV.
- **Turn-by-Turn Journey Instructions**: Provides step-by-step navigation instructions including line transfers.
- **Network Visualization**: Renders an interactive, color-coded visual map of the metro network using NetworkX and Matplotlib.
- **Rich Terminal UI**: Displays formatted tables and styled output using the Rich terminal library.

## Installation

### Prerequisites

- Python 3.10 or higher
- A graphical environment (required for Matplotlib graph rendering window)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/brokenCart/metro-ticketing-system-cli.git
   cd metro-ticketing-system-cli
   ```

2. Create and activate a virtual environment:

   Linux / macOS:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Windows:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:

```bash
python main.py
```

### Menu Options

Upon running the application, an interactive menu will be displayed with the following options:

1. **List of available stations**: View all system stations and their unique identifiers.
2. **Purchase a ticket**: Select origin and destination stations to compute optimal route, fare, and issue a ticket.
3. **Check your purchased tickets**: Display all previously purchased and saved tickets.
4. **Info about ticket journey**: View turn-by-turn route and line transfer details for a specific ticket ID.
5. **Look at a map of the station network**: Render the graphical network diagram.
6. **Exit**: Terminate the application.
