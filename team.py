from enum import Enum
"""The Enum classifies the teams"""
class Team(Enum):
    #Red team
    RED = 1
    R = 1

    #Black team
    BLACK = -1
    BLUE = -1
    B = -1

    #None team
    NONE = 0
    N = 0

    def __str__(self):
        return self.name.lower()
    """Reverse function"""
    @staticmethod
    def get_reverse_team(team):
        if team is Team.RED:
            return Team.BLACK
        elif team is Team.BLACK:
            return Team.RED
        else:
            raise ValueError("Invalid input team")