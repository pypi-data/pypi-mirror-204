from setuptools import setup, find_packages

setup(name="system_superset_driver",version="0.0.7",packages=find_packages(),
      entry_points={
          "shillelagh.adapter": [
              "system = apm_system.apm_adapter:SystemAPI",
          ],
          "sqlalchemy.dialects": [
              "system = apm_system.apm_dialect:SystemDialect",
          ],
      },

      )
