from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        return TgBot(token=token)


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    """

    tg_bot: TgBot



def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)
    print(env.str("ADMINS"))
    return Config(
        tg_bot=TgBot.from_env(env),
    )
def get_admins():
    env = Env()
    env.read_env()
    admins = env.list('ADMINS', [])
    print(f"ADMINS: {admins}")
    return admins

# Функція для запису списку адміністраторів у .env файл
def set_admins(admin_list):
    with open('.env', 'r') as file:
        lines = file.readlines()

    with open('.env', 'w') as file:
        for line in lines:
            if line.startswith('ADMINS='):
                file.write(f"ADMINS={','.join(admin_list)}\n")
            else:
                file.write(line)

# Функція для додавання адміністратора
def add_admin(admin_id):
    admins = get_admins()
    if admin_id not in admins:
        admins.append(admin_id)
        set_admins(admins)

# Функція для видалення адміністратора
def remove_admin(admin_id):
    admins = get_admins()
    if admin_id in admins:
        admins.remove(admin_id)
        set_admins(admins)