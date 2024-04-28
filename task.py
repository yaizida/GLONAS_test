import math

import requests


class VehicleManager:
    def __init__(self):
        self.url = 'https://test.tspb.su/test-task/vehicles'

    def get_vehicles(self) -> list:
        response = requests.get(self.url)
        vehicles = response.json()
        return [self.vehicle_to_string(vehicle) for vehicle in vehicles]

    def vehicle_to_string(self, vehicle) -> list:
        return '<Vechicle: {} {} {} {} {}>'.format(
            vehicle['name'],
            vehicle['model'],
            vehicle['color'],
            vehicle['year'],
            vehicle['price'],
        )

    def filter_vehicles(self, params: dict) -> list:
        vechiles = []
        for vechile in self.get_vehicles():
            for param in params.values():
                if param in vechile:
                    vechiles.append(vechile)
        return vechiles

    def get_vehicle(self, id: int) -> str:
        response = requests.get(self.url + '/' + str(id))
        return self.vehicle_to_string(response.json())

    def append_vehicle(self, vehicle: dict) -> None:
        requests.post(self.url, json=vehicle)

    def change_vehicle(self, id: int, vehicle: dict) -> None:
        requests.put(self.url + '/' + str(id), json=vehicle)

    def delete_vehicle(self, id: int) -> None:
        requests.delete(self.url + '/' + str(id))

    def distance(self, coordinates1: tuple, coordinates2: tuple) -> int:
        lon1, lat1, lon2, lat2 = map(math.radians, [coordinates1[0],
                                                    coordinates1[1],
                                                    coordinates2[0],
                                                    coordinates2[1]
                                                    ]
                                     )
        # haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (math.sin(dlat/2)**2 + math.cos(lat1) *
             math.cos(lat2) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        # Радиус Земли в километрах - равен 6371
        dist = 6371000 * c
        return dist

    def get_all_coordinates(self) -> list:
        all_vehicles = requests.get(self.url).json()
        list_coordinates = []
        for i in all_vehicles:
            list_coordinates.append(
                {'id': i['id'],
                 'lat': i['latitude'],
                 'lon': i['longitude']}
            )
        return list_coordinates

    def nearest_vehicle(self, target_id: int):
        data = self.get_all_coordinates()
        id_to_data = {d['id']: d for d in data}
        target_machine = id_to_data[target_id]
        target_lat = target_machine['lat']
        target_lon = target_machine['lon']
        nearest_object = min(
            data, key=lambda obj: self.distance(
                (target_lat, target_lon),
                (obj['lat'], obj['lon']))
            )
        return nearest_object


vechile = VehicleManager()

# print(vechile.get_vehicles())
# print(vechile.filter_vehicles(params={'name': 'BMW'}))
# print(vechile.get_vehicle(5))

print(vechile.nearest_vehicle(5))
