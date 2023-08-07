import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="wcmp",
  version="1.0",
  author="moshangsang24",
  author_email="liuyifan731@163.com",
  description="A simple message plus package for notification via wechat.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/moshangsang24/wcmp",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)