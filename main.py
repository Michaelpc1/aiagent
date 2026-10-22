import os
import argparse
import json
from call_function import available_functions
from prompts import system_prompt
from dotenv import load_dotenv
from openai import OpenAI



def main():
    load_dotenv()

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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("response.usage is None")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")

    print(message.content)


if __name__ == "__main__":
    main()
