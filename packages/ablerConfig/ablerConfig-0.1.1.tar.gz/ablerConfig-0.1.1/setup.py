from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ablerConfig",
    version="0.1.1",
    author="憨老汉",
    author_email="hh28642257@gmail.com",
    description="配置信息处理包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hanlaohan/abler-config",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[
        'pyjson5',
        'json5'
    ]
)
