from __future__ import division
import pyaudio
import scipy.io.wavfile as wav
import math
from os import listdir
from os.path import isfile, join

segments = []

path = "calls"
c_total = 0
c_read = 0
c_skipped = 0
audio_files = [f for f in listdir(path) if isfile(join(path, f))]
for audio_file in audio_files:
    c_total+=1
    print "Reading file: "+str(c_total)
    try:
        rate_sig, sig = wav.read(join(path, audio_file))
        c_read+=1
    except:
        c_skipped+=1
        continue
    for i in range(int(math.ceil(len(sig)/(rate_sig*20)))):
        segments.append(sig[i*(rate_sig*20):i*(rate_sig*20) + rate_sig*20])
print "\n\n"
print "Total files: "+str(c_total)
print "Read files: "+str(c_read)
print "Skipped files:"+str(c_skipped) 
print "Total 20 sec chunks: "+str(len(segments))

FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1024

map_key_to_emotion = {'1':'negative','2':'neutral', '3':'positive'}

p = pyaudio.PyAudio()  
#open stream  
stream = p.open(format = FORMAT,  
                channels = CHANNELS,  
                rate = rate_sig,  
                output = True, frames_per_buffer=rate_sig)  
#read data
count_label = 293   
for segment in segments[293:]:
    count_label+=1
    stream.write(segment[0:int(len(segment)/2)])
    stream.write(segment[int(len(segment)/2):])
    try:
        segment_label = map_key_to_emotion[raw_input(str(count_label)+"> ")]
    except:
        continue
    wav.write("data\\"+segment_label+"_"+str(count_label)+".wav", rate_sig, segment)


#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()  