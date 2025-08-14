"""LangChain agent with explicit tool schemas to avoid arg mismatch errors."""

import json
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from tool_factory import tools
# utils is optional for this script; avoid hard dependency


class MyLogger(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print("LLM call started!")
        for i, p in enumerate(prompts):
            print(f"Prompt {i}:\n{p}")

    def on_llm_end(self, response, **kwargs):
        print("LLM call finished!")
        # Print the full message objects from the generations (ChatGeneration.message)
        try:
            generations = getattr(response, "generations", []) or []
            for i, gen_list in enumerate(generations):
                for j, gen in enumerate(gen_list or []):
                    msg = getattr(gen, "message", None)
                    if msg is not None:
                        print(f"[message {i}.{j}] {msg}")
                    else:
                        text = getattr(gen, "text", "")
                        print(f"[text {i}.{j}] {text}")
        except Exception as e:
            print(f"[debug] error printing LLM message objects: {e}")


if __name__ == '__main__':

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        callback_manager=CallbackManager([MyLogger()]),
        verbose=True,
    )

    # --- Initialize agent ---
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )

    # --- Run the agent ---
    user_input = "What's the weather in Paris? Should I wear sunscreen?"
    response = agent.run(user_input)
    print("\nFinal response:", response)