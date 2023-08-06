from setuptools import setup,find_packages

setup(
    name="cnki_html2json",
    author = "WangK2",
    author_email = "kw221225@gmail.com",
    version="0.1.1",
    description="A package to convert cnki html to json",
    long_description = open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords = ["cnki","text-structure","crawler"],
    license="MIT",
    url="https://github.com/doublessay/cnki-html2json",
    packages=find_packages(exclude=['test']),
    exclude_package_data={'':['test/*']},
    python_requires=">=3.8.0",
    install_requires=[
        "selenium",
        "lxml",
        "opencv-python",
        "numpy",
        "loguru"],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "cnki-crawler = cnki_html2json.cli:main",
        ]
    },

)