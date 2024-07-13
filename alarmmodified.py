from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import asyncio
from datetime import datetime, timedelta
import winsound

app = FastAPI()

# In-memory storage for alarms (in a real app, you would use a database)
alarms = []

class Alarm(BaseModel):
    time: datetime
    tone: str  # Path to the custom alarm tone

@app.post("/set_alarm/")
async def set_alarm(alarm: Alarm):
    alarms.append(alarm)
    alarms.sort(key=lambda x: x.time)  # Sort alarms based on time
    return {"message": "Alarm set successfully"}

@app.get("/check_alarms/")
async def check_alarms():
    current_time = datetime.now()
    triggered_alarms = []
    while alarms and alarms[0].time <= current_time:
        triggered_alarms.append(alarms.pop(0))
    if triggered_alarms:
        for alarm in triggered_alarms:
            play_alarm_tone(alarm.tone)  # Play the custom alarm tone
        return {"message": "Triggered alarms", "alarms": triggered_alarms}
    else:
        return {"message": "No alarms triggered"}

def play_alarm_tone(tone_file):
    winsound.PlaySound("simplealarm.WAV", winsound.SND_FILENAME)

async def background_task():
    while True:
        await asyncio.sleep(1)  # Check every second
        current_time = datetime.now()
        triggered_alarms = []
        while alarms and alarms[0].time <= current_time:
            triggered_alarms.append(alarms.pop(0))
        if triggered_alarms:
            for alarm in triggered_alarms:
                play_alarm_tone(alarm.tone)  # Play the custom alarm tone
            print("Triggered alarms:", triggered_alarms)  # Replace with actual notification logic

def startup_event():
    asyncio.create_task(background_task())

app.add_event_handler("startup", startup_event)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
