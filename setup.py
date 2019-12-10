from setuptools import setup

setup(
    name="Validator",
    version="0.1.0",
    description="A wrapper around goodtables-py & table schema CSV validation",
    url="https://github.com/digital-land/validator",
    license="MIT",
    packages=["validator"],
    install_requires=["goodtables",
                      "validators",
                      "cchardet",
                      "click",
                      "bidict",
                      "dateparser",
                      "jinja2",
                      "csvkit",
                      "xlsx2csv",
                      "pandas",
                      "python-magic",
                      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'validate = validator.cli:validate',
        ]
    },
    python_requires=">=3.6",
)
