"""Memory utility functions for the email assistant."""

from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langgraph.store.base import BaseStore

from email_assistant_hitl.prompts.defaults import MEMORY_UPDATE_INSTRUCTIONS, MEMORY_UPDATE_INSTRUCTIONS_REINFORCEMENT

class UserPreferences(BaseModel):
    """Updated user preferences based on user's feedback."""
    chain_of_thought: str = Field(description="Reasoning about which user preferences need to add / update if required")
    user_preferences: str = Field(description="Updated user preferences")

def get_memory(store: BaseStore, namespace: tuple, default_content: str = None) -> str:
    """Get memory from the store or initialize with default if it doesn't exist.
    
    Args:
        store: LangGraph BaseStore instance to search for existing memory
        namespace: Tuple defining the memory namespace, e.g. ("email_assistant", "triage_preferences")
        default_content: Default content to use if memory doesn't exist
        
    Returns:
        str: The content of the memory profile, either from existing memory or the default
    """
    user_preferences = store.get(namespace, "user_preferences")
    
    if user_preferences:
        return user_preferences.value
    
    if default_content:
        store.put(namespace, "user_preferences", default_content)
        return default_content
    
    return ""

def update_memory(store: BaseStore, namespace: tuple, messages: list):
    """Update memory profile in the store based on user feedback.
    
    Args:
        store: LangGraph BaseStore instance to update memory
        namespace: Tuple defining the memory namespace, e.g. ("email_assistant", "triage_preferences")
        messages: List of messages to update the memory with
    """

    user_preferences = store.get(namespace, "user_preferences")
    current_profile = user_preferences.value if user_preferences else ""

    llm = init_chat_model("openai:gpt-4.1", temperature=0.0).with_structured_output(UserPreferences)
    
    system_instruction = MEMORY_UPDATE_INSTRUCTIONS.format(
        current_profile=current_profile, 
        namespace=namespace
    )
    
    result = llm.invoke(
        [
            {"role": "system", "content": system_instruction},
        ] + messages
    )
    print(f"\nUpdated memory for {namespace}:\n{result.chain_of_thought}\n{result.user_preferences}\n")
    
    store.put(namespace, "user_preferences", result.user_preferences)
