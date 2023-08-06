import setuptools

setuptools.setup(
    name="bp_data_fabric",
    version="0.0.9",
    author="Bluepinapple",
    author_email="viveksthul@bluepinapple.com",
    description="",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8.10",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.20.0",
        "bp-query-tool >= 0.0.3",
        "bp-data-grid >= 0.0.9",
        "bp-data-visualization >= 0.0.9",
    ],
)
