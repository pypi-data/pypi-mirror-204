import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modnpay-pgsdk",
    version="0.0.1",
    author="seeroo",
    author_email="developers@seeroo.co.kr",
    description="modnpay-pgsdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.seeroo.info/juyeol.jang/modnpay-pgsdk-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
)