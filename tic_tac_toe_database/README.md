# Tic Tac Toe Database Container

This container provides the database and schema for the Tic Tac Toe application. It defines tables for users, games, moves, and tracks win/loss history.

- Database: SQLite (default; easy migration to PostgreSQL by editing the connection string if desired)
- ORM: SQLAlchemy

## Running

1. (Optional) Set environment variable `DATABASE_URL` to override the SQLite file path.
2. Run main.py to initialize the database:

```bash
python main.py
```

## Tables

- `users`: User authentication and profile.
- `games`: Tic Tac Toe games (two-player or against the AI).
- `moves`: Moves made in each game, by player and sequence.
- `game_results`: Results and scores.
