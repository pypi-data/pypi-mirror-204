import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

requirements = [
]

setuptools.setup(
    name='ssenv',
    version='1.0.0',
    author='Jaewook Lee',
    author_email='me@jwlee.xyz',
    description='Super Duper Simple dotenv (.env) handler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/asheswook/Environment',
    project_urls={
        'Bug Tracker': 'https://github.com/asheswook/Environment/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package=setuptools.find_packages(),
    python_requires='>=3.0',
    install_requires=requirements,
)
