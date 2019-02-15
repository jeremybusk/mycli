import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mycli",
    version="0.0.1",
    py_modules=['mycli'],
    include_package_data=True,
    install_requires=[
        'click',
        'click-repl',
        'prompt_toolkit',
        'pyyaml',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        mycli=mycli:cli
    ''',
    author="Jeremy Busk",
    author_email="jeremybusk@gmail.com",
    description="Example cli tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeremybusk/mycli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# from setuptools import setup
# 
# setup(
#     name='click-example-bashcompletion',
#     version='1.0',
#     py_modules=['bashcompletion'],
#     include_package_data=True,
#     install_requires=[
#         'click',
#     ],
#     entry_points='''
#         [console_scripts]
#         bashcompletion=bashcompletion:cli
#     ''',
# )
