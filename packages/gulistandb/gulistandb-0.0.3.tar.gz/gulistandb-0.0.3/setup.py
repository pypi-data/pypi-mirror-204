from setuptools import setup


with open('README.md', 'r', encoding='utf-16') as f:
    long_description = f.read()

setup(
    name='gulistandb',
    version='0.0.3',
    install_requires=[
        'pandas',
        # add more dependencies as needed
    ],
    package_dir={'': 'src'},

    # metadata
    author='Azaz Ahmed Lipu',
    author_email='lipuahmedazaz79@gmail.com',
    description="This is a user-friendly local database package designed for beginners. You don't need to know any query language - simply import the package and use its methods according to the documentation. The data will be automatically saved in a CSV file in a 'data' folder within your current working directory. This package is perfect for small-scale projects or for those who are just getting started with beginner python project",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AzazAhmedLipu79/GuliStan_DB',
    python_requires='>=3'
)
