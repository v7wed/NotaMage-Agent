import os

def get_system_prompt(user_name: str) -> str:
    """
    Returns a string that is the system prompt for The Mage agent.
    """
    prompt_file_path = os.getenv('SYSTEM_PROMPT_FILE')
    
    if prompt_file_path and os.path.exists(prompt_file_path):
        with open(prompt_file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    else:
        raise 
