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
        """
        Print x, y, and z dimensions.
        """
        print(self.GetX(), self.GetY(), self.GetZ())

    def GetX(self) -> float:
        """
        Get x dimension.

        Returns:
            x (float): x dimension.
        """
        return self.x

    def GetY(self) -> float:
        """
        Get y dimension.

        Returns:
            y (float): y dimension.
        """
        return self.y

    def GetZ(self) -> float:
        """
        Get z dimension.

        Returns:
            z (float): z dimension.
        """
        return self.z
