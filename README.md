# Evaluate-Code-Edits

## The Task

Your task is to generate code edits in three different ways using ten different models living behind the same API.
You can freely define or reuse the edition tasks from existing benchmarks, and the API to be used. But it has to be code edition (and not code generation).
Then, I ask you to write a short document comparing both the edit formats and the model performance, and giving your reflection on the task. If you're not successful, you can reflect about the main difficulties you faced.

## Setup

1.  **Environment Variables**: Create a `.env` file in the root directory to store your API key. The scripts use OpenRouter.

    ```bash
    OPENROUTER_API_KEY=your_openrouter_api_key_here
    ```

2.  **Dependencies**: Install the required Python packages.
    ```bash
    pip install openai python-dotenv tqdm
    ```

## Usage

### 1. Generate Model Responses

Run the main prompting script to query the 10 defined models. This script iterates through three test scenarios (Logic, Crash, Class Extension) and three edit formats (Whole, Diff, UDiff), saving all outputs to `model_responses.json`.

```bash
python prompt_models.py
```

### 2. Run the analytics notebook

Open `analytics.ipynb` and run the code blocks to extract results from the responses in `model_responses.json` and view them as graphs.
