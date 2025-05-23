from sqlalchemy import Column, Integer, String, ForeignKey, func, Date, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship

from database.base import Base


class EventORM(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    sport_key = Column(String, index=True, nullable=False)
    commence_time_utc = Column(TIMESTAMP(timezone=True), index=True)
    home_team = Column(String, index=True)
    away_team = Column(String, index=True)
    derived_game_name = Column(String)
    created_at_utc = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at_utc = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with PlayerProp
    player_props = relationship("PlayerPropORM", back_populates="event")


class PlayerPropORM(Base):
    __tablename__ = 'player_props'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey('events.id'),
                     index=True, nullable=False)
    game_start_time_utc = Column(TIMESTAMP(timezone=True), index=True)
    player_name = Column(String, index=True)
    prop_type = Column(String, index=True)  # e.g. Points, Rebounds, Assists
    line = Column(Numeric(5, 2))
    over_odds = Column(Numeric(5, 2))
    under_odds = Column(Numeric(5, 2))
    bookmaker = Column(String, index=True)
    odds_collection_time_utc = Column(TIMESTAMP(timezone=True))
    job_start_time_utc = Column(TIMESTAMP(timezone=True))

    # Relationship with Event
    event = relationship("EventORM", back_populates="player_props")


class PlayerORM(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, unique=True)  # Keep this as external ID reference
    name = Column(String, index=True)
    team = Column(String, index=True)

    # Relationships
    games = relationship("GameStatsORM", back_populates="player")


class GameStatsORM(Base):
    __tablename__ = 'game_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False)
    game_id = Column(String, index=True)
    game_date = Column(Date, index=True)  # EDT date
    matchup = Column(String, index=True)
    season = Column(String, index=True)
    # Regular Season, Playoffs, Preseason
    season_type = Column(String, index=True)

    # Basic stats
    points = Column(Integer, nullable=False, default=0)
    assists = Column(Integer, nullable=False, default=0)
    rebounds = Column(Integer, nullable=False, default=0)
    three_pointers_made = Column(Integer, nullable=False, default=0)

    # Additional stats
    minutes = Column(Integer)

    player = relationship("PlayerORM", back_populates="games")
