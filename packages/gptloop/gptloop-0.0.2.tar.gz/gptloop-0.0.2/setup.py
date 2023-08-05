from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name="gptloop",
    version="0.0.2",
    author="Min Cai",
    author_email="min.cai.china@gmail.com",
    description="GPTLoop is a versatile AI-powered assistant to enhance work quality and efficiency",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mcai/GPTLoop",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "gptloop = gptloop.cli:main",
        ],
    },
)
