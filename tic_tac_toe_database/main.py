import os
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

# Load .env if available
load_dotenv()

Base = declarative_base()

# PUBLIC_INTERFACE
class User(Base):
    """User for authentication and game tracking"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    games = relationship("Game", back_populates="player_x", foreign_keys="[Game.player_x_id]")
    games_as_o = relationship("Game", back_populates="player_o", foreign_keys="[Game.player_o_id]")
    moves = relationship("Move", back_populates="user")
    results = relationship("GameResult", back_populates="user")

# PUBLIC_INTERFACE
class Game(Base):
    """A Tic Tac Toe game instance"""
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    player_x_id = Column(Integer, ForeignKey("users.id"))
    player_o_id = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(16), default="in_progress")  # in_progress, finished

    player_x = relationship("User", back_populates="games", foreign_keys=[player_x_id])
    player_o = relationship("User", back_populates="games_as_o", foreign_keys=[player_o_id])
    moves = relationship("Move", back_populates="game")
    result = relationship("GameResult", uselist=False, back_populates="game")

# PUBLIC_INTERFACE
class Move(Base):
    """A move in a Tic Tac Toe game"""
    __tablename__ = "moves"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    move_number = Column(Integer, nullable=False)
    row = Column(Integer, nullable=False)
    col = Column(Integer, nullable=False)
    symbol = Column(Enum("X", "O", name="symbol_enum"), nullable=False)
    played_at = Column(DateTime(timezone=True), server_default=func.now())

    game = relationship("Game", back_populates="moves")
    user = relationship("User", back_populates="moves")

# PUBLIC_INTERFACE
class GameResult(Base):
    """Final result of a game and user outcome"""
    __tablename__ = "game_results"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    result = Column(Enum("win", "loss", "draw", name="result_enum"), nullable=False)
    score_delta = Column(Integer, default=0)

    game = relationship("Game", back_populates="result")
    user = relationship("User", back_populates="results")

# PUBLIC_INTERFACE
def get_engine():
    """Get the SQLAlchemy database engine using DATABASE_URL or fallback."""
    db_url = os.getenv("DATABASE_URL", "sqlite:///tic_tac_toe.db")
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    engine = create_engine(db_url, echo=True, future=True, connect_args=connect_args)
    return engine

# PUBLIC_INTERFACE
def init_db():
    """Initialize the database and create all tables."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Database initialized and tables created.")

if __name__ == "__main__":
    init_db()
