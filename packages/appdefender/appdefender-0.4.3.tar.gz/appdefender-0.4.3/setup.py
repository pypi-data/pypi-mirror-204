from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='appdefender',
    version="0.4.3",
    description='Extrinsec AppDefender: Real time serverless protection',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.extrinsec.com',
    author='Extrinsec LLC',
    author_email='support@extrinsec.com',
    platforms='Linux',
    license='Other/Proprietary License',
    packages=['appdefender'],
    python_requires=">=3.6, <4",
    install_requires=[],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
