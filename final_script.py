'''
<Execution script>
This script is the main script that actually returns the analysed emotions present in a set of audio samples.
All the files to be analysed are kept in a folder named 'test_calls'.
The classifer is loaded/trained, each call is analysed and three things are evaluated for each call:
1. Overall call result
2. Transition from first half to second half
3. Emotions in each 20 seconds segments of the call.
Finally, all the results are entered into a csv file for further analysis/visualization.
'''
from __future__ import division
from audio_emotion_analysis import emotion_analysis
import cPickle
import csv
import os
import scipy.io.wavfile as wav
import math
import numpy as np

emo = emotion_analysis.EmotionAnalysis()

csvfile = open('call_analysis.csv', 'wb')
writer = csv.writer(csvfile, delimiter=',')

#Either load a pre-trained existing classifier or train a new classifier.
if(os.path.exists('my_dumped_classifier.pkl')):
	print "Loading existing classifier..."
	with open('my_dumped_classifier.pkl', 'rb') as fid:
	    clf = cPickle.load(fid)
	print "Loaded..."
else:
	print "Building a classifier..."
	print "Loading data..."
	inp, lab = emo.prepare_dataset('data')
	print "Training on the data..."
	clf = emo.train_classifier([inp, lab])
	print "\nClassifier score: "+str(clf.oob_score_)+"\n"
	# save the classifier
	with open('my_dumped_classifier.pkl', 'wb') as fid:
	    cPickle.dump(clf, fid)    

row = ['Name', 'Length of call', 'Overall call result', 'Transition: First half', 'Transition: Second half']
writer.writerow(row)

#Read each audio call present in the folde, perform the analysis and store in the csv file. 
path = 'test_calls'
audio_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
counter = 0
for audio_file in audio_files:
	row = []
	counter += 1
	print "Processing file: "+str(counter)
	try:
		rate_sig, sig = wav.read(os.path.join(path, audio_file))
		complete_call_result = emo.evaluate(clf, audio_signal = (rate_sig, sig))
		first_half_result = emo.evaluate(clf, audio_signal = (rate_sig, sig[:int(len(sig)/2)]))
		second_half_result = emo.evaluate(clf, audio_signal = (rate_sig, sig[int(len(sig)/2):]))
		segment_result = []
		for i in range(int(math.ceil(len(sig)/(rate_sig*20)))):
		    segment_result.append(emo.evaluate(clf, audio_signal = (rate_sig, sig[i*rate_sig*20:i*rate_sig*20+rate_sig*20])))
		row.append(audio_file)
		row.append(str(int((len(sig)/rate_sig)/60))+" min "+str(int((len(sig)/rate_sig)%60))+" sec")
		row.append(complete_call_result)
		row.append(first_half_result)
		row.append(second_half_result)
		row.extend(segment_result)
		writer.writerow(row)
		csvfile.flush()
	except:
		print "Skipping file: "+str(counter)+", name: "+audio_file
csvfile.close()
print "Completed..."