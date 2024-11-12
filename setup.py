from setuptools import setup, find_packages

setup(
    name='MLconversor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'train-ml=ml_library.main:main'
        ]
    },
    author='Y. Campos, P. Pereira, R. Duarte, J. Perez, G. Pessin, T. Pinto',
    description='Biblioteca para geração e conversão de técnicas de machine learning: decision tree e multilayer perceptron.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ThomasVBP/ML_Convertion-Python_To_StructuredText',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.6',
)
