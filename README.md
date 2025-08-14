## LangChainExample

This project demonstrates two ways to build a tool-using agent:

- OpenAI Chat Completions with function calling (`main.py`)
- LangChain Tools Agent (`Agent.py`) using tools defined in `tool_factory.py`

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
python Agent.py
```

What you’ll see:

- Step-by-step agent logs (colored) showing tool calls and observations
- Callback logs for every LLM call, including full prompts, tool-calls, and the final message object
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

- `Agent.py`: builds the LangChain agent, wires callbacks, and runs it
- `tool_factory.py`: defines tools and wraps them with `StructuredTool.from_function`
- `main.py`: minimal OpenAI Chat Completions loop (function-calling) alternative

### Logging OpenAI calls

`Agent.py` includes a `MyLogger` callback that prints on every model call:

- on_llm_start: prints each prompt
- on_llm_end: prints the returned message object via `response.generations[0][0].message`

You can toggle verbosity by setting `verbose=True` when initializing the agent.

Disable colored output (optional):

```bash
NO_COLOR=1 python Agent.py
```

### Optional: Tracing with LangSmith

Enable rich traces and a web UI with LangSmith (optional):

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your_langsmith_key
python Agent.py
```

### Alternative: OpenAI function-calling loop

You can also run the original, minimal loop using the OpenAI Chat Completions API directly:

```bash
python main.py
```

That script manually executes tool calls using the schema and prints request/response tables for debugging.


