from setuptools import setup, find_packages

setup(
    name="Astras",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "xgboost",
        "catboost",
    ],
    author="Harshit Singh",
    author_email="harsh502singh@gmail.com",
    url="https://github.com/Harsh502s/Astras",
    description="Package for Classification and Regression",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
