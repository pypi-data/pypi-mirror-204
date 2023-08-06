from distutils.core import setup 

setup(
  name = 'conlp',
  packages = ['conlp'],
  version = '0.0.6',
  license='Apache-2.0',
  description = 'TYPE YOUR DESCRIPTION HERE',   
  author = 'Nick S.H Oh',
  author_email = 'nick.sh.oh@socialscience.ai',    
  url = 'https://github.com/SOCIALSCIENCEai/coNLP',  
  download_url = 'https://github.com/SOCIALSCIENCEai/coNLP/archive/refs/tags/0.0.6.tar.gz',
  keywords = ['NLP', 'SOCIAL SCIENCE'],   
  install_requires=[           
          'torch',
          'transformers',
          'transformers[sentencepiece]',
          'scipy',
          'numpy',
          'tqdm'
      ]
)