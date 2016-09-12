SELECT game.status, game.created, game_player.user_id
FROM game
JOIN game_player ON game_player.game_id = game.id
WHERE game.server_id = ?
AND game.channel_id = ?
