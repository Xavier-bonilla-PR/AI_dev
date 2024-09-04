# Automated Experimentation System

This repository contains a Python script for an automated experimentation system. The system uses AI-generated code to iteratively run experiments based on a given idea, allowing for efficient exploration and testing of hypotheses.

## Features

- Automated code generation using the Claude 3.5 Sonnet AI model
- Iterative experiment execution and result analysis
- Configurable maximum number of runs and iterations
- Automatic error handling and timeout management

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- Git
- An Anthropic API key (for Claude 3.5 Sonnet)

## Installation

Install Aider:

   ```
   python -m pip install aider-chat
   ```

## Configuration

1. Set up your Anthropic API key:
   ```
   Mac/Linux: export ANTHROPIC_API_KEY=your_api_key_here
   Windows: SET ANTHROPIC_API_KEY=your_api_key_here
   
   ```
2. (Optional) Adjust the `MAX_RUNS`, `MAX_ITERATIONS`, and `MAX_STDERR_OUTPUT` constants in the script if needed.

## Usage

To run the automated experimentation system:

1. Execute the main script:
   ```
   python iterative_code_generator.py
   ```

2. When prompted, enter:
   - The file name for your experiment (without '.py')
   - The title of your experiment
   - The idea or hypothesis you want to test

The system will then generate code, run experiments, and iterate based on the results.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

[MIT License](LICENSE)

## Acknowledgements

- This project uses the Aider library for code generation and management.
- Used prompts and code from AI scientist from Sakana AI: https://github.com/SakanaAI/AI-Scientist/tree/main
- The Claude 3.5 Sonnet model by Anthropic is used for AI-powered code generation.
