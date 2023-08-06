import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(name='gpt-scrapper',
                 version="1.0",
                 description='Utility to scrap code from a directory, so GPT can tell you something about it',
                 long_description=long_description,
                 author="danpeczek",
                 url="https://github.com/danpeczek/gpt-scrapper",
                 project_urls={
                     "Bug Tracker": "https://github.com/danpeczek/gpt-scrapper/issues"
                 },
                 # To provide executable scripts, use entry points in preference to the
                 # "scripts" keyword. Entry points provide cross-platform support and allow
                 # pip to create the appropriate form of executable for the target platform.
                 entry_points={
                     'console_scripts': [
                         'gpt-scrapper=gpt_code_scrapper.scrapper:scrap_code'
                     ]
                 },
                 install_requires=["pyyaml", "click"],
                 classifiers=[
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'Operating System :: POSIX',
                     'Programming Language :: Python',
                     'Topic :: Communications :: Email',
                     'Topic :: Software Development :: Bug Tracking',
                     'License :: OSI Approved :: MIT License'
                 ],
                 package_dir={"": "src"},
                 packages=setuptools.find_packages(where="src"),
                 python_requires=">=3.8",
                 license="MIT",
                 )