SELECT id, status FROM game
WHERE game.server_id = ?
AND game.channel_id = ?
