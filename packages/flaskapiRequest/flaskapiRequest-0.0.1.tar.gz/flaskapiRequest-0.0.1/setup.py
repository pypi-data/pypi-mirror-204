from setuptools import setup, find_packages

NAME = "flaskapiRequest"
VERSION = '0.0.1'
DESCRIPTION = 'FlaskApi Python package'
LONG_DESCRIPTION = 'Python package for my flask API'
AUTHOR = "Ajang Elvis Ngwesse"
AUTHOR_EMAIL = "<ngwesseaws@gmail.com>"
REQUIREMENTS = [
    "certifi==2022.12.7",
    "charset-normalizer==3.1.0",
    "future==0.18.3",
    "idna==3.4",
    "names==0.3.0",
    "packaging==23.1",
    "Pillow==9.4.0",
    "platformdirs==2.6.2",
    "random-address==1.1.1",
    "requests==2.28.2",
    "urllib3==1.26.15"
]

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'flaskapi package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
