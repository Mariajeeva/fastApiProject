from fastapi import FastAPI, HTTPException
from datetime import datetime, time
import asyncio
import threading
import winsound

app = FastAPI()

# Variable to store alarm time
alarm_time = None
sound_file = "samplealarm.WAV"
# Function to play alarm sound
def play_alarm():
    for _ in range(5):
        print("Alarm!")
        winsound.Beep(1000,500)
        # You can replace this with your preferred sound playing method
        # For simplicity, we'll just print "Alarm!" here
        # Example: winsound.Beep(1000, 500) for Windows

# Function to check and trigger alarm asynchronously
async def check_alarm_async():
    global alarm_time
    while True:
        if alarm_time is not None and datetime.now().time() >= alarm_time:
            play_alarm()
            alarm_time = None  # Reset alarm time once triggered
        await asyncio.sleep(1)  # Await asyncio.sleep inside an async function

# Start checking alarm in a separate thread
thread = threading.Thread(target=lambda: asyncio.run(check_alarm_async()))
thread.start()

# Endpoint to set alarm time
@app.get("/set_alarm")
def set_alarm(hour: int, minute: int):
    global alarm_time
    try:
        alarm_time = time(hour=hour, minute=minute)
        return {"message": f"Alarm set for {hour}:{minute}"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format")

# Endpoint to cancel alarm
@app.get("/cancel_alarm")
def cancel_alarm():
    global alarm_time
    alarm_time = None
    return {"message": "Alarm canceled"}

