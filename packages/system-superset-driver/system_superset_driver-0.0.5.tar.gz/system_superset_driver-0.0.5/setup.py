from setuptools import setup, find_packages

setup(name="system_superset_driver",version="0.0.5",packages=find_packages(),
      entry_points={
          "shillelagh.adapter": [
              "system = apm_adapter:SystemAPI",
          ],
          "sqlalchemy.dialects": [
              "system = dialect:SystemDialect",
          ],
      },

      )
