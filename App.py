from openai import OpenAI
from Models import AIplayer

key = input("Enter your API key from openrouter: ")

client = OpenAI(api_key=key, base_url = "https://openrouter.ai/api/v1")

models = []

while len(models) < 2:
    modelName = input("Enter your model name: ")
    try:
        newPlayer = AIplayer(modelName)
    except ValueError: pass
    else: models.append(newPlayer)

