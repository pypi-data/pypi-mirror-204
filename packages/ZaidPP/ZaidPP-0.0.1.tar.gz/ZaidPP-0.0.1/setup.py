import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
f = open("requirements.txt","w")
f.write('instaloder\nuser_agent\nrequests\nuuid')

fr = open("requirements.txt",'r')
requires = fr.read().split('\n')
    
setuptools.setup(
    name="ZaidPP",
    version="0.0.1",
    author="Zaid",
    author_email="www710700@gmail.com",
    description="• Scrape Instagram Profile and login Instagram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requires,
)
