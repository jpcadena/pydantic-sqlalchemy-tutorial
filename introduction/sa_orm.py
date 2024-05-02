"""
This module demonstrates the use of SQLAlchemy as a full Object Relational
 Mapper (ORM) for interacting with a SQL database. It defines classes
  representing database tables and includes functionality to add players to
   teams, leveraging the ORM capabilities for database operations.
"""

from typing import Optional, Type

from sqlalchemy import (
    Column,
    Engine,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declarative_base,
    relationship,
    sessionmaker,
)

Base: Type[DeclarativeBase] = declarative_base()
url: str = "mssql+pyodbc://user:password@server.database"
engine: Engine = create_engine(
    url,
    pool_pre_ping=True,
    future=True,
    echo=True,
)
Session = sessionmaker(
    bind=engine,
)
session = Session()


class Team(Base):  # type: ignore
    """
    Represents a team in the database with its name and list of players.
    """

    __tablename__ = "teams"

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(
        String,
    )
    players = relationship(
        "Player",
        backref="team",
    )


class Player(Base):  # type: ignore
    """
    Represents a player in the database with the name of the player and the
    jersey.
    """

    __tablename__ = "players"

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(
        String,
    )
    number = Column(
        Integer,
    )
    team_id = Column(
        Integer,
        ForeignKey("teams.id"),
    )


Base.metadata.create_all(
    engine,
)


def add_player_to_team(
    player_name: str,
    player_number: int,
    team_name: str,
) -> None:
    """
    Adds a player to a team in the database, creating the team if it does not
     exist.
    :param player_name: Name of the player to be added.
    :type player_name: str
    :param player_number: Jersey number of the player.
    :type player_number: int
    :param team_name: Name of the team to which the player will be added.
    :type team_name: str
    :return: None
    :rtype: NoneType
    """
    team: Optional[Type[Team]] | Team = (
        session.query(Team).filter_by(name=team_name).first()
    )
    if not team:
        team = Team(
            name=team_name,
        )
        session.add(team)
        session.commit()
    new_player = Player(
        team.id,
        player_name,
        player_number,
    )
    session.add(new_player)
    session.commit()


add_player_to_team(
    "Juan Carlos",
    9,
    "FC Pythonistas",
)
if fcp_team := (session.query(Team).filter_by(name="FC Pythonistas").first()):
    print(f"Team: {fcp_team.name}")
