#!/usr/bin/python3
"""Module defining the BaseModel class."""
from uuid import uuid4
from datetime import datetime
import models

class BaseModel:
    """Represents the base model for the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        Args:
            *args: Variable length argument list (not used).
            **kwargs: Arbitrary keyword arguments for attributes.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    setattr(self, key, datetime.strptime(value, time_format))
                else:
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at with the current datetime and save changes."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance."""
        instance_dict = self.__dict__.copy()
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        instance_dict["__class__"] = self.__class__.__name__
        return instance_dict

    def __str__(self):
        """Return the string representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

