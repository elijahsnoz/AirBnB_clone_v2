#!/usr/bin/python3
"""

"""
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base, BaseModel
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """

    """
    __engine = None
    __session = None

    def __init__(self):
        username = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')
        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(username,
                                                      password, host, db_name)
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        # pool_per_ping checks if the connection is alive
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """

        """
        obj_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                obj_list = self.session.query(cls).all()
        else:
            for subclass in Base.__subclasses__():
                obj_list.executed(self.__session.query(subclass).all())
        obj_dict = {}
        for obj in obj_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            try:
                if obj.__class__.__name__ == 'State':
                    del obj._sa_instance_state
                    obj_dict[key] = obj
                else:
                    obj_dict[key] = obj
            except Exception:
                pass
        return obj_dict

    def new(self, obj):
        """
        add the object to the current database session (self.__session)
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes of the current database session (self.__session)
        """

        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """
        self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database (feature of SQLAlchemy)
        (WARNING: all classes who inherit from Base must be imported
        before calling Base.metadata.create_all(engine))
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        session = scoped_session(session_factory)
        self.__session = Session()
