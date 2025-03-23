import discum
import json
import time
import fade
import logging
from datetime import datetime
from colorama import Fore, init


init(autoreset=True)

logging.basicConfig(filename='discord_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def print_gradient_text(text):
    gradient = fade.purplepink(text)
    print(gradient)

def main():
    ascii_art = """
    ░▒▓████████▓▒░▒▓█▓▒░              ░▒▓██████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░▒▓██████▓▒░
    ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░
    ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░
    ░▒▓██████▓▒░ ░▒▓█▓▒░             ░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░
    ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░
    ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░
    ░▒▓████████▓▒░▒▓████████▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓██████▓▒░
    """

    print_gradient_text(ascii_art)
    
    config = load_config()

    token = config.get('token') or input("Please enter the Discord token: ")
    channel_id = config.get('channel_id') or input("Please enter the channel ID: ")
    cooldowns = config.get('cooldowns', {})
    
    if not config.get('token') or not config.get('channel_id'):
        config['token'] = token
        config['channel_id'] = channel_id
        config['cooldowns'] = cooldowns
        save_config(config)

    bot = discum.Client(token=token)

    def send_message(channel_id, message):
        try:
            response = bot.sendMessage(channel_id, message)
            if response.status_code == 200:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"✅ Message sent successfully in {channel_id} at {current_time}!")
                logging.info(f"Message sent in {channel_id} at {current_time}.")
            else:
                print(f"❌ Failed to send (Code {response.status_code}). Check permissions or slowmode.")
                logging.warning(f"Failed to send message in {channel_id}. Status code: {response.status_code}")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            logging.error(f"Error occurred: {e}")
    
    while True:
        channel_id = input("Enter channel ID (or press Enter to use default): ") or config['channel_id']
        message = input("Enter the message to send: ")
        cooldown = int(input(f"Enter cooldown for channel {channel_id} (seconds): ") or cooldowns.get(channel_id, 5))
        
        cooldowns[channel_id] = cooldown
        config['cooldowns'] = cooldowns
        save_config(config)
        
        while True:
            send_message(channel_id, message)
            for i in range(cooldowns[channel_id], 0, -1):
                print(f"Next message in {i} seconds...", end='\r')
                time.sleep(1)
            print(" " * 30, end='\r')

if __name__ == "__main__":
    main()