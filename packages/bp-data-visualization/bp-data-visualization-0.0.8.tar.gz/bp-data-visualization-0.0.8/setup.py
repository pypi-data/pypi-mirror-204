import setuptools

setuptools.setup(
    name="bp-data-visualization",
    version="0.0.8",
    author="Bluepinapple",
    author_email="viveksthul@bluepinapple.com",
    description="Show data in charts",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.9.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.20.0",
    ],
)
