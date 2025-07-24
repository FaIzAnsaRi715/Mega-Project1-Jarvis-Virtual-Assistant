from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)
completion = client.chat.completions.create(
    model = "deepseek/deepseek-chat-v3-0324:free",
    messages=[
        {"role": "system", "content": "You are a virtual assistent named jarvis skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": "What is coding"}
    ]
)

print(completion.choices[0].message.content)


