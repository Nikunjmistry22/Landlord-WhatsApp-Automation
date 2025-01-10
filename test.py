import os
import time
import logging
import pyautogui
import pandas as pd
import pywhatkit as kit
from datetime import datetime

# Set up logging configuration
logging.basicConfig(filename='message_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def send_whatsapp_message(phone, message, delay=10):
    try:
        # Send message using PyWhatKit
        kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=delay, tab_close=True)
        time.sleep(2)
        pyautogui.press('enter')
        logging.info(f"Message sent to {phone}")  # Log the successful message send
        return True
    except Exception as e:
        logging.error(f"Error sending message to {phone}: {e}")  # Log the error
        return False

def process_csv_and_send_messages(input_csv='2025- Bills tenant paying.csv'):
    # Load the data from the CSV file
    data = pd.read_csv(input_csv)

    # Get current year for dynamic file naming
    current_year = datetime.now().year
    error_csv = f'error_{current_year}.csv'

    # If the error file doesn't exist, create it with headers
    if not os.path.exists(error_csv):
        error_data = pd.DataFrame(columns=data.columns)
        error_data.to_csv(error_csv, index=False)  # Create the CSV with headers if it doesn't exist
    else:
        error_data = pd.read_csv(error_csv)  # Load existing error data if the file exists

    # Loop through each row in the data
    for index, row in data.iterrows():
        phone = '+91' + str(row['Phone Number'])  # Format phone number
        room_no = row['Room No']
        rent_total = row['Rent 2025']
        Tax=row['Property Tax']
        Total=row['Total']
        # Create the message
        message = f"Bill of Room No {room_no} for {current_year}\nRent: {rent_total}\nProperty Tax: {Tax}\nTotal: {Total}\nRepair sales bill has not come yet.\nPlease pay at the earliest possible."

        # Try sending the message
        success = send_whatsapp_message(phone, message)

        # If message sending fails, log the error and append to error CSV
        if not success:
            row_data = {
                'Phone No': phone,
                'Room No': room_no,
                'Total': rent_total
            }
            error_data = error_data.append(row_data, ignore_index=True)
            error_data.to_csv(error_csv, index=False)  # Write the row to the error CSV
            logging.error(f"Error occurred with {phone}, added to {error_csv}")

        # Log the message details (successful attempt)
        else:
            logging.info(f"Sent message for Room No {room_no}, Rent: {rent_total}, Phone: {phone}")
        
        time.sleep(5)  # Delay between messages

    print("Processing complete. Any errors have been logged in the error file.")
    logging.info("Processing complete. Any errors have been logged in the error file.")

# Run the function to process the CSV and send messages
process_csv_and_send_messages()
