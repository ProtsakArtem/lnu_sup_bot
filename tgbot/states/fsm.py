import re

from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, CommandObject

from aiogram.fsm.state import State, StatesGroup

MainState = State("MainState")
ChatState = State("ChatState")
Support_busy_state = State("Support_busy_state")
Free_support = State("Free_support")
Choose_support = State("Choose_support")
Scarga = State("Scarga")
Chat = State("Chat")