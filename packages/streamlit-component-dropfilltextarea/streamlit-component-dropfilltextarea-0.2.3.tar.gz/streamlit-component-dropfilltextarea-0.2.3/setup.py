from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-component-dropfilltextarea",
    version="0.2.3",
    author="Jiayi Chen",
    author_email="chenjiayi_344@hotmail.com",
    description="Streamlit's DropFillTextarea lets users drag and drop files onto a text area, filling in text quickly. It populates text areas with pre-existing files, reducing manual input, while offering layout customization. Ideal for simplifying workflows for both developers and users.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=["streamlit>=1.2", "jinja2"],
)
