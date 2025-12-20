import requests

class Notifier:
    def __init__(self, topic: str):
        self.url = f'https://ntfy.sh/{topic}'

    def send(self, message: str, title: str = "Security Alert", priority: str = "default", tags: str = None) -> bool:
        headers = {
            "Title": title,
            "Priority": priority,
        }
        
        if tags:
            headers["Tags"] = tags

        try:
            response = requests.post(
                self.url, 
                data=message.encode('utf-8'), 
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"[Error] Notification failed: {e}")
            return False

if __name__ == "__main__":

    notifier = Notifier("air-github")
    
    success = notifier.send(
        message="SSH Brute Force detected from 192.168.1.55!", 
        title="Intrusion Attempt", 
        priority="high",
        tags="rotating_light,lock"
    )
    
    if success:
        print("Test notification sent!")
    else:
        print("Test failed.")