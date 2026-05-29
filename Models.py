from openai import OpenAI
from collections import Counter

listModels = {
    "Grok": "x-ai/grok-4.3",
    "Qwen":"qwen/qwen3.7-max",
    "Mistral": "mistralai/mistral-medium-3-5",
    "Nemotron": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "Laguna":"poolside/laguna-m.1:free",
    "Deepseek":"deepseek/deepseek-v4-flash:free",
    "GPT":"openai/gpt-oss-120b:free",
    "Kimi":"moonshotai/kimi-k2.6:free"

}

gamePromt = lambda name, role, players: f"""Ты - игрок в мафию,твоё имя {name} твоя роль - {role}. Список всех игроков - {players}. 
Игра будет проходить в несколько этапов: 
Представление, в этом этапе ты должен придумать свою роль и представить её другим игрокам;
Ночь: В этом ходу мафия будет определять кого из игроков убить, так же мафия может воздержаться от каких-либо действий;
День: В этом ходу игроки проводят обсуждение и проводят голосование кого из игроков исключить.
Мафия ни в коем случае не должна расказывать свою роль, для остальных она будет обычным игроком.
Твои сообщения не должны превышать 100 слов, говори максимально естественно имитируя обчный диалог, учитывай что ты говоришь один раз за ход.
Далее будет описана история сообщений:"""




class AIplayer:

    mafia = 0
    peace = 0
    client = None
    messeges = [""]
    players = []
    voteList = []
    roles = {}

    def VoteResult(mafia: bool):
        voteList = AIplayer.voteList
        messeges = AIplayer.messeges
        vote = Counter(voteList).most_common(2)
        if len(voteList) > 1 and vote[0][1] == vote[1][1]:
            if  mafia: text = "Прошедшей ночью никто не был убит"
            else:  text = "Жители не смогли прийти к единому мнению, на голосовании никто не был исключен"
        else:
            AIplayer.players.remove(vote[0][0])
            if  mafia: text = f"{vote[0][0]} был убит мафией"
            else:  text = f"{vote[0][0]} был исключен"

            if AIplayer.roles[vote[0][0]] == "mafia":
                AIplayer.mafia -= 1
            else: AIplayer.peace -= 1

        messeges.append(text)
        AIplayer.voteList = []
        return text

    ### Установка параметров ####

    def __init__(self, modelName: str, name: str):
        if modelName in listModels and not(name in AIplayer.players) :
            self.name = name
            self.modelName = modelName
            self.modelUrl = listModels[modelName]
            AIplayer.players.append(name)
        else: raise ValueError("Invalid model name")

    def setRole(self, role):
        self.role = role
        if role == "mafia":
            AIplayer.mafia += 1
        else: AIplayer.peace += 1
        AIplayer.roles[self.name] = role

    #### Ходы ####

    def getAnswer(self, question: str):
        if self.name in AIplayer.players:
            messageHist = [gamePromt(self.name, self.role, AIplayer.players)] + AIplayer.messeges
            messageHist_text = "\n".join(msg for msg in messageHist)
            completion = AIplayer.client.chat.completions.create(
                model=self.modelUrl,
                messages=[
                    {"role": "system", "content": messageHist_text},
                    {"role": "user", "content": question}
                ],
                extra_body={"reasoning": {"enabled": True}}
            )
            return completion.choices[0].message.content
        else: return "Данный игрок был исключен из игры"

    def Introduce(self):
        return self.getAnswer("Твой ход, тебе нужно представить себя подобающим образом перед другими игроками")



    def MafiaStep(self):
        if self.name in AIplayer.players and self.role == "mafia":
            answ = self.getAnswer("Настала ночь. Твой ход. Нужно выбрать того, кто станет жертвой мафии в эту ночь.По возможности распиши свои рассуждения. В конце сообщения напиши \"Исключить:ИмяАппонента\" После этого ничего не писать, даже точку.")
            who = answ.split("Исключить:")[1]
            if who in AIplayer.players:
                AIplayer.voteList.append(who)
            return answ
        else:
            return self.name + " спит"

    def Disput(self):
        if self.name in AIplayer.players:
            answ = self.getAnswer(
                "Настал день. В этом ходе вам предстоит разобраться с ситуацией, и решить, кто из вас является мафией и он будет исключен из игры. В конце сообщения напиши \"Исключить:ИмяАппонента\" После этого ничего не писать, даже точку.")
            AIplayer.messeges.append(answ)
            who = answ.split("Исключить:")[1]
            if who in AIplayer.players:
                AIplayer.voteList.append(who)
            return answ
        else: return "Персонаж был убит"
