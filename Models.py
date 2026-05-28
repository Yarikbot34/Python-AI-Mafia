from openai import OpenAI

listModels = {
    "Grok 4.3": "x-ai/grok-4.3",
    "Qwen 3.7":"qwen/qwen3.7-max",
    "Mistral": "mistralai/mistral-medium-3-5"
}

class AIplayer:

    def __init__(self, modelName: str):
        if modelName in listModels:
            self.modelName = modelName
            self.modelUrl = listModels[modelName]
        else: raise ValueError("Invalid model name")

    def getAnswer(self, question: str, client):
        completion = client.chat.completions.create(
            model=self.modelUrl,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            extra_body={"reasoning": {"enabled": True}}
        )
        return completion.choices[0].message.content



