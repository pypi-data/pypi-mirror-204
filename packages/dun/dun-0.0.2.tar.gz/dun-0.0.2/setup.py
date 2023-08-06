import setuptools

with open("README.md", "r") as f:
    long_decription = f.read()

with open("requirements.txt", "r") as f:
    install_requires = [l.strip() for l in f.readlines()]

setuptools.setup(
    name="dun",
    version="0.0.2",
    author="Francis Lim",
    author_email="thyeem@gmail.com",
    description="End in one line: forget all the annyoing things",
    long_decription=long_decription,
    long_decription_content_type="text/markdown",
    install_requires=install_requires,
    url="https://github.com/thyeem/__",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security :: Cryptography",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
