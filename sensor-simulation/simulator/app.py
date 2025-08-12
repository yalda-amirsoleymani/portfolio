import asyncio
import aiohttp
import random
import json
import logging
from  datetime import datetime

sensors = [
    {"id": "sensor1", "city": "city1", "house-number": "X54XX1", "room": "1"},
    {"id": "sensor2", "city": "city2", "house-number": "X54XX2", "room": "1"},
    {"id": "sensor3", "city": "city1", "house-number": "X54XX3", "room": "3"},
    {"id": "sensor4", "city": "city3", "house-number": "X54XX4", "room": "1"},
    {"id": "sensor5", "city": "city5", "house-number": "X54XX5", "room": "2"},
    {"id": "sensor6", "city": "city5", "house-number": "X54XX5", "room":"1"}
]
#api_url = "http://127.0.0.1:8000/sensor-data"
api_url = "http://sensor-api:8000/sensor-data"

def generate_sensor_data(sensor):
    return {
        "id": sensor["id"],
        "time": datetime.utcnow().isoformat(),
        "co2": round(random.uniform(300, 800), 2),
        "gas": round(random.uniform(0, 100), 2),
        "smoke": round(random.uniform(0, 100), 2),
        "temperature": round(random.uniform(18, 40), 1),
        "battery_level": round(random.uniform(30, 100), 1),

    }
async def  send_data(session,sensor):
    while True:
        data = generate_sensor_data(sensor)
        try:
            async with session.post(api_url, json = data) as response:
                status = response.status
#                print(f"{sensor["id"]} sent data: {data},  STATUS: {status}")
        except Exception as e:
            print(f"{sensor["id"]} faced ERROR: {e}")
        await asyncio.sleep(random.uniform(1,5))


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [send_data(session, sensor) for sensor in sensors]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

