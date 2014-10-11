class ClassNotActive(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s is not open for registration now." % self.value

class TakingOwnClass(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "You can't take your own class (%s)." % self.value