class Dimensions:
    """
    A class that specifies dimensions of an instance.

    Attributes:
            _dx (float): Length in x direction.
            _dy (float): Length in y direction.
            _dz (float): Length in z direction.
    """

    _dx: float
    _dy: float
    _dz: float

    def __init__(self, dx, dy, dz):
        self.set_x(dx)
        self.set_y(dy)
        self.set_z(dz)

    def __repr__(self) -> str:
        """
        Provides a string representation of the Dimension instance.

        Returns:
            str: String representation of the Dimension instance.
        """
        return f"(dx={self._dx}, dy={self._dy}, dz={self._dz})"

    def set_x(self, dx: float) -> None:
        """
        Sets length in x direction.

        Args:
            dx (float): Length in x direction.
        """
        self._dx: float = dx

    def get_x(self) -> float:
        """
        Gets length in x direction.

        Returns:
            float: Length in x direction.
        """
        return float(self._dx)

    def set_y(self, dy: float) -> None:
        """
        Sets length in z direction.

        Args:
            dy (float): Length in y direction.
        """
        self._dy: float = dy

    def get_y(self) -> float:
        """
        Gets length in z direction.

        Returns:
            float: Length in y direction.
        """
        return float(self._dy)

    def set_z(self, dz: float) -> None:
        """
        Sets length in z direction..

        Args:
            dz (float): Length in z direction.
        """
        self._dz: float = dz

    def get_z(self) -> float:
        """
        Gets length in z direction..

        Returns:
            float: Length in z direction.
        """
        return float(self._dz)


class Position:
    """
    A class that represents a position in Cartesian space.

    Attributes:
        _x (float): x coordinate.
        _y (float): y coordinate.
        _z (float): z coordinate.
    """

    _x: float
    _y: float
    _z: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.set_x(x)
        self.set_y(y)
        self.set_z(z)

    def __add__(self, other: "Position") -> "Position":
        """
        Adds two Position instances as 3D vectors.

        Args:
            other (Position): The other Position instance to add.

        Returns:
            Position: A new Position instance which is the vector sum.
        """
        return Position(
            self._x + other._x, self._y + other._y, self._z + other._z
        )

    def __sub__(self, other: "Position") -> "Position":
        """
        Subtracts one Position instance from another as 3D vectors.

        Args:
            other (Position): The other Position instance to subtract.

        Returns:
            Position: A new Position instance which is the vector difference.
        """
        return Position(
            self._x - other._x, self._y - other._y, self._z - other._z
        )

    def __repr__(self) -> str:
        """
        Provides a string representation of the Position instance.

        Returns:
            str: String representation of the Position instance.
        """
        return f"(x={self._x}, y={self._y}, z={self._z})"

    def set_x(self, x: float) -> None:
        """
        Sets the x coordinate.
        """
        self._x: float = x

    def get_x(self) -> float:
        """
        Gets the x coordinate.
        """
        return float(self._x)

    def set_y(self, y: float) -> None:
        """
        Sets the y coordinate.
        """
        self._y: float = y

    def get_y(self) -> float:
        """
        Gets the y coordinate.
        """
        return float(self._y)

    def set_z(self, z: float) -> None:
        """
        Sets the z coordinate.
        """
        self._z: float = z

    def get_z(self) -> float:
        """
        Gets the z coordinate.
        """
        return float(self._z)
