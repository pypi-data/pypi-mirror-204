
from distutils.core import setup
setup(
  name = 'exceltotable',         # How you named your package folder (MyLib)
  packages = ['exceltotable'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'the way transfer excel,csv,file to database table',   # Give a short description about your library
  author = 'lunongyun',                   # Type in your name
  author_email = '770190990@qq.com',      # Type in your E-Mail
  url = 'https://github.com/user/excel_to_table',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/abocidee/excel_to_table/archive/refs/tags/v1.0.0.tar.gz',    # I explain this later on
  keywords = ['excel', 'table' ],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
       	'argparse',
	'sqlalchemy',
	'pandas',
	'numpy',
	'ms_graph'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
