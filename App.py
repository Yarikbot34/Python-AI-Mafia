from openai import OpenAI

from openai.types.conversations import message

from Models import AIplayer




def startGame():
    print("Первая встеча")
    for model in models:
        answ = model.Introduce()
        answ = f"{model.modelName} : {answ}"
        print(answ)
        AIplayer.messeges.append(answ)

def NightGame():
    print("\nНаступает ночь\n")
    for model in models:
        answ = model.MafiaStep()
        print(answ)
    AIplayer.VoteResult(True)

def DayGame():
    print("\nНаступает день\n")
    for model in models:
        answ = model.Disput()
        print(answ)
    AIplayer.VoteResult(False)


key = input("Enter your API key from openrouter: ")

client = OpenAI(api_key=key, base_url = "https://openrouter.ai/api/v1")

AIplayer.client = client

models = []

while len(models) < 4:
    modelName = input("Enter your model name: ")
    try:
        newPlayer = AIplayer(modelName)
    except ValueError: pass
    else: models.append(newPlayer)

models[0].setRole("Мирный")
models[1].setRole("mafia")
models[2].setRole("Мирный")
models[3].setRole("Мирный")

startGame()
NightGame()
DayGame()
NightGame()
DayGame()


