CREATE TABLE game (
    id INTEGER PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    server_id BIGINT NOT NULL,
    admin_id BIGINT NOT NULL,
    status VARCHAR NOT NULL,
    created INTEGER NOT NULL
);


CREATE INDEX game_id_idx ON game(id);
CREATE INDEX game_server_id_idx ON game(server_id);


CREATE TABLE game_player (
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY(game_id) REFERENCES game(id) ON DELETE CASCADE,
    UNIQUE (game_id, user_id)
);


CREATE INDEX game_player_game_id_idx ON game_player(game_id);
CREATE INDEX game_player_user_id_idx ON game_player(user_id);
