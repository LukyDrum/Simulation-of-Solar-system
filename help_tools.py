from math import sqrt


class Vector2D:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.vector = [self.x, self.y]
        self.magnitude = sqrt(self.x**2 + self.y**2)
        if self.magnitude != 0:
            self.normalized = UnitVector2D(self.x / self.magnitude, self.y / self.magnitude)

    def normalize(self) -> None:
        """
        Normalizes the Vector
        *IN PLACE*
        """
        if self.magnitude != 0:
            self.x = self.x / self.magnitude
            self.y = self.y / self.magnitude

    def update(self) -> None:
        self.vector = [self.x, self.y]
        self.magnitude = sqrt(self.x**2 + self.y**2)
        if self.magnitude != 0:
            self.normalized = UnitVector2D(self.x / self.magnitude, self.y / self.magnitude)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x * other, self.y * other)
        else:
            print("Operation failed - Invalid operation")
    
    def __truediv__(self, other):
        if other == 0:
            print("Operation failed - Cannot divide by 0")
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x / other, self.y / other)
        else:
            print("Operation failed - Invalid operation")

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        else:
            print("Operation failed - Invalid operation")

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        else:
            print("Operation failed - Invalid operation")


class UnitVector2D(Vector2D):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.vector = [self.x, self.y]
        self.magnitude = 1


def distance_of_two_points(pos1:list[float|int, float|int], pos2:list[float|int, float|int]) -> float:
    return sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)


def vector_between_two_points(pos1:list[float|int, float|int], pos2:list[float|int, float|int]) -> Vector2D:
    return Vector2D(pos2[0] - pos1[0], pos2[1] - pos1[1])


def meters_to_pixels(meters: float|int) -> float:
    """
    1 pixel = 10**9 meters
    """
    pixels = meters / 10**9
    return pixels

def pixels_to_meters(pixels: float|int) -> float:
    meters = pixels * 10**9
    return meters