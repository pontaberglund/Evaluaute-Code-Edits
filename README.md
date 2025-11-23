# Evaluate-Code-Edits

## The Task

The task was to generate code edits in three different ways using ten different models living behind the same API. The responses were parsed according to the edit format and evalauted agains some tests.

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
