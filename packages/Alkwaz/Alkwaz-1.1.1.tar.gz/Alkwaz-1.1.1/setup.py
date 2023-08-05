import setuptools

setuptools.setup(
    name="Alkwaz",
    version="1.1.1",
    description="Solve some data analysis problems",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Sajad Beassm",
    author_email="sajad.beassm.bi.2020@uoitc.edu.iq",
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    url="https://github.com/SajadAlkwaz/Alkwaz",
    project_urls={
        "Bug Tracker": "https://github.com/SajadAlkwaz/Alkwaz/issues"
    },
    package_dir={"": "src"}
)
