import json
import random
import pandas as pd
import copy
random.seed(40)


class ShipmentVariationsGenerator:
    def __init__(self, drivers, input_file_path='../data/standard_routes.json', output_file_path='../data/all_variations.json', number_of_variations=20, add_item_max=3, general_variation = ['add_item', 'extend_routes', 'merchandise_variation','remove_trips']):
        self.drivers = drivers
        self.shipments = pd.read_json(input_file_path)
        self.file_path= output_file_path
        self.number_of_variations = number_of_variations
        self.general_variation = general_variation
        self.add_item_max = add_item_max
        self.cities = [
            'Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Bari', 'Catania',
            'Verona', 'Venice', 'Messina', 'Padua', 'Prato', 'Trieste', 'Brescia', 'Parma', 'Taranto', 'Modena',
            'Reggio Calabria', 'Reggio Emilia', 'Perugia', 'Ravenna', 'Livorno', 'Rimini', 'Cagliari', 'Foggia',
            'Ferrara', 'Salerno', 'Latina', 'Giugliano in Campania', 'Monza', 'Sassari', 'Bergamo', 'Pescara',
            'Trento', 'Forlì', 'Syracuse', 'Vicenza', 'Terni', 'Bolzano-Bozen', 'Piacenza', 'Novara', 'Ancona',
            'Udine', 'Andria', 'Arezzo', 'Cesena', 'Pesaro', 'Lecce', 'Barletta', 'La Spezia', 'Alessandria', 'Pisa',
            'Pistoia', 'Lucca', 'Guidonia Montecelio', 'Catanzaro', 'Treviso', 'Como', 'Brindisi', 'Busto Arsizio',
            'Grosseto', 'Torre del Greco'
        ]
        self.merchandise_list = [
            'milk', 'pens', 'butter', 'honey', 'tomatoes', 'bread', 'cheese', 'apples', 'oranges', 'fish', 'laptop',
            'mouse', 'keyboard', 'eggs', 'broccoli', 'razor', 'chicken', 'shampoo', 'toothpaste', 'socks', 'sweater',
            'toilet paper', 'yogurt', 'cereal', 'coffee', 'toothbrush', 'salad dressing', 'ketchup', 'paper towels',
            'soap', 'potatoes', 'carrots', 'onions', 'juice', 'chocolate', 'ice cream', 'garlic', 'shoes',
            'laundry detergent', 'dish soap', 'tuna', 'rice', 'spaghetti', 'beans', 'toilet cleaner', 'trash bags',
            'kitchen towels', 'light bulbs'
        ]

    def random_choice_excluding(self, lst, exclude_values):
        eligible_values = [value for value in lst if value not in exclude_values]

        if eligible_values:
            return random.choice(eligible_values)
        else:
            return None

    def find_cities_in_route(self, route):
        taken_route = []
        for path in route:
            if taken_route !=[]:
                taken_route.append(path['to'])
            else:
                taken_route.append(path['from'])
                taken_route.append(path['to'])
        return taken_route

    def item_lost(self, merchandise, length):
        for _ in range(random.randint(0, length)):
            if length > 5:
                key = list(merchandise.keys())[random.randint(0, length - 1)]
                del merchandise[key]
                length -= 1
        return merchandise

    def item_quantity_change(self, merchandise, length):
        changed_items = []
        for _ in range(random.randint(0, length)):
            key = list(merchandise.keys())[random.randint(1, length - 1)]
            changed_items.append(key)
            merchandise[key] = random.randint(1, 50)
        # print(f'changed items: {changed_items}')
        return merchandise

    def get_merchandise_in_trip(self, trip):
        return list(trip['merchandise'].keys())

    def variation_in_merchandise(self, route):
        index = random.randint(0, len(route) - 1)
        merchandise = route[index]['merchandise']
        length = len(merchandise)
        if random.randint(0, 1):
            merchandise = self.item_lost(merchandise, length)
        else:
            merchandise = self.item_quantity_change(merchandise, length)
        route[index]['merchandise'].update(merchandise)
        return route

    def variation_in_trip_merchandise(self, trip):
        merchandise = trip['merchandise']
        length = len(merchandise)
        if random.randint(0, 1):
            merchandise = self.item_lost(merchandise, length)
        else:
            merchandise = self.item_quantity_change(merchandise, length)
        trip['merchandise'].update(merchandise)
        return trip['merchandise']

    def add_item(self, route):
        for index in range(0, len(route)):
            current_merchandise = self.get_merchandise_in_trip(route[index])
            available_merchandise = [m for m in self.merchandise_list if m not in current_merchandise]

            new_items = {}
            if available_merchandise:
                selected_merchandise = random.sample(available_merchandise, random.randint(1, min(self.add_item_max,len(available_merchandise))))
                # print(f'items: {selected_merchandise} are added')
                new_items = {item: random.randint(1, 50) for item in selected_merchandise}
            else:
                new_items = self.variation_in_trip_merchandise(copy.deepcopy(route[index]))

            route[index]['merchandise'].update(new_items)
        return route

    def add_extra_route(self, route, index, cities_to_exclude):
        try:
            temp = route[index]['to']
            route[index]['to'] = self.random_choice_excluding(self.cities, cities_to_exclude)
            route.insert(index + 1, {'from': route[index]['to'], 'to': temp,
                                      'merchandise': self.variation_in_trip_merchandise(route[index])})
            return route
        except Exception as e:
            print(f'--------------------------------------{e}------------------------------')
            pass  # Continue working after catching the exception
    
    def remove_trip(self, route, trip_number_to_remove=None):
        if trip_number_to_remove is None:
            trip_number_to_remove = random.randint(1, min(3, len(route)))

        for _ in range(trip_number_to_remove):
            if len(route) < 2:
                return route

            if len(route) > 2 and random.choice([True, False]):
                # Remove the initial city
                del route[0]
            elif len(route) > 2 and random.choice([True, False]):
                # Remove the ending city            
                del route[-1]
            else:
                # remove the cities in between
                index = random.randint(0, len(route) - 2)
                if index < len(route) - 1:
                    route[index]['to'] = route[index + 1]['to']
                    route[index]['merchandise'] = route[index + 1]['merchandise']
                    del route[index + 1]

        return route
    
    def extend_routes(self, route, cities_to_exclude, number_of_extra_routes=None):
        if number_of_extra_routes is None:
            number_of_extra_routes = random.randint(1, 3)

        for _ in range(number_of_extra_routes):
            index = random.randint(0, len(route) - 1)
            route = self.add_extra_route(route, index, cities_to_exclude)

        return route

    def random_joined_variations(self, shipment, cities_to_exclude):
        route = shipment['route']
        variations = []

        for _ in range(self.number_of_variations):
            variation_type = random.choice(self.general_variation)

            if variation_type == 'add_item':
                variation = self.add_item(copy.deepcopy(route))

            elif variation_type == 'extend_routes':
                variation = self.extend_routes(copy.deepcopy(route), cities_to_exclude, number_of_extra_routes=random.randint(1, 3))
            
            elif variation_type == 'remove_trips':
                variation = self.remove_trip(copy.deepcopy(route), trip_number_to_remove=2)
        
            elif variation_type == 'merchandise_variation':
                variation = self.variation_in_merchandise(copy.deepcopy(route))

            variations.append(variation)

        return variations

    def generate_variations(self):
        all_variations = []
        id = 0

        for index, shipment in self.shipments.iterrows():
            cities_in_route = self.find_cities_in_route(shipment['route'])
            variations = self.random_joined_variations(shipment.copy(deep=True), cities_in_route)

            for i, variation in enumerate(variations):
                driver = random.choice(self.drivers)
                variation_with_sroute = {'id': f'a{id}', 'driver': driver, 'sroute': shipment['id'], 'route': variation}
                all_variations.append(variation_with_sroute)
                id += 1
                
        with open(self.file_path, 'w') as file:
            json.dump(all_variations, file, indent=2)

        return all_variations


