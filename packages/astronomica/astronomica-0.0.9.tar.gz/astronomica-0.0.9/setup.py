import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='astronomica',
    version='0.0.9',
    author='Siddhu Pendyala',
    author_email='elcientifico.pendyala@gmail.com',
    description='A Python library that deals with astronomy and mathematical calculations. It also helps with Julian Dates',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PyndyalaCoder/astronomica',
    project_urls = {
        "Bug Tracker": "https://github.com/PyndyalaCoder/astronomica/issues"
    },
    license='MIT',
    packages=['astronomica'],
    install_requires=['astroquery', 'requests', 'astropy', 'skyfield', 'matplotlib'],
)
