import re

from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

MainState = State("MainState")
ChatState = State("ChatState")
Support_busy_state = State("Support_busy_state")
Free_support = State("Free_support")
Choose_support = State("Choose_support")
Scarga = State("Scarga")
Chat = State("Chat")


def create_new_user_session(user_id):
    return(f"{user_id}_session")

async def count_users_in_state(state_name, fsm_context: FSMContext):
    async with fsm_context.proxy() as data:
        users_in_state = [user_id for user_id, user_data in data.items() if user_data.get('state') == state_name]
        print(f"Count users in state '{state_name}': {len(users_in_state)}")
        return len(users_in_state)