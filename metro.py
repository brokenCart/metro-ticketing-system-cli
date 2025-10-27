import csv
import random
import string
from collections import deque
from rich import print

PRICE_PER_STATION = 10
CHARACTERS = string.ascii_uppercase + string.digits
RANDOM_TICKET_ID_LENGTH = 10

class Station:
    all_stations = {}
    def __init__(self, station_id, station_name):
        self.id = station_id
        self.name = station_name
        self.neighbouring_stations = set()
        self.lines = set()
        self.__class__.all_stations[self.id] = self
    
    def __repr__(self):
        return f"Station('{self.id}', '{self.name}')"
    
    @classmethod
    def get_station(cls, station_id):
        try:
            return cls.all_stations[station_id]
        except KeyError:
            raise KeyError(f"There is no such station with id '{station_id}'.")
    
    def add_neighbour(self, neighbouring_station):
        self.neighbouring_stations.add(neighbouring_station)
        neighbouring_station.neighbouring_stations.add(self)
    
    @classmethod
    def read_stations(cls, filename):
        try:
            with open(filename, "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    cls(row["station_id"], row["station_name"])
        except FileNotFoundError:
            print(f"File [bold]'{filename}'[/bold] doesn't exists.")
            exit()

class Ticket:
    all_tickets = {}
    def __init__(self, origin_station, destination_station, shortest_path, price):
        self.origin = origin_station
        self.destination = destination_station
        self.shortest_path = shortest_path

        if not self.shortest_path:
            raise ValueError(f"No such path exists between [bold]{self.origin.name}[/bold] to [bold]{self.destination.name}[/bold]!")

        self.price = price
        self.lines = self.__get_journey_instructions()

        while True:
            ticket_id = f"{self.origin.id}-{self.destination.id}-{''.join(random.choices(CHARACTERS, k=RANDOM_TICKET_ID_LENGTH))}"
            if ticket_id not in self.all_tickets:
                break

        self.id = ticket_id

    def __repr__(self):
        return f"Ticket({self.origin}, {self.destination}, {self.shortest_path}, {self.price})"

    def __str__(self):
        return f"ID: {self.id}, PRICE: ₹{self.price}, {self.origin.name} to {self.destination.name}"
    
    @classmethod
    def get_ticket(cls, ticket_id):
        try:
            return cls.all_tickets[ticket_id]
        except KeyError:
            raise KeyError(f"There is no such ticket with id '{ticket_id}'.")

    @staticmethod
    def calculate_shortest_path(origin, destination):
        # BFS
        if origin == destination:
            raise ValueError(f"Origin and destination cannot be same!")
        
        stations_queue = deque([origin])
        visited_stations = set([origin])
        path_tracker = {origin: None}

        while stations_queue:
            current_station = stations_queue.popleft()
            if current_station == destination:
                break
            for neighbour in current_station.neighbouring_stations:
                if neighbour not in visited_stations:
                    visited_stations.add(neighbour)
                    stations_queue.append(neighbour)
                    path_tracker[neighbour] = current_station
        
        if destination not in path_tracker:
            return None

        path = []
        while current_station:
            path.append(current_station)
            current_station = path_tracker[current_station]

        return path[::-1]

    @staticmethod
    def calculate_price(path):
        return PRICE_PER_STATION * (len(path) - 1)

    def __get_journey_instructions(self):
        lines = []
        current_line = None
        for i in range(len(self.shortest_path) - 1):
            station_a = self.shortest_path[i]
            station_b = self.shortest_path[i + 1]
            common_lines = station_a.lines.intersection(station_b.lines)
            if current_line not in common_lines:
                current_line = random.choice(list(common_lines))
            lines.append(current_line)
        return lines

    def print_journey(self):
        print(f"Board the [{self.lines[0].color}]{self.lines[0].name}[/{self.lines[0].color}] at [bold]{self.shortest_path[0].name}[/bold].")
        for i in range(1, len(self.lines)):
            if self.lines[i] != self.lines[i - 1]:
                print(f"At [bold]{self.shortest_path[i].name}[/bold], change to [{self.lines[i].color}]{self.lines[i].name}.[/{self.lines[i].color}]")
        print(f"You will arrive at [bold]{self.shortest_path[-1].name}[/bold].")

    @classmethod
    def load_tickets(cls, filename):
        try:
            with open(filename, "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    origin = Station.get_station(row["origin_id"])
                    destination = Station.get_station(row["destination_id"])
                    shortest_path = cls.calculate_shortest_path(origin, destination)
                    price = cls.calculate_price(shortest_path)
                    ticket = cls(origin, destination, shortest_path, price)
                    ticket.id = row["ticket_id"]
                    cls.all_tickets[ticket.id] = ticket
        except FileNotFoundError:
            print(f"File [bold]'{filename}'[/bold] doesn't exists.")
            exit()

    @classmethod
    def save_tickets(cls, filename):
        fieldnames = ["ticket_id", "origin_id", "destination_id"]
        with open(filename, "w", newline="") as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for ticket in cls.all_tickets.values():
                csv_writer.writerow({
                    "ticket_id": ticket.id,
                    "origin_id": ticket.origin.id,
                    "destination_id": ticket.destination.id
                })

class Line:
    all_lines = {}
    def __init__(self, line_id, line_name, line_color):
        self.id = line_id
        self.name = line_name
        self.color = line_color
        self.stations = []
        self.__class__.all_lines[self.id] = self
    
    def __repr__(self):
        return f"Line('{self.id}', '{self.name}', '{self.color}')"

    def add_station(self, station, position):
        self.stations.insert(position - 1, station)
    
    @classmethod
    def get_line(cls, line_id):
        try:
            return cls.all_lines[line_id]
        except KeyError:
            raise KeyError(f"There is no such line with id [bold]'{line_id}'[/bold].")
    
    @classmethod
    def load_lines(cls, filename):
        try:
            with open(filename, "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    line_id = row["line_id"]
                    if line_id not in cls.all_lines:
                        line = cls(line_id, row["line_name"], row["line_color"])
                    else:
                        line = cls.get_line(line_id)
                    station = Station.get_station(row["station_id"])
                    station.lines.add(line)
                    line.add_station(station, int(row["position"]))
            cls.__connect_stations()
        except FileNotFoundError:
            print(f"File [bold]'{filename}'[/bold] doesn't exists.")
            exit()
    
    @classmethod
    def __connect_stations(cls):
        for line in cls.all_lines.values():
            for i in range(len(line.stations) - 1):
                line.stations[i].add_neighbour(line.stations[i + 1])
