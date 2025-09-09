from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file-organizer",
    version="1.0.0",
    author="File Organizer Team",
    author_email="contact@fileorganizer.com",
    description="A production-ready file organizer with GUI, scheduler, and theme support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-organizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.1.0",
        "schedule>=1.2.0",
        "psutil>=5.9.6",
    ],
    entry_points={
        "console_scripts": [
            "file-organizer=file_organizer.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "file_organizer": ["themes/*.json", "icons/*.png"],
    },
)
