import json
from dataclasses import dataclass
from datetime import datetime
import paho.mqtt.client as mqtt

import requests
import os
import logging
import sys
from dotenv import load_dotenv
from time import sleep

load_dotenv()

broker = 'gcmb.io'
port = 8883
client_id = 'stefan/smard/data-generator/pub'
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWORD']

# Default interval is 5 minutes
interval = os.environ.get('INTERVAL', 60 * 5)

log_level = os.environ.get('LOG_LEVEL', 'INFO')
print("Using log level", log_level)

logger = logging.getLogger()
logger.setLevel(log_level)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


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

energy_types = [
    {
        'code': '1223',
        'name': 'brown-coal',
        'type': 'production'
    },
    {
        'code': '1224',
        'name': 'nuclear',
        'type': 'production'
    },
    {
        'code': '1225',
        'name': 'wind-offshore',
        'type': 'production'
    },
    {
        'code': '1226',
        'name': 'hydro',
        'type': 'production'

    },
    {
        'code': '1227',
        'name': 'misc-conventional',
        'type': 'production'
    },
    {
        'code': '1228',
        'name': 'misc-renewable',
        'type': 'production'
    },
    {
        'code': '4066',
        'name': 'biomass',
        'type': 'production'
    },
    {
        'code': '4067',
        'name': 'wind-onshore',
        'type': 'production'
    },
    {
        'code': '4068',
        'name': 'photovoltaic',
        'type': 'production'
    },
    {
        'code': '4069',
        'name': 'hard-coal',
        'type': 'production'
    },
    {
        'code': '4070',
        'name': 'pumped-storage',
        'type': 'production'
    },
    {
        'code': '4071',
        'name': 'natural-gas',
        'type': 'production'
    },
    {
        'code': '410',
        'name': 'total',
        'type': 'consumption'
    },
    {
        'code': '4359',
        'name': 'residual',
        'type': 'consumption'
    },
    {
        'code': '4387',
        'name': 'pumped-storage',
        'type': 'consumption'
    }
]

countries = [
    'DE',
    'AT',
    'LU'
]


@dataclass
class Value:
    timestamp: int
    value: float


def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            logger.info("Connected to MQTT Broker")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    mqtt_client = mqtt.Client(client_id=client_id,
                              callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.tls_set(ca_certs='/etc/ssl/certs/ca-certificates.crt')
    mqtt_client.username_pw_set(username, password)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = lambda client, userdata, disconnect_flags, reason_code, properties: logger.warning(
        f"Disconnected from MQTT Broker, return code {reason_code}")
    mqtt_client.connect(broker, port)
    return mqtt_client


def mqtt_publish(client, topic, msg):
    result = client.publish(topic, msg, retain=True)
    status = result[0]
    if status == 0:
        logger.debug(f"Sent '{msg}' to topic {topic}")
    else:
        logger.warning(f"Failed to send message to topic {topic}, reason: {status}")


def get_last_value(energy_filter, country_filter):
    r = requests.get(f"https://www.smard.de/app/chart_data/{energy_filter}/{country_filter}/index_quarterhour.json")
    r.raise_for_status()
    last_timestamp = r.json()['timestamps'][-1]

    r = requests.get(
        f"https://www.smard.de/app/chart_data/{energy_filter}/{country_filter}/{energy_filter}_{country_filter}_quarterhour_{last_timestamp}.json")
    r.raise_for_status()
    tuples = list(filter(lambda x: x[1] is not None, r.json()['series']))
    last_value = tuples[-1][1]
    last_value_timestamp = int(tuples[-1][0])
    return Value(timestamp=last_value_timestamp, value=last_value)


def main():
    mqtt_client = connect_mqtt()
    mqtt_client.loop_start()
    while True:
        count = 0
        data = collect_data()
        for entry in data:
            try:
                base_topic = f"stefan/smard/{entry['country']}/{entry['type']}/{entry['energy_type']}"
                topic = f"{base_topic}/value"
                payload = str(entry['value'])
                logger.info(f"Publishing to {topic}: {payload}")
                mqtt_publish(mqtt_client, topic, payload)
                count += 1

                # timestamp is unix milliseconds
                timestamp_iso8601 = datetime.fromtimestamp(entry['timestamp'] / 1000).isoformat() + 'Z'

                json_payload = {
                    'value': entry['value'],
                    'timestamp': timestamp_iso8601,
                    'resolution': '15m',
                    'unit': 'MWh'
                }

                json_topic = f"{base_topic}/json"
                logger.debug(f"Publishing to {json_topic}: {json_payload}")
                mqtt_publish(mqtt_client, json_topic, json.dumps(json_payload))
                count += 1
            except Exception as e:
                logger.error(f"Error publishing data: {e}")

        logger.info(f"Published {count} messages")
        sleep(interval)


def collect_data():
    data = []
    for country in countries:
        for energy_type in energy_types:
            try:
                name = energy_type['name']
                code = energy_type['code']
                production_or_consumption = energy_type['type']

                last_value = get_last_value(code, country)
                logger.info(f"Country: {country}, Energy type: {name}, Value: {last_value.value}")
                data.append({
                    'country': country,
                    'energy_type': name,
                    'value': last_value.value,
                    'timestamp': last_value.timestamp,
                    'type': production_or_consumption
                })
            except Exception as e:
                logger.error(f"Error for country {country} and energy type {energy_type}: {e}")

    return data


if __name__ == '__main__':
    main()