"""AeroPython: An easy to use aerodynamic tool."""

from setuptools import setup, find_packages

setup(name='aeropython',
      version='0.1',
      description='An easy to use aerodynamic tool.',
      author='leal26',
      author_email='leal26@tamu.edu',
      url = 'https://github.com/koentjess/AeroPython',
      license='MIT',
      packages=['aeropython', 'aeropython.CST_2D', 'aeropython.CST_3D',
                'aeropython.morphing', 'aeropython.geometry',
                'aeropython.filehandling', 'aeropython.structural'],
      zip_safe=False,
          package_data={
          # If any package contains *.exe and avian files, include them:
          '': ['*.exe', 'avian'],
          # And include any *.exe files found in the 'CST' package, too:
          'CST': ['*.exe', 'avian'],
          # And include any *.exe files found in the 'geometry' package, too:
          'geometry': ['*.exe'],
      }
      )
