from openai import OpenAI

class LLMClient:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )

    def chat(self, prompt):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是严谨中文科研助手"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content