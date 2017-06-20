from setuptools import setup

splinter_requires = ['splinter']

setup(name='PyPOM',
      use_scm_version=True,
      description='python page object model for selenium',
      long_description=open('README.rst').read(),
      author='Dave Hunt',
      author_email='dhunt@mozilla.com',
      url='https://github.com/mozilla/PyPOM',
      packages=['pypom', 'pypom.interfaces'],
      install_requires=['zope.interface',
                        'zope.component',
                        'selenium',
                        ],
      setup_requires=['setuptools_scm'],
      extras_require={
          'splinter': splinter_requires,
      },
      license='Mozilla Public License 2.0 (MPL 2.0)',
      keywords='pypom page object model selenium',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Utilities',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6'])
