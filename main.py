from dataclasses import dataclass
import requests

production_types = {
    '1223': 'brown-coal',
    '1224': 'nuclear',
    '1225': 'wind-offshore',
    '1226': 'hydro',
    '1227': 'misc-conventional',
    '1228': 'misc-renewable',
    '4066': 'biomass',
    '4067': 'wind-onshore',
    '4068': 'photovoltaic',
    '4069': 'hard-coal',
    '4070': 'pumped-storage',
    '4071': 'natural-gas'
}

# TODO: Also add consumption
consumption_types = {
    '410': 'total',
    '4359': 'residual',
    '4387': 'pumped-storage'
}

countries = [
    'DE',
    'AT',
    'LU'
]


@dataclass
class Value:
    timestamp: int
    value: float


def get_last_value(energy_filter, country_filter):
    r = requests.get(f"https://www.smard.de/app/chart_data/{energy_filter}/{country_filter}/index_quarterhour.json")
    r.raise_for_status()
    last_timestamp = r.json()['timestamps'][-1]

    r = requests.get(f"https://www.smard.de/app/chart_data/{energy_filter}/{country_filter}/{energy_filter}_{country_filter}_quarterhour_{last_timestamp}.json")
    r.raise_for_status()
    tuples = list(filter(lambda x: x[1] is not None, r.json()['series']))
    last_value = tuples[-1][1]
    last_value_timestamp = int(tuples[-1][0])
    return Value(timestamp=last_value_timestamp, value=last_value)


def main():
    collect_data()


def collect_data():
    data = []
    for country in countries:
        print(f"Country: {country}")
        for energy_type_code, energy_type_name in production_types.items():
            print(f"Energy type: {energy_type_name}")
            last_value = get_last_value(energy_type_code, country)
            print(f"Country: {country}, Energy type: {energy_type_name}, Value: {last_value.value}")
            data.append({
                'country': country,
                'energy_type': energy_type_name,
                'value': last_value.value,
                'timestamp': last_value.timestamp,
                'type': 'production'
            })


if __name__ == '__main__':
    main()