import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import json
import schedule
import time
from datetime import datetime
from pprint import pprint



# Load configuration
def load_config(file):
    with open(file, 'r') as f:
        config = json.load(f)
    return config


# Configuration
config_file = 'config.json'
config = load_config(config_file)
database_file = config['database_location']


# Send email notification
def send_email(subject, body):    
    # SMTP settings
    smtp_host = config['smtp']['host']
    smtp_port = config['smtp']['port']
    smtp_username = config['smtp']['username']
    smtp_password = config['smtp']['password']
    sender_email = config['smtp']['sender_email']
    receiver_email = config['smtp']['receiver_email']

    # Create a multipart email message
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email

    # Attach the body of the email
    body_text = MIMEText(body, 'plain')
    message.attach(body_text)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print("Error sending email:", str(e))
        

# Send push notification
def send_push_notification(message):
    
    # FCM server key
    fcm_server_key = config['fcm']['server_key']

    # FCM API URL
    fcm_api_url = 'https://fcm.googleapis.com/fcm/send'

    # Device registration token
    device_token = config['fcm']['device_token']

    # Payload for the push notification
    payload = {
        'notification': {
            'title': 'Website Monitoring',
            'body': message
        },
        'to': device_token
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + fcm_server_key
    }

    try:
        # Send the HTTP POST request to FCM API
        response = requests.post(fcm_api_url, json=payload, headers=headers)

        if response.status_code == 200:
            print("Push notification sent successfully!")
        else:
            print("Failed to send push notification. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error sending push notification:", str(e))


# Log data to SQLite database
def log_to_database(timestamp, url, response):
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, url, response) VALUES (?, ?, ?)", (timestamp, url, response))
    conn.commit()
    conn.close()

# Log incident to SQLite database
def log_incident(timestamp, url, response):
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    c.execute(
            "INSERT INTO incidents (timestamp, url, response) VALUES (?, ?, ?)",
            (timestamp, url, response)
            )
    conn.commit()
    conn.close()
    #send_email("Incident Detected", f"An incident occurred for URL: {url}\nResponse: {response}")
    #send_push_notification(f"Incident detected for URL: {url}")


# Monitor URLs
def monitor_urls():
    c = load_config(config_file)
    urls = c['urls']

    for url in urls:
        try:
            response = requests.get(url)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_to_database(timestamp, url, response.status_code)
            if response.status_code != 200:
                print(f"An incident occurred for URL: {url}")
                log_incident(timestamp, url, response.status_code)
        except requests.exceptions.RequestException as e:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"An incident occurred for URL: {url}")
            log_to_database(timestamp, url, str(e))
            log_incident(timestamp, url, str(e))


# Main function
def main():

    # Initialize the database
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Create logs table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (timestamp TEXT, url TEXT, response TEXT)''')

    # Create incidents table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS incidents
                 (timestamp TEXT, url TEXT, response TEXT)''')

    conn.commit()
    conn.close()

    # Run first monitoring
    monitor_urls()

    # Schedule URL monitoring
    c = load_config(config_file)
    refresh_interval = c['refresh_interval']
    schedule.every(refresh_interval).seconds.do(monitor_urls)

    # Run the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
