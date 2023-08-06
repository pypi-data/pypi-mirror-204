
class Device():
    def __init__(self, target, index):
        self.type = target
        self.index = index
    def __repr__(self):
        if self.index is None:
            return f"device(type='{self.type}')"
        return f"device(type='{self.type}', index={self.index})"
