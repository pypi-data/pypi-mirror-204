from setuptools import setup, find_packages

version = '0.1.20'


base_packages = ['networkx','leidenalg','autocorrect','xlsxwriter','igraph','matplotlib','numpy','emoji']
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
types_of_encoding = ["utf8", "cp1252"]
with open('README.md',encoding = "utf8") as f:
    long_description = f.read()
 
setup(
  name='keypartx',
  version=version,
  description='A Graph-based Perception(Text) Representation',
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  url='https://github.com/pengKiina/KeypartX',  
  author='Peng Yang',
  author_email='pyseptimo@outlook.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['text representation','text mining','nlp','topic modeling','emoji','image','perception'], 
  packages=find_packages(),
  install_requires= base_packages,
  extras_require = {
        'coreferee_spacy': ['coreferee','spacy<3.4.1,>=3.0.0'] , 'crosslingual-coreference_spacy':['crosslingual-coreference','spacy']
    }
)

# long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
