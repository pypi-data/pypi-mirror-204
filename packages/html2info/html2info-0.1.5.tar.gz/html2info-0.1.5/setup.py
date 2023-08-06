import setuptools


def read_requirements(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if not line.startswith("#")]


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="html2info",  # Replace with your package name
    version="0.1.5",  # Replace with your package version
    author="Vladimir Iglovikov",  # Replace with your name
    author_email="iglovikov@gmail.com",  # Replace with your email
    description="A package to parse raw HTML and return structured information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements("requirements.txt"),
)
