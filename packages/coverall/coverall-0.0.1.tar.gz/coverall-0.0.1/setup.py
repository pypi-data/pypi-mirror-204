from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='coverall',
    version='0.0.1',
    description='Useful tools to work through Exact Cover, Set Cover, and Max Cover Problems',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Brancen Clement',
    author_email='Brancenc@gmail.com',
    keywords=['MaxCover', 'SetCover', 'ExactCover'],
    download_url='https://pypi.org/project/coverall/'
)

install_requires = [
    'bitarray'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)