from setuptools import setup, find_packages
# import codecs
# import os
# 
# here = os.path.abspath(os.path.dirname(__file__))
# 
# with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '''0.11'''
DESCRIPTION = '''Creates a collage from images with OpenCV'''

# Setting up
setup(
    name="cv2_collage_v2",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/cv2_collage_v2',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['a_cv2_easy_resize', 'a_cv_imwrite_imread_plus', 'create_empty_image', 'numpy', 'opencv_python', 'rectangle_packer'],
    keywords=['collage', 'opencv'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['a_cv2_easy_resize', 'a_cv_imwrite_imread_plus', 'create_empty_image', 'numpy', 'opencv_python', 'rectangle_packer'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*