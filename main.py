import pywhatkit as kit
import pyautogui
import time
import pandas as pd
from datetime import datetime
def send_whatsapp_message(phone, message, delay=10):
    try:
        # Open WhatsApp Web and send the message
        kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=delay, tab_close=True)
        
        # Wait a moment for the message window to open
        time.sleep(2)

        # Press "Enter" to send the message
        pyautogui.press('enter')
        print(f"Message sent to {phone}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Load the CSV file
data = pd.read_csv('2025.csv')  # CSV should have columns: phone, room No, total

# Loop through the data and send messages
for index, row in data.iterrows():
    phone = '+91'+str(row['Phone No'])  # Phone number as string (e.g., +91987654321)
    room_no = row['Room No']
    rent_total = row['Total']
    current_year=datetime.now().year
    # Format the message
    message = f"Your rent for Room No {room_no} is {rent_total} for {current_year}. Please make the payment at the earliest."
    
    # Send the message
    send_whatsapp_message(phone, message)
    time.sleep(5)  # Wait 5 seconds before sending the next message to avoid too many requests
