import setuptools

setuptools.setup(
    name="pyfx-tool",
    version="0.1.0",
    description="Fx (Function eXecution) in Python, inspired by https://www.npmjs.com/package/fx.",
    author="Wu Runfan",
    author_email="alr_public@hotmail.com",
    url="https://github.com/archeraldrich/pyfx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "pyfx=pyfx.pyfx:main",
        ],
    },
    python_requires=">=3.2",
    install_requires=["json-stream-parser>=0.0.1"],
)
