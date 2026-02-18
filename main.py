# Added this to display plots
import matplotlib
matplotlib.use("TKAgg")

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
from rich import print
from metro import Station, Ticket, Line, RANDOM_TICKET_ID_LENGTH

MAX_STATION_ID_LENGTH = 3

def view_stations():
    print(f"[bold]{"ID".ljust(MAX_STATION_ID_LENGTH)} | NAME[/bold]")
    for station in Station.all_stations.values():
        print(f"{station.id.ljust(MAX_STATION_ID_LENGTH)} | {station.name}")

def purchase_ticket(origin, destination):
    try:
        shortest_path = Ticket.calculate_shortest_path(origin, destination)
        price = Ticket.calculate_price(shortest_path)
        print(f"The ticket from {origin.name} to {destination.name} costs ₹{price}.")
        while True:
            option = input("Do you want to buy it? (Y/N): ").strip().upper()
            if option == "Y":
                ticket = Ticket(origin, destination, shortest_path, price)
                Ticket.all_tickets[ticket.id] = ticket
                Ticket.save_tickets("data/tickets.csv")
                return ticket
            elif option == "N":
                print("No ticket purchased.")
                return None
            else:
                print("Please enter a valid option.")
    except ValueError as e:
        print(e)
    return None

def view_purchased_tickets():
    tickets = Ticket.all_tickets.values()
    print(f"[bold]{"ID".ljust(MAX_STATION_ID_LENGTH * 2 + RANDOM_TICKET_ID_LENGTH + 2)} | ORIGIN | DESTINATION | PRICE[/bold]")
    for ticket in tickets:
        print(f"{ticket.id.ljust(MAX_STATION_ID_LENGTH * 2 + RANDOM_TICKET_ID_LENGTH + 2)} | {ticket.origin.id.ljust(len("ORIGIN"))} | {ticket.destination.id.ljust(len("DESTINATION"))} | ₹{ticket.price}")

def draw_station_graph():
    G = nx.MultiGraph()
    stations = list(Station.all_stations.values())
    G.add_nodes_from(map(lambda x: x.id, stations))

    for station in stations:
        for neighbour in station.neighbouring_stations:
            if G.has_edge(station.id, neighbour.id):
                continue
            common_lines = station.lines.intersection(neighbour.lines)
            for line in common_lines:
                edge_color = mcolors.hex2color(line.color)
                G.add_edge(station.id, neighbour.id, key=line.id, color=edge_color)
    
    pos = nx.spring_layout(G, k=0.5, iterations=40, seed=67)
    plt.figure(figsize=(16, 12))
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1000, edgecolors="gray")
    nx.draw_networkx_labels(G, pos, font_size=15, font_weight="bold")

    drawn_pairs = set()
    for u, v in G.edges(keys=False):
        pair_key = tuple(sorted((u, v)))
        if pair_key in drawn_pairs:
            continue
        
        all_edge_data = G.get_edge_data(u, v)
        arc_radius = 0.5
        num_edges = len(all_edge_data)
        current_rad = -(arc_radius * (num_edges - 1)) / 2

        for _, (_, data) in enumerate(all_edge_data.items()):
            rad_to_use = 0 if num_edges == 1 else current_rad
            nx.draw_networkx_edges(G, pos, edgelist=[pair_key], edge_color=data["color"], width=2.5, connectionstyle=f"arc3, rad={rad_to_use}")
            current_rad += arc_radius
        
        drawn_pairs.add(pair_key)

    plt.title("Metro Network Map", size=40)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    Station.read_stations("data/stations.csv")
    Line.load_lines("data/lines.csv")
    Ticket.load_tickets("data/tickets.csv")

    while True:
        print("\n[bold]Welcome to Metro System![/bold]")
        print("(1) List of available stations.")
        print("(2) Purchase a ticket.")
        print("(3) Check your purchased tickets.")
        print("(4) Info about ticket journey.")
        print("(5) Look at a map of the station network.")
        print("(6) Exit.")
        option = input("Enter a number from 1 to 6: ").strip()
        print()
        if option == "1":
            view_stations()
        elif option == "2":
            while True:
                try:
                    origin = Station.get_station(input("Enter the id of the origin station: ").strip().upper())
                    break
                except KeyError as e:
                    print(e)
                    continue
            
            while True:
                try:
                    destination = Station.get_station(input("Enter the id of the destination station: ").strip().upper())
                    break
                except KeyError as e:
                    print(e)
                    continue

            ticket = purchase_ticket(origin, destination)
            if ticket:
                print("Ticket purchased successfully!")
                print(ticket)
                ticket.print_journey()
        elif option == "3":
            view_purchased_tickets()
        elif option == "4":
            while True:
                try:
                    ticket = Ticket.get_ticket(input("Enter the ticket id: ").strip())
                    ticket.print_journey()
                    break
                except KeyError as e:
                    print(e)
        elif option == "5":
            draw_station_graph()
        elif option == "6":
            print("[italic]Bye![/italic]")
            break
        else:
            print("Enter a valid option!")
