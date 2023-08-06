from distutils.core import setup

setup(
    name='yaypm3',
    version='3.0',
    packages=[
        'yaypm',
        'yaypm.utils',
        'yaypm.utils.resources',
        'yaypm.utils.tester',
        'yaypm.examples',
    ],
    install_requires=[
        'twisted',
    ],
    description='Client lib for yate extmodule',
    author='Daniel Marohn and Youtob Telecom Inc',
    author_email='info@utob.ir',
    url='https://github.com/utob-ir/yaypm',
    download_url='https://github.com/utob-ir/yaypm/archive/3.0.tar.gz',
    keywords=['yate', 'extmodule'],
    license='GPL',
    # Reference: https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License (GPL)',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which python versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
