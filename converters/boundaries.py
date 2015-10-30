class BBox:
    """
    A pickleable Bounding Box object

    :param west: float, indicating a position in mercator
    :param south: float, indicating a position in mercator
    :param east: float, indicating a position in mercator
    :param north: float, indicating a position in mercator
    :returns nothing
    """
    def __init__(self, west, south, east, north):
        self.west, self.south, self.east, self.north = west, south, east, north


__all__ = [
    'BBox',
]
