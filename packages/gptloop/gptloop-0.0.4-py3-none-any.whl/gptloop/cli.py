import openai
import json
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

def gpt3_query(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def solve_task(task_description):
    # Divide and Conquer
    divided_task = f"Divide the following problem into smaller subproblems: {task_description}"
    subproblems = gpt3_query(divided_task)
    
    solutions = []
    for subproblem in subproblems.split("\n"):
        if subproblem.strip() != "":
            # Solve subproblem iteratively
            iterative_prompt = f"Solve the following problem iteratively: {subproblem}"
            solution = gpt3_query(iterative_prompt)
            solutions.append(solution)
    
    # Combine the solutions
    combine_solutions = f"Combine the following solutions into a single solution: {json.dumps(solutions)}"
    final_solution = gpt3_query(combine_solutions)
    return final_solution

def main():
    parser = argparse.ArgumentParser(description='Solve tasks using OpenAI GPT-3 with divide and conquer and iterative techniques.')
    parser.add_argument('task_description', type=str, help='Task description')
    args = parser.parse_args()

    solution = solve_task(args.task_description)
    print("Solution:", solution)

if __name__ == "__main__":
    main()
