DROP TABLE IF EXISTS checkins;

CREATE TABLE checkins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  team_number VARCHAR(255) NOT NULL,
  client_address VARCHAR(255) NOT NULL
);