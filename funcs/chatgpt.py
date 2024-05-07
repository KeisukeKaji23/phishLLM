from openai import OpenAI
import json


def run_conversation(system, user, model):
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": system,
            },
            {"role": "user", "content": user},
        ],
        temperature=0.0,
        timeout=60,
    )
    res = response.choices[0].message.content
    json_res = json.loads(res)
    return json_res
