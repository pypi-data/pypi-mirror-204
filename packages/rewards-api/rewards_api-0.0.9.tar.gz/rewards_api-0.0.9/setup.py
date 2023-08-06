import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="rewards_api",
    version="0.0.9",
    author="rewards.ai",
    author_email="proanindyadeep@gmail.com",
    description="rewards api cli package for starting the local rewards server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rewards-ai/rewards-api/tree/latest",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "rewards-envs", 
        "rewards-experimental", 
        "torch", "opencv-python", 
        "flask", "flask_cors", "flasgger", 
        "boto3", "Flask[async]"
        ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "start-rewards-server = rewards_api.cli:main",
        ]
    }
)