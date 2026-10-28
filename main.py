import os
import argparse
import json
from call_function import available_functions, call_function
from prompts import system_prompt
from dotenv import load_dotenv
from openai import OpenAI




def main():
    print("Hello from bootdev-ai-agent!")

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key Not Found")

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="BootDev Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt for the BootDev Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    
    messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": args.user_prompt},
            ]

    for _ in range(20):
        response = client.chat.completions.create(
        model="openrouter/free",
        messages = messages,
        tools = available_functions,
        )

        if response.usage is None:
                raise RuntimeError ("The API Call Failed")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                results_message = call_function(tool_call, args.verbose)
                if results_message["content"] == "" or results_message["content"] is None:
                    raise Exception ("empty result returned")
                if args.verbose:
                    print(f"-> {results_message['content']}")
                messages.append(results_message)
                    
        else:
            print(message.content)
            break

    else:
        print("Iteration limit reached")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
