from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name='Shyna_speaks',
    version='0.0.7',
    packages=find_packages(),
    author="Shivam Sharma",
    author_email="shivamsharma1913@gmail.com",
    description="Shyna Speak package, Phase one",
    long_description=long_description,
    long_description_content_type="text/markdown",
)

install_requires = ['ShynaDatabase', 'nltk', 'sox', 'setuptools', 'wheel','google_speech']

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
