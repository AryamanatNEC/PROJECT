import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="shopping_spider",
    version="0.0.1",
    author="Aryaman Mishra",
    author_email="aryamanatnec@gmail.com",
    description=("Grab Data from Google Shopping"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AryamanatNEC/shopping_spider",
    project_urls={
        "Bug Tracker": "https://github.com/AryamanatNEC/shopping_spider/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests","beautifulsoup4"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "testhipify = runner.cli:main",
        ]
    }
) 