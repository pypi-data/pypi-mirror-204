"""The ai utilites for lumeny project"""

from typing import Dict, List
import openai
from lumeny.ConfigLoader import ConfigLoader

# Set your API key from environment variables
config = ConfigLoader().get_config()

openai.api_key = config["openai"]["api"]

# Function to interact with the chatcompletion API


def chat_with_gpt(the_conversation: List[Dict], model: str = "gpt-4", temperature: float = 0.1):
    """

    The function to interact with the chatcompletion API

    :param the_conversation: conversation stored in list of dictionaries
    :param model: gpt3.5-turbo, gpt-4
    :param temperature: from 0 to 1, control the randomness of the response
    """

    response: Dict = openai.ChatCompletion.create(
        model=model, messages=the_conversation, temperature=temperature
    )

    return response["choices"][0]["message"]["content"]


def create_system_msg(prompt: str) -> Dict[str, str]:
    """
    Convert the prompt string to dictionary format

    :param prompt: The prompt for the system
    :return: Promt in dictionary format
    """
    return {"role": "system", "content": prompt}


def create_user_msg(prompt: str) -> Dict[str, str]:
    """

    Convert the user prompt string to dictionary format

    :param prompt: The prompt for the user
    :return: Promt in dictionary format
    """
    return {"role": "user", "content": prompt}


def create_ai_msg(prompt: str) -> Dict[str, str]:
    """

    Convert the ai prompt string to dictionary format

    :param prompt: The prompt for the ai
    :return: Promt in dictionary format
    """
    return {"role": "assistant", "content": prompt}


# Example usage
if __name__ == "__main__":
    pass
