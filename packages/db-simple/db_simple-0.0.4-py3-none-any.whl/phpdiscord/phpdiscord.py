from typing import List, Optional, Dict
import commands, description, function
from commands import prefix
import requests
from bs4 import BeatifoulSoup

class EmbedButton:
    def __init__(self, url: str, text: str, style: str):
        self.url = url
        self.text = text
        self.style = style

class EmbedSelectMenuOption:
    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

class EmbedSelectMenu:
    def __init__(self, custom_id: str, options: List[EmbedSelectMenuOption], placeholder: str):
        self.custom_id = custom_id
self.options = options
        self.placeholder = placeholder

class Embed:
    def __init__(self, title: Optional[str] = None, description: Optional[str] = None, color: Optional[int] = None):
        self.title = title
        self.description = description
        self.color = color
        self._footer = None
        self._button = None
        self._select_menu = None

    def set_footer(self, text: str, icon_url: Optional[str] = None):
        self._footer = {"text": text, "icon_url": icon_url}

    def set_button(self, url: str, text: str, style: str):
        self._button = EmbedButton(url, text, style)

    def set_select_menu(self, custom_id: str, options: List[EmbedSelectMenuOption], placeholder: str):
        self._select_menu = EmbedSelectMenu(custom_id, options, placeholder)

    def get_embed_dict(self) -> Dict:
        embed_dict = {"fields": []}
        if self.title:
            embed_dict["title"] = self.title
        if self.description:
            embed_dict["description"] = self.description
        if self.color:
            embed_dict["color"] = self.color
        if self._footer:
            embed_dict["footer"] = self._footer
        if self._button:
            embed_dict["type"] = "button"
            embed_dict["url"] = self._button.url
            embed_dict["text"] = self._button.text
            embed_dict["style"] = self._button.style
        if self._select_menu:
            menu_dict = {"type": "select-menu", "custom_id": self._select_menu.custom_id,
                         "options": [{"label": o.label, "value": o.value} for o in self._select_menu.options],
                         "placeholder": {"text": self._select_menu.placeholder}}
            embed_dict["components"] = [{"type": "action-row", "components": [menu_dict]}]
        return embed_dict

def command_handler(command_name: str, handler_function: Callable[..., str], description_text: str = None): """ Декоратор для обработки команд. :param command_name: Имя команды. :param handler_function: Функция, которая будет вызвана при выполнении команды. :param description_text: Описание команды. """ @command(name=command_name) @description(description_text) def command_wrapper(): return handler_function() def run(commands: List[Callable[..., str]], default_prefix: str = '!'): """ Запустить бота с указанными командами. :param commands: Список функций-обработчиков команд. :param default_prefix: Префикс по умолчанию для команд. """ prefix.set_default_prefix(default_prefix) for cmd in commands: command_name = cmd.__name__.replace('_', '-') command_wrapper = command_handler(command_name, cmd) command_wrapper() function.run() __all__ = ['command_handler', 'run']

class Discord: def __init__(self, token=None, intents=None, system_help=True): self.token = token self.intents = intents if intents is not None else discord.Intents.default() if self.intents.members is False: self.intents.members = True if self.intents.messages is False: self.intents.messages = True self.system_help = system_help self.bot = commands.Bot(command_prefix='!') @self.bot.event async def on_ready(): print(f'{self.bot.user.name} is connected to Discord!') @self.bot.command() async def help(ctx): await ctx.send(self.get_help_message()) def get_help_message(self): if self.system_help: # Список команд бота return 'Список команд бота:\n!command1 - описание команды 1\n!command2 - описание команды 2\n' else: return 

async def start(self, bot_token): await self.client.login(bot_token) await self.bot.login(bot_token) await self.client.connect() async def stop(self): await self.client.close() await self.bot.close() async def get_guilds(self): await self.client.wait_until_ready() return self.client.guilds async def get_emojis(self, guild_id): await self.client.wait_until_ready() guild = self.client.get_guild(guild_id) return guild.emojis async def get_user(self, user_id): await self.client.wait_until_ready() user = await self.client.fetch_user(user_id) return user async def get_roles(self, guild_id): await self.client.wait_until_ready() guild = self.client.get_guild(guild_id) return guild.roles async def get_voice_channels(self, guild_id): await self.client.wait_until_ready() guild = self.client.get_guild(guild_id) return guild.voice_channels async def send_private_message(self, user_id, message): await self.client.wait_until_ready() user = await self.client.fetch_user(user_id) await user.send(message)
def translate(text, language="English", to_language="Russian"): """ Translates text from one language to another using Reverso Context translation service. Args: text (str): The text to translate. language (str): The language of the original text (default is 'English'). to_language (str): The language to translate the text into (default is 'Russian'). Returns: A string containing the translated text. """ headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'} url = f"https://context.reverso.net/translation/{language.lower()}-{to_language.lower()}/{text}" try: response = requests.get(url, headers=headers) soup = BeautifulSoup(response.content, 'html.parser') translations = soup.find('div', {'id': 'translations-content'}).text.strip() examples = soup.find_all('div', {'class': 'example'}) examples_text = [example.text.strip() for example in examples] result = f"{translations}\n\nExamples:\n{examples_text[0]} - {examples_text[1]}" except Exception as e: result = f"Sorry, I could not translate the text.\n{str(e)}" return result

class SelfBot(discord.Client): def __init__(self, prefix, token): super().__init__() self.prefix = prefix self.token = token self.user_message = None self.user_embed = None async def on_ready(self): print(f"Logged in as {self.user}") async def on_message(self, message): if message.author == self.user: return if message.content.startswith(self.prefix): command = message.content[len(self.prefix):].split()[0].lower() if command == "ping": await message.channel.send("Pong!") elif command == "echo": await message.channel.send(message.content[len(self.prefix)+len(command)+1:]) self.user_message = message async def send_embed(self, embed): if self.user_message is None: raise Exception("No message found to send embed.") self.user_embed = embed await self.user_message.channel.send(embed=embed)