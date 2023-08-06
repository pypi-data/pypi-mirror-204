from distutils.core import setup
from update import update_version

v = '1.0.1'
current_version = v

setup(
    name='qwertyuiop',
    packages=['qwertyuiop'],
    version=current_version,
    license='MIT',
    description='Machine Learning Models',
    author='Gleb Maksimov',
    author_email='glebmaksimov092@gmail.com',
    download_url=f'https://github.com/Glebmaksimov/maxilaern/archive/refs/tags/{current_version}.tar.gz',
    keywords=['ML', 'FROM SWCRATCH', 'ADVANCED'],
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'scikit-learn',
        'seaborn',
        'IPython'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
update_version()
