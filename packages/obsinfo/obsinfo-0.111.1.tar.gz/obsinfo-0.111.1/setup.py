import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()
    print(long_description)
    
version={}
with open("obsinfo/version.py") as fp:
    exec(fp.read(),version)

setuptools.setup(
    name="obsinfo",
    version=version['__version__'],
    author="Wayne Crawford",
    author_email="crawford@ipgp.fr",
    description="Tools for documenting ocean bottom seismometer experiments and creating metadata",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://gitlab.com/resif/obsinfo",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'numpy>=1',
          'obspy>=1.1',
          'pyyaml>=3.0',
          'jsonschema>=3.2,<4',
          'python-gitlab>=2.9.0',
          'jsonref>=0.2'
      ],
    entry_points={
        'console_scripts': [
            'obsinfo-validate=obsinfo.console_scripts.validate:main',
            'obsinfo-makeStationXML=obsinfo.console_scripts.makeStationXML:main',
            'obsinfo-print=obsinfo.console_scripts.print:main',
            'obsinfo-setup=obsinfo.console_scripts.setup:main',
            'obsinfo-print_version=obsinfo.console_scripts.print_version:main',
            'obsinfo-test=obsinfo.tests.run_test_script:run_suite_info_files',
            'obsinfo-makescripts_SDPCHAIN=obsinfo.addons.SDPCHAIN:_console_script',
            'obsinfo-makescripts_LCHEAPO=obsinfo.addons.LCHEAPO:_console_script',
            'obsinfo-makescripts_LC2SDS=obsinfo.addons.LC2SDS:_console_script'
        ]
    },
    python_requires='>=3.9',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ),
    keywords='seismology OBS'
)
