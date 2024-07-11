class Dimensions:
    """
    A class that specifies dimensions of instances of different classes.

    Attributes:
            x, y, z (float): Dimensions in x, y and z direction.
    """

    def __init__(self, x_in, y_in, z_in):
        self.x: float = x_in
        self.y: float = y_in
        self.z: float = z_in

    def PrintDimensions(self):
        print(self.GetX(), self.GetY(), self.GetZ())

    def GetX(self) -> float:
        return self.x

    def GetY(self) -> float:
        return self.y

    def GetZ(self) -> float:
        return self.z
