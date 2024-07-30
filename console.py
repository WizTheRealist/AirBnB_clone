#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse_arguments(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            args = [i.strip(",") for i in lexer]
            args.append(brackets.group())
            return args
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        args = [i.strip(",") for i in lexer]
        args.append(curly_braces.group())
        return args


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel", "User", "State", "City", "Place", "Amenity", "Review"
    }

    def emptyline(self):
        """Ignore empty lines."""
        pass

    def default(self, arg):
        """Default behavior for invalid commands."""
        commands = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match:
            cmd_args = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", cmd_args[1])
            if match:
                command = [cmd_args[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in commands:
                    call = f"{cmd_args[0]} {command[1]}"
                    return commands[command[0]](call)
        print(f"*** Unknown syntax: {arg}")
        return False

    def do_quit(self, arg):
        """Exit the command interpreter."""
        return True

    def do_EOF(self, arg):
        """Handle EOF to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Create a new instance of a class."""
        args = parse_arguments(arg)
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            instance = eval(args[0])()
            print(instance.id)
            storage.save()

    def do_show(self, arg):
        """Show the string representation of an instance."""
        args = parse_arguments(arg)
        objdict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in objdict:
            print("** no instance found **")
        else:
            print(objdict[f"{args[0]}.{args[1]}"])

    def do_destroy(self, arg):
        """Delete an instance based on class name and id."""
        args = parse_arguments(arg)
        objdict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in objdict:
            print("** no instance found **")
        else:
            del objdict[f"{args[0]}.{args[1]}"]
            storage.save()

    def do_all(self, arg):
        """Display all instances of a class or all instances."""
        args = parse_arguments(arg)
        if args and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objlist = [str(obj) for obj in storage.all().values()
                       if not args or obj.__class__.__name__ == args[0]]
            print(objlist)

    def do_count(self, arg):
        """Count the number of instances of a class."""
        args = parse_arguments(arg)
        count = sum(1 for obj in storage.all().values()
                    if args[0] == obj.__class__.__name__)
        print(count)

    def do_update(self, arg):
        """Update an instance based on class name and id."""
        args = parse_arguments(arg)
        objdict = storage.all()

        if not args:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if f"{args[0]}.{args[1]}" not in objdict:
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                eval(args[2])
            except NameError:
                print("** value missing **")
                return False

        obj = objdict[f"{args[0]}.{args[1]}"]
        if len(args) == 4:
            if args[2] in obj.__class__.__dict__:
                valtype = type(obj.__class__.__dict__[args[2]])
                setattr(obj, args[2], valtype(args[3]))
            else:
                setattr(obj, args[2], args[3])
        elif isinstance(eval(args[2]), dict):
            for k, v in eval(args[2]).items():
                if k in obj.__class__.__dict__ and isinstance(obj.__class__.__dict__[k], (str, int, float)):
                    valtype = type(obj.__class__.__dict__[k])
                    setattr(obj, k, valtype(v))
                else:
                    setattr(obj, k, v)
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()

