import setuptools

setuptools.setup(
    name = "colored_logging",
    version = "0.1",
    author = "Wagner Cotta",
    description = "Colored logging package from \"is-wire\" to be used in any python script.\n Although I'm the author of this package, the code was not developed by me.\n It was copied and modified from is-wire python package.",
    package_dir = {"":"src"},
    url="https://github.com/wagnercotta/colored-logging",
    packages = setuptools.find_packages(where="src"),
    install_requires = ["colorlog"],
    license = "GNU"
)