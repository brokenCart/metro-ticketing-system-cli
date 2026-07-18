# 🚇 Metro Ticketing System CLI

A command-line metro ticketing system built in Python that models a multi-line metro network, computes shortest-path routes using BFS, and generates an interactive network graph. Built as a recruitment task for the **Department of Visual Media (DVM)**, BITS Pilani.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Station Network** | Models a real-world-inspired metro network with multiple intersecting lines |
| **Shortest Path Routing** | Uses BFS to find the optimal route between any two stations |
| **Ticket Purchasing** | Buy tickets with auto-generated unique IDs and distance-based pricing (₹10/station) |
| **Journey Instructions** | Step-by-step directions including line changes at interchange stations |
| **Network Visualization** | Renders a color-coded, multi-edge graph of the entire metro network using `matplotlib` and `networkx` |
| **Persistent Tickets** | Purchased tickets are saved to disk and restored on next launch |
| **Rich Terminal UI** | Styled output with colors and formatting via the `rich` library |

---

## 📂 Project Structure

```
metro-ticketing-system-cli/
├── main.py              # Entry point — CLI menu, graph drawing, user interaction
├── metro.py             # Core models — Station, Line, Ticket classes + BFS logic
├── requirements.txt     # Python dependencies
└── data/
    ├── stations.csv     # Station definitions (id, name)
    ├── lines.csv        # Line-station mappings with colors and ordering
    └── tickets.csv      # Persisted purchased tickets
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A graphical environment (for the `matplotlib` network map window)

### Installation

```bash
git clone https://github.com/brokenCart/metro-ticketing-system-cli.git
cd metro-ticketing-system-cli

python -m venv venv
source venv/bin/activate   # Mac / Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### Running

```bash
python main.py
```

---

## 🖥️ Usage

On launch you're presented with an interactive menu:

```
Welcome to Metro System!
(1) List of available stations.
(2) Purchase a ticket.
(3) Check your purchased tickets.
(4) Info about ticket journey.
(5) Look at a map of the station network.
(6) Exit.
```

### Buying a Ticket

1. Select option **2**.
2. Enter the origin station ID (e.g. `KG`).
3. Enter the destination station ID (e.g. `DWK`).
4. The system computes the shortest path, displays the price, and prompts for confirmation.
5. On purchase, a unique ticket ID is generated (e.g. `KG-DWK-EBY86HTC9X`) and the ticket is saved.

### Viewing Journey Info

Select option **4** and enter a ticket ID to see turn-by-turn journey instructions, including which lines to board and where to change.

### Network Map

Select option **5** to open a `matplotlib` window displaying the full metro graph with color-coded lines.

---

## 🗂️ Data Format

All data is stored as CSV in the `data/` directory.

### `stations.csv`

| Column | Description |
|---|---|
| `station_id` | Unique short identifier (e.g. `RC`, `KG`) |
| `station_name` | Human-readable name (e.g. `Rajiv Chowk`) |

### `lines.csv`

| Column | Description |
|---|---|
| `line_id` | Unique line identifier (e.g. `L2`) |
| `line_name` | Display name (e.g. `Yellow Line`) |
| `line_color` | Color used for rendering (e.g. `yellow`) |
| `station_id` | Station on this line |
| `position` | Order of the station on the line (1-indexed) |

### `tickets.csv`

| Column | Description |
|---|---|
| `ticket_id` | Auto-generated unique ID (`ORIGIN-DEST-RANDOM`) |
| `origin_id` | Origin station ID |
| `destination_id` | Destination station ID |

---

## 🏗️ Architecture

### Core Classes (`metro.py`)

- **`Station`** — Represents a metro station. Maintains a set of neighbouring stations and the lines passing through it. Loaded from `stations.csv`.
- **`Line`** — Represents a metro line with an ordered list of stations. On load, automatically connects adjacent stations as neighbours.
- **`Ticket`** — Represents a purchased ticket. Computes the shortest path via **BFS**, calculates pricing at ₹10 per station hop, and generates journey instructions that account for line changes at interchanges.

### Pathfinding

The shortest path between two stations is computed using **Breadth-First Search (BFS)** over the station adjacency graph. Since all edges have equal weight (one station hop = ₹10), BFS guarantees the optimal route.

### Graph Visualization

The network map is built with `networkx.MultiGraph` to support parallel edges (multiple lines between two stations). Each line is drawn as a separate curved arc with its designated color, making interchange stations and overlapping routes clearly visible.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3** | Core language |
| **matplotlib** | Network graph rendering |
| **networkx** | Graph data structure and layout algorithms |
| **rich** | Styled terminal output (colors, bold, italic) |

---
