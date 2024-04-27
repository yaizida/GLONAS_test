import requests

#response = requests.get('https://test.tspb.su/test-task/vehicles')
#print(response.text)


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


vechile = VehicleManager()
print(vechile.get_vehicles())
print(vechile.filter_vehicles(params={'name': 'BMW'}))
print(vechile.get_vehicle(5))
