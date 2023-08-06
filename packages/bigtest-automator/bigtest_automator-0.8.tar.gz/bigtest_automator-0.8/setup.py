from setuptools import setup, find_packages

setup(
    name='bigtest_automator',
    version='0.8',
    author='Shantharam Puranik M',
    author_email='shantharam.puranik@ellucian.com',
    description='A small tool that helps to run and collect performance related metrics such as VMSTAT and AWR. Highly specific to my ORG, might not be useful for general public. SORRY! - Noob.',
    packages=find_packages(),
    install_requires=[
        'scp',
        'paramiko',
        'oracledb'
    ],
    entry_points={
        'console_scripts': [
            'reportscraper=entrypoint.main_class:main',
            # Add other command-line tools here
        ],
    },
)
