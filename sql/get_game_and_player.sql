SELECT game.id, game_player.game_id, game.status FROM game
LEFT OUTER JOIN game_player ON game_player.game_id = game.id
WHERE game.channel_id = ?
AND game.server_id = ?
AND (game_player.user_id = ? OR game_player.user_id IS NULL)
