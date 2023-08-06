## test upload
import setuptools

setuptools.setup(
    name = "roof_mask_Yv8",
    version = "0.5.7",
    author = "Ruixu",
    author_email = "lrxjason@gmail.com",
    description = "upload pip package test",
    long_description = 'package supporing Yolo_v8 roof model backend.',
    long_description_content_type="text/markdown",
    url="https://github.com/lrxjason/roof_model_test/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
