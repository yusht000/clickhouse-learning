__author__ = 'lucky'


from setuptools import setup, find_packages

setup(
    name='mclib',
    version='1.0.0',
    keywords=['mclib'],
    description=' mock data for ck ',
    author='shengtao.yu',
    author_email='yusht000@163.com',
    packages=find_packages(include=['mclib', 'mclib.*']),
    install_requires=[
        'faker',
        'clickhouse-driver',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires=">=3.6",
)
