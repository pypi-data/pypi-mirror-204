import setuptools
import versioneer


setuptools.setup(
    name='amlopschat',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    keywords='',
    packages=['amlopschat'],
    description='',
    long_description='',
    long_description_content_type="text/markdown",
    install_requires=[],
)
