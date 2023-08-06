from setuptools import setup, find_packages

setup(
    name='ocr_dict_lookup',
    version='0.1.0',
    description='Extracts highlighted words from images and looks up their meanings in an online dictionary.Basically a tool to help you in your GRE preperation',
    author='Aman Sharma @arcAman07',
    author_email='amananytime07@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'pytesseract',
        'requests'
    ]
)
