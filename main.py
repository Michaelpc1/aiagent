import os
import argparse
import json
import sys
from call_function import available_functions, call_function
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

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        try:
            result = generate_content(client, messages, args.verbose)

            if result:
                print("Final response: ")
                print(result)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")


    print("Error: Maximum iterations reached")
    sys.exit(1)





def generate_content(client: OpenAI, messages: list, verbose: bool) -> None | str:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("response.usage is None")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)
    if not message.tool_calls:
        print("Response:")
        print(message.content)
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue

        result_message = call_function(tool_call, verbose)
        messages.append(result_message)
        if result_message["content"] == "":
            raise Exception("content is empty")

        if verbose:
            print(f"-> {result_message['content']}")


if __name__ == "__main__":
    main()
