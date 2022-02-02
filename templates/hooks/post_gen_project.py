import os
import shutil

project_slug = "bentoml_gallery_{{ cookiecutter.__project_dir }}"

def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)

include_tests = '{{cookiecutter.include_tests}}' == 'True'

if not include_tests:
    # remove top-level file inside the generated folder
    remove('samples')
    remove('tests')
