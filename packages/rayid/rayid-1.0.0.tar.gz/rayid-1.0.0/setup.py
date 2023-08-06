from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='rayid',
    version='1.0.0',
    author='Amirhossein Mohammadi',
    license='MIT',
    author_email="amirhosseinmohammadi1380@yahoo.com",
    description="RayID is a generated code that we use to track logs, posts or events. You can generate your own rayid, but we made your job easier!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BlackIQ/rayid",
    packages=find_packages(),
    install_requires=find_packages()
)
