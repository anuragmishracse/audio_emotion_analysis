# audio_emotion_analysis
The objective of this project is to predict the emotion present in any audio file/signal.

##Requirements:
1. Anaconda - This installs python along with most popular python libraries including sklearn. If not already install, install it from https://www.continuum.io/downloads . 
2. python_speech_features
3. pyaudio

The requirements 2 and 3 can be installed by typing:
```
pip install -r requirements.txt
```

##Installation:

Once the requirements are installed, just type
`python setup.py install`

##Preparing dataset:
- Put all the unlabelled audio files in a folder named `calls`, or any other folder and update the name of folder in `label_dataset.py`.
- Run the script `label_dataset.py`. 
	- It will scan all the audio files, create a set of 30 sec audio chunks.
	- It will play each chunk and then ask for a label(positive/neutral/negative).
	- Enter 1 for negative, 2 for neutral and 3 for positive.




