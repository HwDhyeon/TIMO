import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TIMO", # Replace with your own username
    version="0.0.1",
    author="HwDhyeon",
    author_email="dev_donghyun@kakao.com",
    description="test integration management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HwDhyeon/TIMO",
    packages=setuptools.find_packages(exclude=[]),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)
