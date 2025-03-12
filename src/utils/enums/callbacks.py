from enum import Enum


class CallbackPrefix(str, Enum):
    quit = "q_chat_"
    cansel = "cansel"
    kick = "k_user_"