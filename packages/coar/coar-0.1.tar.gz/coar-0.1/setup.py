import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='coar',
    version='0.1',
    license='MIT',
    author='Jaroslav Michalovcik',
    author_email='j.michalovcik@gmail.com',
    description='Clustering of association rules based on user defined threshlods.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jmichalovcik/coar",
    packages=setuptools.find_packages(),
    keywords=['association', 'rule', 'clustering', 'association rules', 'association rule clustering'],
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.8',
)
