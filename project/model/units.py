class Dimensions:
    """
    A class that specifies dimensions of an instance.

    Attributes:
            dx (float): Length in x direction.
            dy (float): Length in y direction.
            dz (float): Length in z direction.
    """

    def __init__(self, dx, dy, dz):
        self.SetX(dx)
        self.SetY(dy)
        self.SetZ(dz)

    def PrintDimensions(self) -> None:
        """
        Prints lengths in x, y, and z direction.
        """
        print(self.GetX(), self.GetY(), self.GetZ())

    def SetX(self, dx: float) -> None:
        """
        Sets length in x direction.

        Args:
            dx (float): Length in x direction.
        """
        self.dx: float = dx

    def GetX(self) -> float:
        """
        Gets length in x direction.

        Returns:
            float: Length in x direction.
        """
        return self.dx

    def SetY(self, dy: float) -> None:
        """
        Sets length in z direction.

        Args:
            dy (float): Length in y direction.
        """
        self.dy: float = dy

    def GetY(self) -> float:
        """
        Gets length in z direction.

        Returns:
            float: Length in y direction.
        """
        return self.dy

    def SetZ(self, dz: float) -> None:
        """
        Sets length in z direction..

        Args:
            dz (float): Length in z direction.
        """
        self.dz: float = dz

    def GetZ(self) -> float:
        """
        Gets length in z direction..

        Returns:
            float: Length in z direction.
        """
        return self.dz


class Position:
    """
    A class that represents a position in Cartesian space.

    Attributes:
        x (float): x coordinate.
        y (float): y coordinate.
        z (float): z coordinate.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def SetX(self, x: float) -> None:
        """
        Sets the x coordinate.
        """
        self.x = x

    def GetX(self) -> float:
        """
        Gets the x coordinate.
        """
        return self.x

    def SetY(self, y: float) -> None:
        """
        Sets the y coordinate.
        """
        self.y = y

    def GetY(self) -> float:
        """
        Gets the y coordinate.
        """
        return self.y

    def SetZ(self, z: float) -> None:
        """
        Sets the z coordinate.
        """
        self.z = z

    def GetZ(self) -> float:
        """
        Gets the z coordinate.
        """
        return self.z

    def PrintPosition(self) -> None:
        """
        Prints position of instance in Cartesian space.
        """
        print(f"Position(x={self._x}, y={self._y}, z={self._z})")
