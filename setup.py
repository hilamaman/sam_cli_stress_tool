from setuptools import setup, find_packages

setup(
    name="cli_stress_tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0,<3",
        "numpy>=1.21.0,<2",
        "setuptools>=58.0.0,<59",
        "loguru>=0.6.0,<0.7",
        "pyyaml>=6.0,<7"
    ],
    entry_points={
        "console_scripts": [
            "cli_stress_tool=cli_stress_tool.main:main",
        ],
    },
    python_requires='>=3.10',
    description="A CLI tool for stress testing of reputation service",
    author="Hila Almalem",
    url="https://github.com/hilamaman/sam_cli_stress_tool",
)