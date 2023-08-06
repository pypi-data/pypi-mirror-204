import setuptools

packages = setuptools.find_packages(where="src")

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}",
        "dirty_template": "{tag}.dev{ccount}"
    },
    setup_requires=["setuptools-git-versioning"],
    name='ho-protocols',
    description='ProtoBuf definitions for HO components',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hiveopolis/ho-protocols',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ],
    package_dir={'': 'src'},
    packages=packages,
    package_data={
        "ho_protocols": ["py.typed", "*.pyi", "**/*.pyi"]
    },
    install_requires=[
        'protobuf==3.15.5',
    ],
    python_requires='>=3.6'

)
