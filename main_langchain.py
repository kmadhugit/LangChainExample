import os
from typing import List

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI

from tools.weather import get_weather
from tools.uv_index import get_uv_index
from tools.sunscreen import should_wear_sunscreen


def build_tools() -> List[StructuredTool]:
    weather_tool = StructuredTool.from_function(
        func=get_weather,
        name="get_weather",
        description="Get the weather for a city",
    )

    uv_tool = StructuredTool.from_function(
        func=get_uv_index,
        name="get_uv_index",
        description="Get the UV index for the city",
    )

    sunscreen_tool = StructuredTool.from_function(
        func=should_wear_sunscreen,
        name="should_wear_sunscreen",
        description="Advise if sunscreen is needed based on weather and UV index",
    )

    return [weather_tool, uv_tool, sunscreen_tool]


def build_prompt() -> ChatPromptTemplate:
    system = (
        "You are a helpful assistant.\n"
        "- First, always check the weather by calling get_weather and get_uv_index parallely.\n"
        "- Based on the weather and UV index, decide if sunscreen is needed.\n"
        "- Do not call should_wear_sunscreen for rainy weather."
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )


class LLMCallLogger(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        model = serialized.get("kwargs", {}).get("model", "")
        print(f"[LLM start] model={model}, prompts={len(prompts)}")
        for i, p in enumerate(prompts, 1):
            print(f"--- Prompt {i} ---\n{p}\n---------------")

    def on_llm_end(self, response, **kwargs):
        usage = None
        try:
            # response is an LLMResult; token usage is usually under llm_output["token_usage"]
            usage = getattr(response, "llm_output", None)
            if isinstance(usage, dict):
                usage = usage.get("token_usage", usage)
        except Exception:
            pass
        print(f"[LLM end] usage={usage}")


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set in the environment")

    tools = build_tools()

    # Use the same model as the existing example
    llm = ChatOpenAI(model="gpt-4o-mini", callbacks=[LLMCallLogger()])

    prompt = build_prompt()

    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    user_input = "What's the weather in Paris and should I wear sunscreen?"
    result = executor.invoke({"input": user_input})

    # AgentExecutor returns a dict; the final output is under the "output" key
    print(result.get("output", ""))


if __name__ == "__main__":
    main()


