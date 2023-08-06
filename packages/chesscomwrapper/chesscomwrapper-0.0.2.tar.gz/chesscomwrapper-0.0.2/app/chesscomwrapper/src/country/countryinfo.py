class CountryInfo(object):
    def __init__(self, data) -> None:
        self.name = data.get('name',None)
        self.code = data.get('code',None)
        self.id = data.get('@id',None)