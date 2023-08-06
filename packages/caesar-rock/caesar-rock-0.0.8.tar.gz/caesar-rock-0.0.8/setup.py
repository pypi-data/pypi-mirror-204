from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


with open('README.md', 'r') as arq:
    readme = arq.read()

setup(name='caesar-rock',
      version='0.0.8',
      license='MIT',
      long_description= long_description,
      long_description_content_type="text/markdown",
      author='LCCV/UFAL',
      author_email='erasmo.bezerra@lccv.ufal.br',
      description='Package for estimating the confined compressive strength of rock.',
      packages= ['caesarrock'],
      install_requires=['pandas', 'matplotlib', 'numpy', 'sympy'],)