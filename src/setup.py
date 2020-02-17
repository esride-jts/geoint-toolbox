from setuptools import setup

setup(name="geoint",
      version="0.1",
      description="GEOINT module for the GEOINT toolbox.",
      url="https://github.com/esride-jts/geoint-toolbox",
      author="Esri Deutschland GmbH",
      author_email="j.tschada@esri.de",
      license="LGPL Version 3.0",
      packages=["geoint"],
      include_package_data=True,
      zip_safe=False)