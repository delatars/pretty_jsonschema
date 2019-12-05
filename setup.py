from setuptools import setup


test_requirements = [
    'pytest==5.3.1'
]

setup(
    name='pretty_jsonschema',
    version='1.0.0',
    description='Helps you simply create and visualize jsonschema.',
    url='https://github.com/delatars/pretty_jsonschema',
    author='Alexandr Morokov',
    author_email='morocov.ap.muz@gmail.com',
    license='MIT',
    zip_safe=True,
    packages=['pretty_jsonschema'],
    test_suite='tests',
    tests_require=test_requirements
)
