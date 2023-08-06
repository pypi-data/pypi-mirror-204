from setuptools import setup, find_packages

setup(
    name="image_frequency_analysis",
    version="0.2.0",
    author="M Thivagar",
    packages=find_packages(),
    install_requires=["opencv-python", "numpy", "pandas", "matplotlib"],
    python_requires=">=3.6",
    homepage="https://github.com/thivagar-manickam/image_frequency_analysis",
    description="A package to perform image frequency analysis using the Fourier Transform method",
    bugtracker="https://github.com/thivagar-manickam/image_frequency_analysis/issues",
    readme="README.md",
)
