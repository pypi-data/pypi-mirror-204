import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandas-cat",
    version="0.1.0",
    author="(C) Copyright 2022 - 2023 Petr Masa & LBC",
    author_email="code@cleverminer.org",
    description="Pandas categorical profiling. Generates html profile report for categorical dataset. Also provides several handful functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://petrmasa.com/pandas-cat",
    license = "MIT",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
  	   "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
#	packages=['myapp'],
#   package_dir={'pandas-cat':'pandas-cat'},
    install_requires=['numpy','pandas','seaborn','matplotlib','datasize','jinja2','cleverminer','scikit-learn'],
     package_data={
      'pandas_cat': ['templates/*.tem'],
   },
   include_package_data=True,   
 python_requires=">=3.8"
)