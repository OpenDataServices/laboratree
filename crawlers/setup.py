from datetime import datetime
from setuptools import setup, find_packages

setup(
    name="laboratree-crawlers",
    version=datetime.utcnow().date().isoformat(),
    classifiers=[],
    keywords="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=["memorious", "datafreeze", "newspaper3k", "dataset", "psycopg2"],
    entry_points={},
)
