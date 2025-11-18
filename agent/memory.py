from langchain.memory import ConversationBufferMemory

def get_memory():
    """
    Simple conversation memory for your research agent.
    Stored in RAM (can be upgraded later to Redis).
    """
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
