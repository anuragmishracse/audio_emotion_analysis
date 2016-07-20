try:
    from setuptools import setup #enables develop
except ImportError:
    from distutils.core import setup

setup(name='audio_emotion_analysis',
      version='0.1',
      description='Audio emotion/sentiment analysis library',
      author='Anurag Mishra',
      author_email='anuragmishracse@gmail.com',
      url='https://github.com/anuragmishracse/audio_emotion_analysis',
      packages=['audio_emotion_analysis'],
    )