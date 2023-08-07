import os
import openai


openai.api_key = os.environ["OPENAI_API_KEY"]


def get_answer(content, role="user", model="gpt-3.5-turbo"):
    messages = [
            {'role':role, 'content':content}
    ]
    return openai.ChatCompletion.create(
        model=model,
        messages=messages
    ).choices[0]["message"]["content"].strip()


if __name__ == "__main__":
    pass
