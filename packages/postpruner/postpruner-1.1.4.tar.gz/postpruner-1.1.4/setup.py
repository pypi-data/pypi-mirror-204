from setuptools import setup, find_packages

setup(
    name="postpruner",
    version="1.1.4",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            # "postpruner = postpruner.__main__:main",
            "postpruner = postpruner.postpruner:run",
        ],
    },
    install_requires=[
        "torch",
        "transformers",
        "numpy",
        "scipy",
        "cupy-cuda12x",
        "tqdm",
        "datasets"
    ]
)