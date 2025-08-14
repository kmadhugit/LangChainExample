## LangChainExample

This project demonstrates two ways to build a tool-using agent:

- OpenAI Chat Completions with function calling (`main.py`)
- LangChain Tools Agent using the same Python functions (`main_langchain.py`)

### Prerequisites

- Python 3.10 (project tested with conda env `py310`)
- An OpenAI API key

### Setup

```bash
conda activate py310
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
```

### Run the LangChain agent

```bash
python main_langchain.py
```

What you’ll see:

- Step-by-step agent logs (colored) showing tool calls and observations
- Callback logs for every LLM call, including full prompts and token usage when available
- A final natural-language answer

Example (varies):

```text
The weather in Paris is sunny and 30°C, and the UV index is 8. You should wear sunscreen.
```

### How it works (LangChain)

- The agent prompt instructs the model to check weather and UV, then decide on sunscreen.
- The model chooses which tools to call.
- LangChain runs the requested tools and passes the results back to the model.
- The loop repeats until the model returns a final answer.

Files involved:

- `main_langchain.py`: builds tools, prompt, and an OpenAI Tools Agent; runs `AgentExecutor`
- `tools/weather.py`: `get_weather(city: str) -> str`
- `tools/uv_index.py`: `get_uv_index(city: str) -> int`
- `tools/sunscreen.py`: `should_wear_sunscreen(weather: str, uv_index: int) -> str`

### Logging OpenAI calls

`main_langchain.py` includes an `LLMCallLogger` callback that prints on every model call:

- [LLM start]: model and full prompt text
- [LLM end]: token usage (when available)

You can toggle verbosity of the agent run itself by changing `verbose=True` in the `AgentExecutor`.

Disable colored output (optional):

```bash
NO_COLOR=1 python main_langchain.py
```

### Optional: Tracing with LangSmith

Enable rich traces and a web UI with LangSmith (optional):

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_langsmith_key
python main_langchain.py
```

### Alternative: OpenAI function-calling loop

You can also run the original, minimal loop using the OpenAI Chat Completions API directly:

```bash
python main.py
```

That script manually executes tool calls using the schema in `tools/tools_factory.py` and prints request/response tables for debugging.


