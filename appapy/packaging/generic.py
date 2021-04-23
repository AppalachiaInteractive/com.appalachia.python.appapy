from appapy.packaging.package import Package

class Generic(Package):
    def __init__(self, directory: str, bump: str):
        super(Generic, self).__init__(directory, bump)
