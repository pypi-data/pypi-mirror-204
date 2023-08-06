import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PKG_NAME = 'Perceptron_ndsnajam'
USER_NAME = 'nds-najam'
PROJECT_NAME = 'Perceptron-ndsnajam'

setuptools.setup(
    name = "Perceptron_ndsnajam",
    version = "0.0.2",
    author = USER_NAME,
    author_email="najam.iitm@gmail.com",
    description="Perceptron or/and/xor gates package",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
    project_urls = {
    "Bug Tracker": f"https://github.com/{USER_NAME}/{PROJECT_NAME}/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    install_requires = [
        "numpy==1.21.6",
        "pandas==1.3.5",
        "joblib==1.2.0",
        "matplotlib==3.5.3"
    ]
)
