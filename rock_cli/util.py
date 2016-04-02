from click import Group
from collections import OrderedDict

class OrderedGroup(Group):
    """
    A click Group with ordered command list.
    """

    def __init__(self, name=None, commands=[], **attrs):
        Group.__init__(self, name, **attrs)
        self.commands = OrderedDict(commands)

    def list_commands(self, ctx):
        return self.commands.keys()
