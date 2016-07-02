# The purpose of this script is to extract the features from an audio file and return the feature set.
# The features includes both the 13 - MFCC(Mel Frequency Spectral Coefficients) and 26 - Log Filterbank Energy features.
# An audio file is divided into multiple frames of 25 ms each and the 13 + 26 = 39 features are evaluated for each frame.
# For each feature aggregation is done on all frames and six things are evaluated which are:
# 	1. mean
# 	2. variance
# 	3. maximum
# 	4. minimum
# 	5. mean of first half frames
# 	6. mean of second half frames
# Total number of features returned for an audio input(of any size) are = 6 * (13 + 26) = 39 * 6 = 234
import numpy as np
import scipy.io.wavfile as wav
from features import mfcc, logfbank

class FeatureExtractor():

	def extract_frames_features(self, audio_signal):
		(rate, sig) = audio_signal
		mfcc_features = mfcc(sig, rate)
		fbank_features = logfbank(sig, rate)
		aggregate_features = np.append(mfcc_features, fbank_features, axis = 1)
		return aggregate_features

	def extract_features(self, audio_file=None, audio_signal = None):
		final_features = []
		if audio_file is not None:
			audio_signal = wav.read(audio_file)
			frames_features = self.extract_frames_features(audio_signal)	
		else:
			frames_features = self.extract_frames_features(audio_signal)	
		grouped_per_feature = zip(*frames_features)
		for feature_elements in grouped_per_feature:
			final_features.append(np.mean(feature_elements))
			final_features.append(np.var(feature_elements))
			final_features.append(np.max(feature_elements))
			final_features.append(np.min(feature_elements))
			final_features.append(np.mean(feature_elements[:len(feature_elements)/2]))
			final_features.append(np.mean(feature_elements[len(feature_elements)/2:]))
		return final_features

	def extract_features_per_frame(self, audio_file=None, audio_signal = None):
		if audio_file is not None:
			audio_signal = wav.read(audio_file)
			frames_features = self.extract_frames_features(audio_signal)	
		else:
			frames_features = self.extract_frames_features(audio_signal)	
		return frames_features