from mafiabot import config
from mafiabot.command import Command
from mafiabot.db import insert, select
from mafiabot.exc import InvalidCommand
from time import time


class Mafia(Command):
    prefix = "mafia"
    description = "Initiates a game of mafia for players to join."
    examples = []

    async def default(self):
        created = int(time())
        status = "init"

        game = await select('get_game', self.server_id, self.channel_id,
                            first=True)

        if game:
            raise InvalidCommand("Game currently in progress.")

        await insert('init_game', self.server_id, self.channel_id,
                     self.author_id, created, status)

        # Stupid Sqlite doesn't allow RETURNING.
        game_id ,= await select('get_game_id', self.server_id, self.channel_id,
                            self.author_id, created, status, first=True)

        await insert('join_game', game_id, self.author_id)

        return "**Starting mafia game. Type !join to enter.**"


class Start(Command):
    prefix = "start"
    description = "Starts a game of mafia after players have joined."
    examples = []

    async def default(self):
        players = await select('get_game_players', self.server_id,
                               self.channel_id)

        if not players:
            raise InvalidCommand("No games currently running!")
        elif len(players) < config.MINIMUM_PLAYERS:
            err = "Not enough players have joined, you need {} players."
            raise InvalidCommand(err.format(config.MINIMUM_PLAYERS))

        game_id, status = await select('get_game_status', self.server_id,
                                       self.channel_id, first=True)

        if status != 'init':
            raise InvalidCommand('Game cannot be started')

        await insert('set_game_status', 'queued', game_id)

        # Logic goes here to queue the game up for playing.

        return "Starting game."


class Join(Command):
    prefix = "join"
    description = "Join the mafia game."
    examples = []

    async def default(self):
        result = await select('get_game_and_player', self.channel_id,
                              self.server_id, self.author_id, first=True)

        if result is None:
            raise InvalidCommand("No game is currently in progress.")

        game_id, player_id, status = result

        if player_id is not None:
            raise InvalidCommand("You already joined the game.")

        if status != "init":
            raise InvalidCommand("Can't join game.")

        await insert('join_game', game_id, self.author_id)

        return "<@{}> joined the game.".format(self.author_id)


class Leave(Command):
    prefix = "leave"
    description = "Leave the mafia game."
    examples = []

    async def default(self):
        pass


class Abort(Command):
    prefix = "abort"
    description = "Aborts the mafia game."
    examples = []

    async def default(self):
        pass


class Vote(Command):
    prefix = "vote"
    description = "Vote on who to lynch."
    examples = []

    async def default(self):
        pass
