class List:

    def __init__(self, name, initial_values=None):
        self._name = name
        if initial_values is None:
            self.data = []
        else:
            self.data = list(initial_values)

    def append(self, value):
        self.data.append(value)

    def clear(self):
        self.data = []

    def average(self):
        if not self.data:  # Avoid division by zero
            return 0
        return sum(self.data) / len(self.data)

    def getName(self):
        return self._name
    

    

