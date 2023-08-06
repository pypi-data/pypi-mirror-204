from setuptools import setup, find_packages

setup(name="system_superset_driver",version="0.0.18",packages=find_packages(),
      entry_points={
          "shillelagh.adapter": [
              "system = apm_system.apm_adapter:SystemAPI",
          ],
          "sqlalchemy.dialects": [
              "system = apm_system.apm_dialect:SystemDialect",
          ],
      },
      install_requires=(
          "shillelagh >= 1.0.6",
          "sqlalchemy >= 1.3.0",
          "requests >= 2.20.0",
          "psutil",
          "typing-extensions",
      ),
      )
