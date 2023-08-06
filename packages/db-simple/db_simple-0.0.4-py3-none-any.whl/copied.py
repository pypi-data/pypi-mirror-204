import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_components import DiscordComponents

class DiscordBot:
    def __init__(self, bot_id):
        """
        Initializes the DiscordBot object.

        :param bot_id: the ID of the bot
        """
        self.bot_id = bot_id
        self.bot_prefix = None
        self.bot_events = {}
        self.bot_commands = {}
        self.bot_slash_commands = {}
        self.bot_embeds = {}

    async def copy_bot_prefix(self, bot_prefix):
        """
        Copies the bot prefix.

        :param bot_prefix: the prefix to copy
        """
        self.bot_prefix = bot_prefix

    async def copy_bot_events(self, bot_events):
        """
        Copies the bot events.

        :param bot_events: the events to copy
        """
        for event_name, event_func in bot_events.items():
            self.bot_events[event_name] = event_func

    async def copy_bot_commands(self, bot_commands):
        """
        Copies the bot commands.

        :param bot_commands: the commands to copy
        """
        for command_name, command_func in bot_commands.items():
            self.bot_commands[command_name] = command_func

    async def copy_bot_slash_commands(self, bot_slash_commands):
        """
        Copies the bot slash commands.

        :param bot_slash_commands: the slash commands to copy
        """
        for command_name, command_func in bot_slash_commands.items():
            self.bot_slash_commands[command_name] = command_func

    async def copy_bot_embeds(self, bot_embeds):
        """
        Copies the bot embeds.

        :param bot_embeds: the embeds to copy
        """
        for embed_name, embed in bot_embeds.items():
            self.bot_embeds[embed_name] = embed

    def start_bot(self, token):
        """
        Starts the bot.

        :param token: the bot token to use
        """
        if not self.bot_prefix:
            print("Please provide a bot prefix using copy_bot_prefix method.")
            return

        bot = commands.Bot(command_prefix=self.bot_prefix, intents=discord.Intents.all())
        slash = SlashCommand(bot, sync_commands=True)
        DiscordComponents(bot)

        @bot.event
        async def on_ready():
            print(f'{bot.user.name} has connected to Discord!')

        for event_name, event_func in self.bot_events.items():
            @bot.event
            async def event_handler(*args, **kwargs):
                await event_func(*args, **kwargs)

        for command_name, command_func in self.bot_commands.items():
            @bot.command(name=command_name)
            async def command_handler(ctx, *args, **kwargs):
                await command_func(ctx, *args, **kwargs)

        for command_name, command_func in self.bot_slash_commands.items():
            @slash.slash(name=command_name)
            async def slash_command_handler(ctx: SlashContext, *args, **kwargs):
                await command_func(ctx, *args, **kwargs)

        for embed_name, embed in self.bot_embeds.items():
            bot.add_cog(embed)

        bot.run(token)

