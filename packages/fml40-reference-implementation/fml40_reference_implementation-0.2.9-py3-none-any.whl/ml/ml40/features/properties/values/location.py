from ml.ml40.features.properties.values.value import Value


class Location(Value):
    def __init__(self, namespace="ml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.__latitude = None
        self.__longitude = None
        self.__orientation = None
        self.__x = None
        self.__y = None
        self.__z = None
        self.__json_out = {}

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        self.__latitude = value

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        self.__longitude = value

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, value):
        self.__orientation = value
        
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, value):
        self.__z = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.latitude is not None:
            self.__json_out["latitude"] = self.latitude
        if self.longitude is not None:
            self.__json_out["longitude"] = self.longitude
        if self.orientation is not None:
            self.__json_out["orientation"] = self.orientation
        if self.x is not None:
            self.__json_out["x"] = self.x
        if self.y is not None:
            self.__json_out["y"] = self.y
        if self.z is not None:
            self.__json_out["z"] = self.z
        return self.__json_out
