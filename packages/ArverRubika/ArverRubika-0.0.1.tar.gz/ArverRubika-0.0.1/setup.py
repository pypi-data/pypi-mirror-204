from setuptools import setup, find_packages

setup(
        # the name must match the folder name 'verysimplemodule'
        name="ArverRubika", 
        version='0.0.1',
        author="Aboli Coder",
        author_email="",
        description='Coding the robot in Rubika in the easiest way !',
        long_description='none',
        packages=find_packages(),
        
        # add any additional packages that 
        # needs to be installed along with your package.
        install_requires=["pycryptodome==3.16.0", "Pillow==9.4.0"], 
        
        keywords=['python', 'rubel', 'Rubika', 'ArverRubika', 'robika', 'robot'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
)
