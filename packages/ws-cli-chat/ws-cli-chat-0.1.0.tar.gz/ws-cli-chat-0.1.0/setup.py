from setuptools import setup


with open('README.md', 'rt', encoding='utf-8') as arq:
      readme = arq.read()

keywords = ['pychat']

setup(name='ws-cli-chat',
      url='https://github.com/MikalROn/WS-CLI-Chat',
      version='0.1.0',
      license='MIT license',
      author='Daniel Coêlho',
      long_description=readme,
      long_description_content_type='text/markdown',
      author_email='heromon.9010@gmail.com',
      keywords=keywords,
      description='simple cli-websocket-chat',
      packages=['chat'],
      install_requires=['websockets'],
      python_requires='>=3',
)