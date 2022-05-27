import os

from pathlib import Path
from setuptools import find_packages, setup

from core import __version__

PROJECT_DIR = Path(__file__).resolve().parent

with open(PROJECT_DIR / "README.md", "r", encoding="UTF-8") as readme:
    README = readme.read()

# Create logs directory if it doesn't exist yet
if not os.path.exists(PROJECT_DIR / "logs"):
    os.mkdir(PROJECT_DIR / "logs")

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

dev_requirements = ["pre-commit", "pytest", "pytest-cov", "pytest-django", "django-livereload-server==0.4"]

setup(
    name="m183-hack-me",
    version=__version__,
    description="POC for m183 to be tested for penetration.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Yusup Khasbulatov",
    url="https://github.com/khashashin/m183-app",
    download_url="https://github.com/khashashin/m183-app",
    packages=find_packages("."),
    include_package_data=True,
    install_requires=["Django==4.0.4", "python-dotenv==0.20.0", "django-allauth==0.50.0", "django-pwned==.1.1.1"],
    extras_require={"dev": dev_requirements},
    classifiers=[
        "Development Status :: Test/POC",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: Security",
    ],
)
