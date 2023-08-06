from ml.ml40.features.properties.values.value import Value


class VegetationIndex(Value):
    def __init__(self, namespace="fml40", name="", identifier="", parent=None):
        super().__init__(
            namespace=namespace, name=name, identifier=identifier, parent=parent
        )
        self.__latestTime = None
        self.__latestURL = None
        self.__latestMin = None
        self.__latestMax = None
        self.__latestMean = None
        self.__latestStd = None
        self.__latestMedian = None
        self.__latestP25 = None
        self.__latestP75 = None
        self.__json_out = {}

    @property
    def latestTime(self):
        return self.__latestTime

    @latestTime.setter
    def latestTime(self, value):
        self.__latestTime = value

    @property
    def latestURL(self):
        return self.__latestURL

    @latestURL.setter
    def latestURL(self, value):
        self.__latestURL = value

    @property
    def latestMin(self):
        return self.__latestMin

    @latestMin.setter
    def latestMin(self, value):
        self.__latestMin = value
        
    @property
    def latestMax(self):
        return self.__latestMax

    @latestMax.setter
    def latestMax(self, value):
        self.__latestMax = value
        
    @property
    def latestMean(self):
        return self.__latestMean

    @latestMean.setter
    def latestMean(self, value):
        self.__latestMean = value
        
    @property
    def latestStd(self):
        return self.__latestStd

    @latestStd.setter
    def latestStd(self, value):
        self.__latestStd = value
        
    @property
    def latestMedian(self):
        return self.__latestMedian

    @latestMedian.setter
    def latestMedian(self, value):
        self.__latestMedian = value
        
    @property
    def latestP25(self):
        return self.__latestP25

    @latestP25.setter
    def latestP25(self, value):
        self.__latestP25 = value
        
    @property
    def latestP75(self):
        return self.__latestP75

    @latestP75.setter
    def latestP75(self, value):
        self.__latestP75 = value

    def to_json(self):
        self.__json_out = super().to_json()
        if self.latestTime is not None:
            self.__json_out["latestTime"] = self.latestTime
        if self.latestURL is not None:
            self.__json_out["latestURL"] = self.latestURL        
        if self.latestMin is not None:
            self.__json_out["latestMin"] = self.latestMin        
        if self.latestMax is not None:
            self.__json_out["latestMax"] = self.latestMax        
        if self.latestMean is not None:
            self.__json_out["latestMean"] = self.latestMean        
        if self.latestStd is not None:
            self.__json_out["latestStd"] = self.latestStd        
        if self.latestMedian is not None:
            self.__json_out["latestMedian"] = self.latestMedian        
        if self.latestP25 is not None:
            self.__json_out["latestP25"] = self.latestP25        
        if self.latestP75 is not None:
            self.__json_out["latestP75"] = self.latestP75
        return self.__json_out