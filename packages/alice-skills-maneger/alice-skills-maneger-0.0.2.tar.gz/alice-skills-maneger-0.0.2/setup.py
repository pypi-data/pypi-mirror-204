import os

from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as file_r:
        requirements = file_r.read().splitlines()
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name='alice-skills-maneger',
    version='0.0.2',
    packages=['alice_skills_manager'],
    install_requires=required('requirements/requirements.txt'),
    tests_require=required('requirements/tests.txt'),
    python_requires='>=3.6',
    url='https://github.com/Alice-IA/alice-skills-manager',
    license='Apache-2.0',
    author='jarbasAI, Alice-IA',
    author_email='jarbasai@mailfence.com, yuiassistant@gmail.com',
    description='Alice Skills Manager',
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': {
            'asm=alice_skills_manager.__main__:main'
        }
    },
)
