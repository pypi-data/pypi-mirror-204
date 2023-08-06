from setuptools import setup

readme_content = ""

setup(
    name="python-filter",
    version="1.0.1",
    license="MIT License",
    author="Marcuth",
    long_description=readme_content,
    long_description_content_type="text/plain",
    author_email="marcuth2006@gmail.com",
    keywords="filter tools",
    description=u"Tools for filter items in dict",
    packages=[
        "pyfilter"
    ],
    install_requires=["pydantic"],
)