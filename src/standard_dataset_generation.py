import json
import random
random.seed(40)



class StandardRouteGenerator:
    def __init__(self, number_of_shipments=20, merchandise_size=5):
        # number of shipments = number of standard routes
        self.merchandise_size = merchandise_size
        self.number_of_shipments = number_of_shipments
        self.cities = ['Rome','Milan','Naples','Turin','Palermo','Genoa','Bologna','Florence','Bari','Catania','Verona','Venice','Messina','Padua','Prato','Trieste','Brescia','Parma','Taranto','Modena','Reggio Calabria','Reggio Emilia','Perugia','Ravenna','Livorno','Rimini','Cagliari','Foggia','Ferrara','Salerno','Latina','Giugliano in Campania','Monza','Sassari','Bergamo','Pescara','Trento','Forlì','Syracuse','Vicenza','Terni','Bolzano-Bozen','Piacenza','Novara','Ancona','Udine','Andria','Arezzo','Cesena','Pesaro','Lecce','Barletta','La Spezia','Alessandria','Pisa','Pistoia','Lucca','Guidonia Montecelio','Catanzaro','Treviso','Como','Brindisi','Busto Arsizio','Grosseto','Torre del Greco']
        self.merchandise_list = ['milk', 'pens', 'butter', 'honey', 'tomatoes', 'bread', 'cheese', 'apples', 'oranges', 'fish', 'laptop', 'mouse', 'keyboard', 'eggs', 'broccoli', 'razor', 'chicken', 'shampoo', 'toothpaste', 'socks', 'sweater', 'toilet paper', 'yogurt', 'cereal', 'coffee', 'toothbrush', 'salad dressing', 'ketchup', 'paper towels', 'soap', 'potatoes', 'carrots', 'onions', 'juice', 'chocolate', 'ice cream', 'garlic', 'shoes', 'laundry detergent', 'dish soap', 'tuna', 'rice', 'spaghetti', 'beans', 'toilet cleaner', 'trash bags', 'kitchen towels', 'light bulbs']

        self.shipments = []

    def generate_merchandise(self):
        selected_merchandise = random.sample(self.merchandise_list, random.randint(2, min(self.merchandise_size, len(self.merchandise_list))))
        return {item: random.randint(1, 50) for item in selected_merchandise}

    def generate_route(self, start, end):
        return {
            'from': start,
            'to': end,
            'merchandise': self.generate_merchandise()
        }

    def generate_shipment(self, id_prefix):
        route_sequence = random.sample(self.cities, random.randint(2, 5))
        return {
            'id': id_prefix,
            'route': [
                self.generate_route(route_sequence[i], route_sequence[i + 1]) for i in range(len(route_sequence) - 1)
            ]
        }

    def generate_shipments(self):
        for i in range(self.number_of_shipments):
            shipment = self.generate_shipment(f's{i}')
            self.shipments.append(shipment)

    def save_shipments_to_file(self, file_path='../data/standard_routes.json'):
        with open(file_path, 'w') as file:
            json.dump(self.shipments, file, indent=2)
        print(f"Generated {self.number_of_shipments} standard routes and stored in '{file_path}'")

