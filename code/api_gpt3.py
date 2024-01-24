import openai
import requests

openai.api_key = ""  # replace with your api_key
ApiKey = ""  # replace with your api_key


def get_response(model, prompt):
    """Get response from different OpenAI models."""
    if model == "gpt-3.5-turbo":
        h = {"Content-Type": "application/json", "Authorization": f"Bearer {ApiKey}"}
        d = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0,
        }
        u = "https://api.openai.com/v1/chat/completions"
        r = requests.post(url=u, headers=h, json=d).json()
        return r["choices"][0]["message"]["content"].strip()

    elif model == "text-davinci-003":
        response = openai.Completion.create(
            model="text-davinci-003", prompt=prompt, temperature=0.6
        )
        return response["choices"][0]["text"].strip()

    elif model == "text-davinci-002":
        response = openai.Completion.create(
            model="text-davinci-002", prompt=prompt, temperature=0.6
        )
        return response["choices"][0]["text"].strip()

    elif model == "gpt-3.5-turbo-instruct":
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200,
        )
        return response["choices"][0]["text"].strip()
