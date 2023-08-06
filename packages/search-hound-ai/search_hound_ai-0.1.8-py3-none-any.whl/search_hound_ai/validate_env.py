import logging
import os

import pkg_resources

def ValidateEnv():
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    print("OPENAI_API_KEY", OPENAI_API_KEY)
    if OPENAI_API_KEY == None or OPENAI_API_KEY == '':
        open_ai_key_value = input("Enter your OPENAI_API_KEY: ")

        if open_ai_key_value == None or open_ai_key_value == '':
            logging.error("OPENAI_API_KEY is required.")
            exit(1)

        if open_ai_key_value != None and open_ai_key_value != '':
            filename = pkg_resources.resource_filename(__name__, ".env")
            text_file = open(filename, "w")
            text_file.write('OPENAI_API_KEY=' + open_ai_key_value)
            text_file.close()
            logging.info("OPENAI_API_KEY ENV saved")
            exit(1)

