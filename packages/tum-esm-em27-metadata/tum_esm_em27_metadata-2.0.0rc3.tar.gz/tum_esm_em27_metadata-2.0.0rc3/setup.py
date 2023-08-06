# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tum_esm_em27_metadata']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['pydantic>=1.10.7,<2.0.0', 'tum-esm-utils>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'tum-esm-em27-metadata',
    'version': '2.0.0rc3',
    'description': "Single source of truth for ESM's EM27 measurement logistics",
    'long_description': '# EM27 Metadata\n\n## The purpose of this library\n\nThis repository is the single source of truth for our EM27 measurement logistics: "Where has each station been on each day of measurements?" We selected this format over putting it in a database due to various reasons:\n\n-   Easy to read, modify and extend by selective group members using GitHub permissions\n-   Changes to this are more evident here than in database logs\n-   Versioning (easy to revert mistakes)\n-   Automatic testing of the files integrities\n-   Easy import as a statically typed Python library\n\n<br/>\n\n## How it works\n\nThis repository only contains a Python library to interact with the metadata. The metadata itself is stored in local files or a GitHub repository. The library can load the metadata from both sources and provides a unified interface with static types to access it.\n\n<br/>\n\n## Library Usage\n\nInstall as a library:\n\n```bash\npoetry add tum-esm-em27-metadata\n# or\npip install tum-esm-em27-metadata\n```\n\n```python\nimport tum_esm_em27_metadata\n\nem27_metadata = tum_esm_em27_metadata.load_from_github(\n    github_repository="org-name/repo-name",\n    access_token="your-github-access-token",\n)\n\n# or load it from local files\nem27_metadata = tum_esm_em27_metadata.load_from_local_files(\n    locations_path="location-data/locations.json",\n    sensors_path="location-data/sensors.json",\n    campaigns_path="location-data/campaigns.json",\n)\n\nmetadata = em27_metadata.get(\n    sensor_id = "ma", date = "20220601"\n)\n\nprint(metadata.dict())\n```\n\nPrints out:\n\n```json\n{\n    "sensor_id": "ma",\n    "serial_number": 61,\n    "utc_offset": 0,\n    "pressure_data_source": "ma",\n    "pressure_calibration_factor": 1,\n    "output_calibration_factor": 1,\n    "date": "20220601",\n    "location": {\n        "location_id": "TUM_I",\n        "details": "TUM Dach Innenstadt",\n        "lon": 11.569,\n        "lat": 48.151,\n        "alt": 539\n    }\n}\n```\n\nThe object returned by `em27_metadata.get()` is of type `tum_esm_em27_metadata.types.SensorDataContext`. It is a Pydantic model (https://docs.pydantic.dev/) but can be converted to a dictionary using `metadata.dict()`.\n\nYou can find dummy data in the `data/` folder.\n\n<br/>\n\n## Set up an EM27 Metadata Storage Directory\n\nYou can use the repository https://github.com/tum-esm/em27-metadata-storage-template to create your own repository for storing the metadata. It contains a GitHub Actions workflow that automatically validates the metadata on every commit in any branch.\n\n<br/>\n\n## For Developers\n\nRun tests:\n\n```bash\n# used inside the GitHub CI for this repo\npytest -m "ci"\n\n# used inside the GitHub Actions workflow for storage repos\npytest -m "action"\n\n# can be used for local development (skips pulling from GitHub)\npytest -m "local"\n```\n\nPublish the Package to PyPI:\n\n```bash\npoetry build\npoetry publish\n```\n',
    'author': 'Moritz Makowski',
    'author_email': 'moritz.makowski@tum.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tum-esm/em27-metadata',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
