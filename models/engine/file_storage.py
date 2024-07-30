#!/usr/bin/python3
"""Module defining the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Represents an abstracted storage engine for saving and loading objects.

    Attributes:
        __file_path (str): Path to the JSON file for storage.
        __objects (dict): Dictionary to store all objects by <class name>.id.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary of all stored objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object to the storage dictionary with key <obj_class_name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize the objects to the JSON file specified by __file_path."""
        obj_dict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserialize the JSON file to __objects if the file exists."""
        try:
            with open(FileStorage.__file_path, "r") as file:
                obj_dict = json.load(file)
                for obj_data in obj_dict.values():
                    class_name = obj_data.pop("__class__")
                    self.new(eval(class_name)(**obj_data))
        except FileNotFoundError:
            pass

