import argparse
import os
from langchain import OpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType

def get_llm_response(prompt):
    llm = OpenAI(temperature=0)
    tools = []
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    response = agent.run(prompt)
    return response

def main():
    parser = argparse.ArgumentParser(description="Get a response from an LLM for a given prompt.")
    parser.add_argument("prompt", help="text prompt for the LLM")

    args = parser.parse_args()

    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is not set in the environment.")
        return

    response = get_llm_response(args.prompt)
    print(response)

if __name__ == "__main__":
    main()
