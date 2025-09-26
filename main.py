from api_import import keys_settings
from utils.uLogger import logger
from agent import Chatbot
from langchain_core.messages import HumanMessage
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from utils.log_helper import log_messages
import datetime

if __name__ == "__main__":
    
    chatbot = Chatbot()
    graph = chatbot.create_graph()
    logger.info("Chatbot initialized and ready!")
    
    state = {"messages": []}
    config = {"configurable": {"thread_id": "1"}}
    logger.info(f"Using config: {config}")

    while True:
        print("================== Please enter you Message for the Chatbot ========================= ")
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            logger.info("User ended the session.")
            print("Goodbye! See you again")
            break

        start_time = datetime.datetime.now()
        logger.info(f"User request started at: {start_time}")
        state["messages"].append(HumanMessage(content=user_input))
        
        try:
            result = graph.invoke(state, config)
            response = result["messages"][-1].content
            end_time = datetime.datetime.now()
            logger.info(f"Agent response completed at: {end_time}")
            logger.info(f"Total response time: {end_time - start_time}")
            log_messages(result["messages"])
            print(f"================================== Chatbot Response==============================")
            print(f"Chatbot Response: {response}")

            # Update state with new messages
            state = result
            logger.info(f"State updated, total messages now: {len(state['messages'])}")

        except Exception as e:
            logger.error(f"Error during chatbot invoke: {e}")
            print(f"Error during chatbot invoke: {e}")