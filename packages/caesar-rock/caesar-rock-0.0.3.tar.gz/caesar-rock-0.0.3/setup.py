from setuptools import setup

with open('README.md', 'r') as arq:
    readme = arq.read()

setup(name='caesar-rock',
      version='0.0.3',
      license='MIT',
      long_description= readme,
      long_description_content_type="text/markdown",
      author='LCCV/UFAL',
      author_email='erasmo.bezerra@lccv.ufal.br',
      description='Module for calculating the confined compressive strength of rock.',
      packages= ['caesarrock'],
      install_requires=['pandas', 'matplotlib', 'numpy', 'sympy'],)