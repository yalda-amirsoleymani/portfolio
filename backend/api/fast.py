from fastapi import FastAPI, Request
import uvicorn
from pathlib import Path
#from dotenv import load_dotenv
import os
import asyncpg

#env_path = Path(__file__).resolve().parent.parent / ".env"
#load_dotenv(dotenv_path=env_path)

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
app = FastAPI()

async def insert_reading(data):
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        host=POSTGRES_HOST
    )
    await conn.execute(
        '''
        INSERT INTO sensor_readings(co2, gas, smoke, temperature, battery_level)
        VALUES($1, $2, $3, $4, $5)
        ''',
        data["co2"],
        data["gas"],
        data["smoke"],
        data["temperature"],
        data["battery_level"]
    )
    await conn.close()

@app.post("/sensor-data")
async def receive_sensor_data(request: Request):
    data = await request.json()
    print(f"Received data: {data}")
    await insert_reading(data)
    return {"status": "received", "data": data}

@app.get("/readings")
async def get_readings():
    query = "SELECT * FROM sensor_readings;"
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        host=POSTGRES_HOST
    )
    readings = await conn.fetch(query)
    await conn.close()
    return [dict(row) for row in readings]



@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down ..... The DB connection is getting close!")

if __name__ == "__main__":
    uvicorn.run(app, host=POSTGRES_HOST, port=8000)

