from setuptools import setup, find_packages

setup(name="system_superset_driver",version="0.0.1",packages=find_packages(),
      entry_points={
          "shillelagh.adapter": [
              "apm_data = apm_adapter:SystemAPI",
          ],
      },
      )
