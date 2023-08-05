import argparse
import os
import openai

def get_llm_response(prompt, api_key):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

def main():
    parser = argparse.ArgumentParser(description="Get a response from an LLM for a given prompt.")
    parser.add_argument("prompt", help="text prompt for the LLM")

    args = parser.parse_args()

    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is not set in the environment.")
        return

    response = get_llm_response(args.prompt, api_key)
    print(response)

if __name__ == "__main__":
    main()
