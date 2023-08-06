import pkg_resources


path = pkg_resources.resource_filename("vault", "VERSION")
__version__ = open(path).read()
