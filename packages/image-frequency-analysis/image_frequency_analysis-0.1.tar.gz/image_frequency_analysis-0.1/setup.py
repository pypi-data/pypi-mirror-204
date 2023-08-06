from setuptools import setup, find_packages

setup(
    name="image_frequency_analysis",
    version="0.1",
    author="M Thivagar",
    packages=find_packages(),
    install_requires=["opencv-python", "numpy", "pandas", "matplotlib"],
    python_requires=">=3.6",
)
