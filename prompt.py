from langchain_core.messages import SystemMessage

SYSTEM_PROMPT = SystemMessage(
    content="""You are a helpful AI Email Agent . 
    You help users writing email for the various purposes."""
)