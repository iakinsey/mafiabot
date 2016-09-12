from discord import Client
from discord.errors import Forbidden
from mafiabot import config
from mafiabot.command import get_command
from mafiabot.exc import InvalidCommand, AppException
import discord


client = Client()


def get_contents(message):
    if message.content.startswith(config.COMMAND_PREFIX):
        return message.content.strip(config.COMMAND_PREFIX).strip()

    if message.content.startswith("<@"):
        mentions = message.mentions

        if not mentions:
            return False

        mention_id = message.mentions[0].id
        me = message.server.me.id
        template = "<@{}>".format(me)

        if message.content.startswith(template):
            return message.content.replace(template, "").strip()

    return False


async def process_message(message):
    if message.server is None:
        return

    author = message.author.id
    server = message.server.id
    contents = get_contents(message)

    if contents:
        tokens = contents.split()
        Command = get_command(tokens[0])

        if Command is not None:
            command = Command(client, message, contents, tokens)
            response = await command.perform()

            if response:
                await client.send_message(message.channel, response)


@client.event
async def on_message(message):
    try:
        await process_message(message)
    except AppException as e:
        if e.args and e.public:
            await client.send_message(message.channel, e.args[0])
        else:
            raise
    except NotImplementedError:
        await client.send_message(message.channel, "Not implemented yet.")
    except Forbidden as e:
        if e.code == 50013:
            err = "I don't have permission to do that."
            await client.send_message(message.channel, err)
    except Exception:
        err = "You broke something"
        await client.send_message(message.channel, err)
        raise


def connect_to_discord():
    client.run(config.DISCORD_TOKEN)
