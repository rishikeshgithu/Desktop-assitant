import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import random

def recognize_and_perform_action():
    # Initialize the speech recognition object
    r = sr.Recognizer()

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    browser = None  # Initialize browser outside the loop

    while True:
        with sr.Microphone() as source:
            print("Please start speaking.")
            audio_text = r.listen(source)
            print("Recording finished. Recognizing...")

            try:
                # Convert speech to text
                recognized_text = r.recognize_google(audio_text)
                print("You: " + recognized_text)
                if "hi" in recognized_text.lower():
                      responses = ["Hi, how can I assist you?", "Hello, what do you need help with?", "Hey there, what can I do for you?"]
                      response = random.choice(responses)

                      engine.say(response)
                      engine.runAndWait()

                if "how are you" in recognized_text.lower():
                      responses = ["i am fine,what do u want me to do?","i am good,what do u want me to do?","i am great,what do u want me to do?"]
                      response = random.choice(responses)

                      engine.say(response)
                      engine.runAndWait()

                if "what is your name" in recognized_text.lower():
                      responses = ["i am your desktop assistant","i am wonderfull desktop assistant"]
                      response = random.choice(responses)
                      engine.say(response)
                      engine.runAndWait()
                
                if "what can you do" in recognized_text.lower():
                    responses=["I can search in google","Open websites for you","scroll the webpage for you"]                
                    response = random.choice(responses)
                    engine.say(response)
                    engine.runAndWait()                

                elif "open browser" in recognized_text.lower():
                    engine.say("Sure, please tell me the website you want to visit.")
                    engine.runAndWait()

                    # Listen for the website name
                    audio_text = r.listen(source)
                    print("Recording finished. Recognizing...")

                    # Convert speech to text
                    website_name = r.recognize_google(audio_text)
                    print("Website: " + website_name)

                    # Open the specified website using Selenium
                    if "www." not in website_name:
                        website_name = "www." + website_name  # Assume "www." is missing
                    url = f"https://{website_name.lower()}"
                    browser = webdriver.Firefox()
                    browser.get(url)

                    engine.say(f"Opened {website_name} successfully!")
                    engine.runAndWait()

                elif "search" in recognized_text.lower():
                    # Extract the search query from the recognized text
                    search_query = recognized_text.replace("search", "").strip()
                    engine.say(f"Searching for: {search_query}")

                    # Construct the Google search URL
                    google_search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

                    # Open the Google search URL using Selenium
                    browser = webdriver.Firefox()
                    browser.get(google_search_url)

                    engine.say(f"Here are the search results for {search_query}.")
                    engine.runAndWait()

                elif "click link" in recognized_text.lower():
                    if browser:
                        engine.say("Sure, please tell me the text of the link you want to click.")
                        engine.runAndWait()

                        # Listen for the link text
                        audio_text = r.listen(source)
                        print("Recording finished. Recognizing...")

                        # Convert speech to text
                        link_text = r.recognize_google(audio_text)
                        print("Link to click: " + link_text)

                        # Use Selenium to find the link element and click it
                        try:
                            link_element = browser.find_element_by_partial_link_text(link_text)
                            link_element.click()
                            engine.say(f"Clicked the link with text: {link_text}")
                            engine.runAndWait()
                        except Exception as e:
                            engine.say(f"Could not find or click the link with text: {link_text}")
                            engine.runAndWait()
                    else:
                        engine.say("You need to open a browser first before clicking a link.")
                        engine.runAndWait()

                elif "scroll down" in recognized_text.lower():
                    if browser:
                        # Scroll the page down by 100 pixels using JavaScript
                        browser.execute_script("window.scrollBy(0, 100)")
                        engine.say("Scrolled down the page.")
                        engine.runAndWait()
                    else:
                        engine.say("You need to open a browser first before scrolling.")
                        engine.runAndWait()

                # Add more commands and actions as needed here

                else:
                    available_commands = "Available commands: 'open browser', 'search [query]', 'click link [link text]', 'scroll down'"
                    engine.say("I didn't understand your request. " + available_commands)
                    engine.runAndWait()

            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio.")
            except sr.RequestError as e:
                print("Error occurred in connecting to the API. Check your internet connection. Error: ", e)
            except WebDriverException as e:
                print("Error occurred in opening the website or browser. Make sure the input is correct. Error: ", e)

if __name__ == "__main__":
    recognize_and_perform_action()
