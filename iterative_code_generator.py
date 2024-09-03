import subprocess
import os
import json
from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
import anthropic

client = anthropic.Anthropic()

MAX_ITERATIONS = 5
MAX_RUNS = 5
MAX_STDERR_OUTPUT = 1500

coder_prompt = """Your goal is to implement the following idea: {title}.
The proposed experiment is as follows: {idea}.
You are given a total of up to {max_runs} runs to complete the necessary experiments. You do not need to use all {max_runs}.

First, plan the list of experiments you would like to run. For example, if you are sweeping over a specific hyperparameter, plan each value you would like to test for each run.

After you complete each change, we will run the command `python {file_name}.py' and evaluate the results.
YOUR PROPOSED CHANGE MUST USE THIS COMMAND FORMAT, DO NOT ADD ADDITIONAL COMMAND LINE ARGS.
You can then implement the next thing on your list."""

def generate_and_run_code(prompt: str, file_name) -> None:
    io = InputOutput(
            yes=True, chat_history_file=f"{file_name}_aider.txt"
        )
    model = Model("claude-3-5-sonnet-20240620")
    coder = Coder.create(
        main_model=model,
        io=io,
        stream=False,
        use_git=False,
        edit_format="diff",
    )

    run = 1
    while run < MAX_RUNS + 1:
        print(f"Run {run}")
        
        # Generate code
        generated_code = coder.run(prompt)
        
        # Run the generated code
        result = run_experiment(run, file_name)
        print("Code was run.")
        if result.returncode == 0:
            next_prompt = f"""Run {run} completed. Here are the results:
{result.stdout}

Decide if you need to re-plan your experiments given the result (you often will not need to).

Make file {file_name}_notes.txt and include *all* relevant information for the writeup on Run {run}, including an experiment description and the run number. Be as verbose as necessary.

Then, implement the next thing on your list.
We will then run the command `python {file_name}.py'.
YOUR PROPOSED CHANGE MUST USE THIS COMMAND FORMAT, DO NOT ADD ADDITIONAL COMMAND LINE ARGS.
If you are finished with experiments, respond with 'ALL_COMPLETED'."""
        else:
            stderr_output = result.stderr
            if len(stderr_output) > MAX_STDERR_OUTPUT:
                stderr_output = "..." + stderr_output[-MAX_STDERR_OUTPUT:]
            next_prompt = f"Run failed with the following error {stderr_output}"
        
        prompt = next_prompt
        if "ALL_COMPLETED" in generated_code:
            break
        run += 1
    
    if run == MAX_RUNS + 1:
        print("Maximum runs reached. Experiments completed.")

def run_experiment(run_num, file_name, timeout=100):
    command = [
        "python",
        f"{file_name}.py"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            print(f"Run {run_num} failed with return code {result.returncode}")
            print(f"Run failed with the following error {result.stderr}")
        return result
    except subprocess.TimeoutExpired:
        print(f"Run {run_num} timed out after {timeout} seconds")
        return subprocess.CompletedProcess(args=command, returncode=1, stdout="", stderr=f"Timed out after {timeout} seconds")

if __name__ == "__main__":
    file_name = input("what is file name? (without '.py') ")
    title = input("What is title? ")
    idea = input('What is idea: ')
    initial_prompt = coder_prompt.format(
        title=title,
        idea=idea,
        max_runs=MAX_RUNS,
        file_name = file_name
    )
    generate_and_run_code(initial_prompt, file_name)
