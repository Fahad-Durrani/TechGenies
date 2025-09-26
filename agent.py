from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START,END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from typing import List, Dict, Optional
from typing import TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.messages import RemoveMessage
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime, timezone
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#local imports
from api_import import keys_settings
from tools.weather_tool import get_weather
from tools.news_tool import search_news
from utils.uLogger import logger



class Chatbot:
    def __init__(self):
        # Load values from .env
        self.max_history = keys_settings.max_history
        self.keep_n = keys_settings.keep_n

        logger.info(f"Chatbot initialized with max_history={self.max_history}, Keep messages after reset={self.keep_n}")

        # LLM + tools setup
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=keys_settings.openai_api_key
        )
        logger.info(f"LLM initialized with: {self.llm.model_name}")

        self.tools = [get_weather, search_news]
        self.llm_with_tools = self.llm.bind_tools(self.tools, parallel_tool_calls=False)
    

        # Load system prompt
        with open("prompts/chatbot_prompt.txt", "r", encoding="utf-8") as f:
            self.conversational_sys_prompt = SystemMessage(content=f.read())
        logger.info("Chabot Agent prompt loaded successfully")

    def ai_chat(self, state: MessagesState) -> MessagesState:
        response = self.llm_with_tools.invoke([self.conversational_sys_prompt] + state["messages"])
        messages = state["messages"]

        if len(messages) >= self.max_history:
            logger.info(f"[AI_CHAT] Memory reset due to length of message =({len(messages)})")
            delete_messages = [RemoveMessage(id=m.id) for m in messages[:-self.keep_n]]
            trimmed_messages = delete_messages + [response]
            logger.info(f"[AI_CHAT] Resetting memory, keeping last {self.keep_n} messages")
            return {"messages": trimmed_messages}

        logger.info(f"[AI_CHAT] Appending response, total messages now: {len(messages) + 1}")
        return {"messages": messages + [response]}

    def create_graph(self):
        logger.info("[GRAPH] Creating conversation graph...")
        memory = MemorySaver()
        graph = StateGraph(MessagesState)

        graph.set_entry_point("ai_chat")
        graph.add_node("ai_chat", self.ai_chat)
        graph.add_node("tools", ToolNode(self.tools))
        graph.add_conditional_edges("ai_chat", tools_condition)
        graph.add_edge("tools", "ai_chat")

        logger.info("[GRAPH] Graph compiled with memory saver")
        return graph.compile(checkpointer=memory)
