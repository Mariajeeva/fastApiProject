from http.client import HTTPException

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
from datetime import datetime, timedelta, time

app = FastAPI()

# In-memory storage for alarms (in a real app, you would use a database)
alarms = []

class Alarm(BaseModel):
    time: datetime

@app.post("/set_alarm/")
def set_alarm(hour: int, minute: int):
    global alarm_time
    try:
        alarm_time = time(hour=hour, minute=minute)
        return {"message": f"Alarm set for {hour}:{minute}"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format")
@app.get("/check_alarms/")
async def check_alarms():
    current_time = datetime.now()
    triggered_alarms = []
    while alarms and alarms[0] <= current_time:
        triggered_alarms.append(alarms.pop(0))
    if triggered_alarms:
        return {"message": "Triggered alarms", "alarms": triggered_alarms}
    else:
        return {"message": "No alarms triggered"}

async def background_task():
    while True:
        await asyncio.sleep(1)  # Check every second
        current_time = datetime.now()
        triggered_alarms = []
        while alarms and alarms[0] <= current_time:
            triggered_alarms.append(alarms.pop(0))
        if triggered_alarms:
            print("Triggered alarms:", triggered_alarms)  # Replace with actual notification logic

def startup_event():
    asyncio.create_task(background_task())

def shutdown_event():
    print("Shutting down, stopping background task if any...")

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
