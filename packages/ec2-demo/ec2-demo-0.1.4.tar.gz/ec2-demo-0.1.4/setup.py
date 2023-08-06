from setuptools import setup
from ec2_demo import VERSION

with open("README.md", "r") as f:
  description = f.read()

setup(
  name="ec2-demo",
  version=VERSION,
  description="EC2 demo",
  long_description=description,
  long_description_content_type="text/markdown",
  author="jpedro",
  author_email="jpedro.barbosa@gmail.com",
  url="https://github.com/jpedro/ec2-demo",
  download_url="https://github.com/jpedro/ec2-demo/tarball/master",
  keywords="ec2 create delete demo",
  license="MIT",
  python_requires='>=3',
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
  ],
  packages=[
    "ec2_demo",
    "tests",
  ],
  install_requires=[
    "pyyaml",
    "jinja2",
    "requests",
    "boto3",
  ],
  entry_points={
    "console_scripts": [
      "ec2-demo=ec2_demo.cli:main",
    ],
  },
)
