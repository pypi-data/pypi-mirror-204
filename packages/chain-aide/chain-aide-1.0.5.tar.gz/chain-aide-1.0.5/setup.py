from setuptools import (
    setup,
    find_packages,
)


deps = {
    'chain-aide': [
        'web3>=6.0.0',
        'eth_account>=0.8.0',
        'eth_typing>=3.3.0',
        'eth_utils>=2.1.0',
        'loguru>=0.6.0',
    ]
}

with open('./README.md', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='chain-aide',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='1.0.5',
    description="""An aide that helps you quickly access mainstream public chain and use its basic functions.""",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shinnng',
    author_email='shinnng@outlook.com',
    url='https://github.com/shinnng/chain-aide',
    include_package_data=True,
    install_requires=deps['chain-aide'],
    py_modules=['chain_aide'],
    extras_require=deps,
    license="MIT",
    zip_safe=False,
    package_data={'chain-aide': ['py.typed']},
    keywords='chain',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
