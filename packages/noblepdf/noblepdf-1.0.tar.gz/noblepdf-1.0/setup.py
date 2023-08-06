import setuptools
from pathlib import Path


setuptools.setup(name="noblepdf", version=1.0,
                 long_description=Path(r"C:\Users\3991731036\Desktop\practice\noblepdf\README.md").read_text(), 
                 packages=setuptools.find_packages(exclude=["tests", "data"]))