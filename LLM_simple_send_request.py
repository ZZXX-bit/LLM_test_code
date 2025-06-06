import requests

url = "http://localhost:18011/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}
data = {
    "model": "meta-llama/llama-4-scout-17b-16e-instruct",
    "messages": [
        {"role": "system", "content": "你是一个乐于助人的 AI 助手。"},
        {"role": "user", "content": "介绍一下Llama 4 Scout模型的特点"}
    ],
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 512,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
print(response.json()['choices'][0]['message']['content'])
