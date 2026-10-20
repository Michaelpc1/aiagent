import os
import argparse
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

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if response.usage is None:
        raise RuntimeError("response.usage is None")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
