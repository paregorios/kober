import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kober",
    version="0.0.1",
    author="Tom Elliott",
    author_email="ipse@paregorios.org",
    description="Try systematically to figure out the format of a (text) file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9.7",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=['python-magic', 'regex'],
    python_requires='>=3.9.7'
)
