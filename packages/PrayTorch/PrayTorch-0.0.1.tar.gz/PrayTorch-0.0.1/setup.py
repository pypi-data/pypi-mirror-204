import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PrayTorch',
    description='Hi! It\'s a wrapper for PyTorch training code, hoping to help reduce the complexity of training code in a way that make the training implementation more human-memorable.',
    version='0.0.1',
    packages=setuptools.find_packages(),
    include_package_data=True,
    url="https://github.com/Cathesilta/PrayTorch",
    author='Cathesilta',
    author_email='dliketequila@gmail.com',
    keywords='PyTorch PrayTorch',
    install_requires=[
        'torch',
        'matplotlib',
        'albumentations',
        'seaborn'
    ],
    entry_points={
        'console_scripts': ['praytorch=praytorch.command_line:main'],
    }
)
