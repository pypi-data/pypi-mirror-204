from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.11'
DESCRIPTION = "A library for geometric calculations"
LONG_DESCRIPTION = """
    Geomat is a comprehensive Python library tailored to transportation engineering and surveying applications. 
    It offers a wide array of geometric calculations, including horizontal and vertical curves, angles, triangles, polygons, 
    leveling, and geodesy. With a user-friendly interface and support for both metric and imperial units, Geomat enables users 
    to efficiently compute various curve parameters, calculate points of intersection, curvature, and tangency, and perform 
    angle conversions and calculations. Additional functionality includes area and perimeter calculations for triangles and polygons, 
    elevation and height difference calculations in leveling, as well as distance and bearing computations in geodesy. 
    Geomat streamlines geometric calculations for professionals and students alike, enhancing productivity and accuracy in engineering and surveying tasks.
    """

# Setting up
setup(
    name="geomat",
    version=VERSION,
    author="Charles Gameti",
    author_email="gameti@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["typing", "math", "pandas", "numpy", "matplotlib"],
    keywords=['python', 'geomatic', 'levelling', 'curves', 'geodesy', 'polygon', 'triangle', 'horizontal', 'vertical'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)