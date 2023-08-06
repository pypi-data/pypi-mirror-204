import os
from setuptools import setup

# with open("README.md", "r") as fh:
#     long_desc = fh.read()


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base_dir, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'ALICE_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name='alice-messagebus-client',
    version='0.10.1',
    packages=['alice_bus_client', 'alice_bus_client.client',
              'alice_bus_client.util'],
    package_data={
      '*': ['*.txt', '*.md']
    },
    include_package_data=True,
    install_requires=required('requirements.txt'),
    url='https://github.com/Alice-IA/alice-messagebus-client',
    license='Apache-2.0',
    author='Mycroft AI, Åke Forslund',
    author_email='devs@mycroft.ai, ake.forslund@gmail.com',
    description='Alice Messagebus Client',
    # long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
