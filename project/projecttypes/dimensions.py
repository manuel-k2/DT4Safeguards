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

    def returnX(self) -> float:
        return self.x

    def returnY(self) -> float:
        return self.y

    def returnZ(self) -> float:
        return self.z
