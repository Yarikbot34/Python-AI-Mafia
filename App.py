from openai import OpenAI

key = input("Enter your API key from openrouter: ")

client = OpenAI(api_key=key, base_url = "https://openrouter.ai")