import winsound
import time

def alarm_clock(alarm_time):
    while True:
        current_time = time.strftime('%H:%M')
        if current_time == alarm_time:
            print("Wake up!")
            # Play beep sound
            for _ in range(5):  # Beep sound 5 times
                winsound.Beep(1000, 200)  # Frequency = 1000 Hz, Duration = 200 ms
            break
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    alarm_time = input("Enter the alarm time (HH:MM in 24-hour format): ")
    alarm_clock(alarm_time)
