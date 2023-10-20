from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Float
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
import datetime
from data.config import host, user, password, db_name
import pg8000

Base = declarative_base()

engine = create_engine(f'postgresql+pg8000://{user}:{password}@{host}/{db_name}', echo=False)

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
conn = engine.connect()


class CasesPrice(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    time_check = Column(DateTime, default=datetime.datetime.utcnow)
    Clutch_Case = Column(Float)
    Danger_Zone_Case = Column(Float)
    CS20_Case = Column(Float)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    telegram_id = Column(BigInteger, index=True)
    access = Column(String, default="User")
    steam_id = Column(BigInteger, index=True, default=None)
    created = Column(DateTime, default=datetime.datetime.utcnow)


Base.metadata.create_all(engine)


def add_close(user, session):
    session.add(user)
    session.commit()
    session.close()
    print("Successful adding")


def add_user(telegram_id, nickname):
    session = Session()
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    print(user)
    if user is not None:
        print("User is already in database")
    else:
        user = Users(nickname=nickname, telegram_id=telegram_id)
        add_close(user, session)


def add_admin(telegram_id, nickname):
    session = Session()
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    if user is not None:
        print("User is already in database")
    else:
        user = Users(nickname=nickname, telegram_id=telegram_id, access="Admin")
        add_close(user, session)


def change_access(telegram_id, access):
    session = Session()
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    if user is not None:
        user.access = access
        session.commit()
        session.close()


def check_access(telegram_id):
    user = session.query(Users).filter(Users.access == "Admin").where(Users.telegram_id == telegram_id).first()
    if user is not None:
        return "Admin"
    else:
        user = session.query(Users).filter(Users.access == "User").where(Users.telegram_id == telegram_id).first()
        if user is not None:
            return "User"
        else:
            user = session.query(Users).filter(Users.access == "Owner").where(Users.telegram_id == telegram_id).first()
            if user is not None:
                return "Owner"
            else:
                user = session.query(Users).filter(Users.access == "Vip").where(
                    Users.telegram_id == telegram_id).first()
                if user is not None:
                    return "Vip"
                else:
                    return None


def change_steam_id(telegram_id, steam_id):
    session = Session()
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    user.steam_id = steam_id
    session.commit()
    session.close()


def get_steamid(telegram_id):
    session = Session()
    user = session.query(Users).where(Users.telegram_id == telegram_id).first()
    if user.steam_id is None:
        session.close()
        return None
    else:
        user_message = f"{user.steam_id}"
        session.close()
        return user_message


def add_close_case(cases, session):
    session.add(cases)
    session.commit()
    session.close()
