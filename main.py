import os
from dotenv import load_dotenv
from openai import OpenAI



def main():
    load_dotenv()
    if load_dotenv():
        print("found .env file")

    key = os.environ.get("OPENROUTER_API_KEY")

    if key is None:
        raise RuntimeError("key is None")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ],
    )

    if response.usage is None:
        raise RuntimeError("response.usage is None")

    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
