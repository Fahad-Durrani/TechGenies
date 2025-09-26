
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from utils.uLogger import logger
def log_messages(messages):

    """
    Logs conversation messages in a clean and structured format.
    Supports Human, AI, and Tool messages with tool call details.
    """
    for msg in messages:
        # Human Message
        if isinstance(msg, HumanMessage):
            logger.info("================================== Human Message ==================================")
            logger.info(msg.content)

        # AI Message
        elif isinstance(msg, AIMessage):
            logger.info("================================== Ai Message ==================================")
            logger.info(msg.content)

            # Handle tool calls (if any)
            tool_calls = msg.additional_kwargs.get("tool_calls")
            if tool_calls:
                logger.info("Tool Calls:")
                for call in tool_calls:
                    func_name = call["function"]["name"]
                    args = call["function"]["arguments"]
                    call_id = call.get("id", "N/A")

                    logger.info("-" * 80)
                    logger.info(f"Tool Function Name : {func_name}")
                    logger.info(f"Tool Arguments     : {args}")
                    logger.info(f"Tool Call ID       : {call_id}")
                    logger.info("-" * 80)

        # Tool Message
        elif isinstance(msg, ToolMessage):
            logger.info(f"================================== Tool Message (Name: {msg.name}) ==================================")
            logger.info(msg.content)

        # Fallback for unknown message types
        else:
            logger.info(f"================================== Other Message ==================================")
            logger.info(str(msg))