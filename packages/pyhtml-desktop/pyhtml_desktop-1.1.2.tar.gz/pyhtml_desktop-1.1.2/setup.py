from setuptools import setup, find_packages

VERSION = '1.1.2' 
DESCRIPTION = 'build desktop apps with Python and HTML'
LONG_DESCRIPTION = 'build desktop apps with Python and HTML'
setup(
        name="pyhtml_desktop", 
        version=VERSION,
        author="Kellan Butler",
        author_email="kellanbutler52@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python', 'html'],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux",
        ],
        project_urls={
            "Github":'https://github.com/kellantech/pyhtmldesktop/'
        }
)