from openai import OpenAI

from Models import AIplayer




def startGame():
    print("Первая встеча")
    for model in models:
        answ = model.Introduce()
        answ = f"{model.name} : {answ}"
        print(answ)
        AIplayer.messeges.append(answ)

def NightGame():
    print("\nНаступает ночь\n")
    for model in models:
        answ = model.MafiaStep()
        answ = f"{model.name} : {answ}"
        print(answ)
    print(AIplayer.VoteResult(True))

def DayGame():
    print("\nНаступает день\n")
    for model in models:
        answ = model.Disput()
        answ = f"{model.name} : {answ}"
        print(answ)
    print(AIplayer.VoteResult(False))


key = input("Enter your API key from openrouter: ")
client = OpenAI(api_key=key, base_url = "https://openrouter.ai/api/v1")
AIplayer.client = client

models = []

while len(models) < 5:
    modelName = input("Enter your model name: ")
    name = input("Enter your model nickname: ")
    try:
        newPlayer = AIplayer(modelName, name)
    except ValueError: pass
    else: models.append(newPlayer)

models[0].setRole("Мирный")
models[1].setRole("mafia")
models[2].setRole("Мирный")
models[3].setRole("Мирный")
models[4].setRole("Мирный")

startGame()
while AIplayer.peace > AIplayer.mafia > 0:
    NightGame()
    DayGame()

print("Игра завершена")


