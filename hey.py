import requests
from playsound import playsound
import sys
import time
import colorama
def cookie_generator():
    import undetected_chromedriver as uc
    driver = uc.Chrome(headless=True,driver_executable_path='DataBase\chromedriver.exe')
    with driver:
        driver.get('https://pi.ai/talk')
        driver.add_cookie({'name' : '__Host-session', 'value' : 'ENTER YOUR HOST SESSION VALUE HERE IF YOU WANT TO CONTINUE THE CONVERSATION'})
        driver.refresh()
        cookies = driver.get_cookies()
        cookie_data = cookies
        # driver.quit()

    import json

# Initialize variables to store cookie values
    host_session_value = None
    cfm_value = None

    # Iterate through the cookie data list
    for cookie in cookie_data:
        if cookie['name'] == '__Host-session':
            host_session_value = cookie['value']
        elif cookie['name'] == '__cf_bm':
            cfm_value = cookie['value']

    # Check if both cookie values were found
    if host_session_value is not None and cfm_value is not None:
        # Create a dictionary to hold the cookie values
        cookies_dict = {
            "__Host-session": host_session_value,
            "__cf_bm": cfm_value
        }

        # Save the dictionary as JSON in a file
        with open('Data\\cookies.json', 'w') as file:
            json.dump(cookies_dict, file)
    else:
        print("Error: One or both cookie values were not found.")
#####################################################################################################################

def friday(que):
    import threading
    while True:
            
        import json

        with open('Data\\cookies.json', 'r') as json_file:
            data = json.load(json_file)
        

    # Extract the values
        # host_value = data.get('__Host-session')
        cfbm_value = data.get('__cf_bm')
        host = data.get("__Host-session")
        cookies = {"__Host-session":host , "__cf_bm": cfbm_value }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        json_data = {
            'text': que,
        }

        response = requests.post('https://pi.ai/api/chat', cookies=cookies, headers=headers, json=json_data,stream=True)
        # print(response.text,end="")
    
        if response.status_code == 403 or response.status_code == 401:
            cookie_generator()
            pass

        else:
            import json

            data = response.text

            lines = data.split("\n")


            for i in range(len(lines)):
                if "event: message" in lines[i]:
                    message_json = lines[i+1].replace("data: ", "")
                    message_data = json.loads(message_json)
                    extracted_part = message_data["sid"]
                    
                    params = {
                        'messageSid': extracted_part,
                        'voice': 'voice5',
                        'mode': 'eager',
                    }
                    response = requests.get('https://pi.ai/api/chat/voice', params=params, headers=headers,cookies=cookies,stream=True)
                    audio_bytes = response.content
                elif "event: partial" in lines[i]:
                    partial_json = lines[i+1].replace("data: ", "")
                    partial_data = json.loads(partial_json)
                    partial_text = partial_data["text"]
                    # print("Friday:", partial_text)

            # events = response.text.strip().split('\nevent: ')
            def Text(partial_text):
                        for char in partial_text:
                                print(colorama.Fore.BLUE+char, end='', flush=True)
                                time.sleep(0.05)
                                # sys.stdout.write(char)
                                # sys.stdout.flush()
                        # print("Jarvis :",partial_text)
            def audio(audio_bytes):
                        import os
                        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
                        import pygame
                        import io

                        # Initialize pygame
                        pygame.mixer.init()

                        # Your audio data in bytes format
                        audio_bytes = response.content  # Replace with your actual audio bytes

                        # Create a BytesIO object from the audio data
                        audio_stream = io.BytesIO(audio_bytes)

                        # Load the audio stream
                        audio = pygame.mixer.Sound(audio_stream)

                        # Play the audio
                        audio.play()
            threading.Thread(target=Text,args = [partial_text]).start()
            threading.Thread(target=audio,args = [audio_bytes]).start()


            # threading.Thread(target=Text,args = [events]).start()
            break
