"""Users service db models."""
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ARRAY, Float, DateTime
from sqlalchemy.ext.hybrid import hybrid_method

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    categories_ids = Column(ARRAY(Integer))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    join_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"User {self.id}: [{(self.name, self.email)}"

    @hybrid_method
    def in_range(self, latitude, longitude, radius):
        """Check if user in range (radius in meters)."""
        from math import sin, cos, sqrt, atan2, radians
        R = 6373.0  # approximate radius of earth in km
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(latitude)
        lon2 = radians(longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c <= radius

    @in_range.expression
    def in_range(cls, latitude, longitude, radius):
        """Check if user in range (radius in meters)."""
        R = 6373.0  # approximate radius of earth in km
        from sqlalchemy import func
        lat1 = func.radians(cls.latitude)
        lon1 = func.radians(cls.longitude)
        lat2 = func.radians(latitude)
        lon2 = func.radians(longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = func.pow(func.sin(dlat / 2), 2) + func.cos(lat1) * func.cos(lat2) \
            * func.pow(func.sin(dlon / 2), 2)
        c = R * 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))
        print(c)
        return c
