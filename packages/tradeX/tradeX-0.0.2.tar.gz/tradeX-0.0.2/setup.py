from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
# with open("requirements.txt", "r") as f:
#     lines = f.readlines()
#     required_pkgs = [item.strip() for item in lines]

new_ver = "0.0.2"
print(f"Building =========================================={new_ver}")
print("packages", setuptools.find_packages(where="."))
setup(
    name='tradeX',
    version=new_ver,
    packages= ["tradeX"],#setuptools.find_packages(where="."),
    # url='https://github.com/TaQuangTu/TaCV',
    license='LICENSE',
    author='TaQuangTu',
    install_requires= [],#required_pkgs,
    author_email='taquangtu132@gmail.com',
    description='Machine learning based crypto currency price prediction',
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
