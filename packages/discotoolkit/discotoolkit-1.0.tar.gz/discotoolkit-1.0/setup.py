from setuptools import setup, find_packages

setup(
    name='discotoolkit',
    version='1.0',
    author='Li Mengwei, Rom Uddamvathanak',
    author_email='uddamvathanak_rom@immunol.a-star.edu.sg',
    description="""DISCOtoolkit is an python package that allows users to access data and use the tools provided by the DISCO database. It provides the following functions:
                    Filter and download DISCO data based on sample metadata and cell type information
                    CELLiD: cell type annotation
                    scEnrichment: geneset enrichment using DISCO DEGs
                    CellMapper: project data into DISCO atlas""",
    packages=find_packages(include=["discotoolkit", "discotoolkit.*"]),
    install_requires=[
        'numpy',
        'pandas',
    ],
    python_requires = '>=3.8',
)