from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gpt-pynvim",
    version="0.1.0",
    author="Your Name",
    author_email="fumikazu.kiyota@gmail.com",
    description="A neovim plugin to generate code comments using OpenAI API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JFK/gpt-pynvim-plugin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "openai",
        "pynvim",
    ],
)

