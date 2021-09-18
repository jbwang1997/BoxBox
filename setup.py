from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


if __name__ == '__main__':
    setup(name='boxbox',
          version='0.1',
          description='A tiny toolkit containing box operations.',
          long_description=readme(),
          long_description_content_type='text/markdown',
          author='jbwang1997',
          author_email='jbwang1997@gmail.com',
          keywords='computer vision, box transform, algorithms',
          url='https://github.com/jbwang1997/BoxBox',
          packages=find_packages(),
          license='Apache License 2.0',
          python_requires='>=3.5', # support typeing
          install_requires=[
              'numpy'
          ])
