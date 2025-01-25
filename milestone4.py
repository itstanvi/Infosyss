import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


TWILIO_PHONE = os.getenv("TWILIO_PHONE")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TO_PHONE = os.getenv("TO_PHONE")


def send_whatsapp_notification(item, action, reason):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        body=f"Item: {item}\nAction: {action}\nReason: {reason}",
        from_=TWILIO_PHONE,
        to=TO_PHONE
    )
    
    print(f"Notification sent for {item}: {action} - {reason}")
    return message.sid


def analyze_inventory(file_path):
    import pandas as pd
    data = pd.read_csv(file_path)
    inventory_capacity_threshold = 0.8  
    alerts = []

    for _, row in data.iterrows():
        utilization = row["Quantity"] / row["Capacity"]
        if utilization > inventory_capacity_threshold:
            action = "SELL" if row["Risk Analysis"] == "High" else "MONITOR"
            alerts.append((row["Item"], action, f"High utilization ({utilization:.2f}) with {row['Risk Analysis']} risk"))
            send_whatsapp_notification(row["Item"], action, f"High utilization ({utilization:.2f}) with {row['Risk Analysis']} risk")
        elif utilization < 0.4: 
            alerts.append((row["Item"], "BUY", f"Low utilization ({utilization:.2f}), consider buying material"))
            send_whatsapp_notification(row["Item"], "BUY", f"Low utilization ({utilization:.2f}), consider buying material")
    
    return alerts


data = {
    "Item": ["microchips", "circuit boards", "semiconductors"],
    "Quantity": [850, 400, 120],
    "Capacity": [1000, 500, 300],
    "Risk Analysis": ["Medium", "High", "Low"],
    "Sentiment": ["Neutral", "Negative", "Positive"]
}


sample_file = "inventory_data.csv"
import pandas as pd
pd.DataFrame(data).to_csv(sample_file, index=False)


alerts = analyze_inventory(sample_file)


for alert in alerts:
    print(f"Item: {alert[0]}, Action: {alert[1]}, Reason: {alert[2]}")
