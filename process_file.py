#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from am_analysis.explore_stfft_ama_gui import calculate_stfft_ama_features
import librosa
import numpy
import sys

if __name__ == "__main__":
    filename = ""
    output_app = ""
    if len(sys.argv) == 3:
        filename = sys.argv[1]
        output_app = sys.argv[2]
    else:
        raise AssertionError('Please provide first argument with the audio \
                             filename and second the output file to append to')
    #% ECG data (1 channel) using STFFT-based Modulation Spectrogram
    #[x, fs] = pickle.load(open( "./example_data/ecg_data.pkl", "rb" ))
    print("Will open "+filename)
    x, fs = librosa.load(filename,sr=8000)
    y=numpy.reshape(x,(x.size,1))
    print(fs,y.shape)

    # STFFT Modulation Spectrogram
    #explore_stfft_ama_gui(y, fs, ['audio'])

    result = calculate_stfft_ama_features(y,fs, ['audio'])

    #print(result)

    power_mod_spec_sum = numpy.sum(result['power_modulation_spectrogram'][:,:,0],0)

    #print(power_mod_spec_sum)

    freq_axis = result['freq_axis']

    #print(freq_axis)

    mode_freq_axis = result['freq_mod_axis']

    #print (mode_freq_axis)

    mod_freq_selection = (result['freq_mod_axis'] < 1.0) | (result['freq_mod_axis'] > 4.0)

    #print(mod_freq_selection)

    power_mod_spec_sum_limited = power_mod_spec_sum

    power_mod_spec_sum_limited[mod_freq_selection] = 0

    #print(power_mod_spec_sum_limited)


    max_index = power_mod_spec_sum_limited.argmax()

    max3_indices = power_mod_spec_sum_limited.argsort()[-3:][::-1]
    #print(max3_indices)

    max3_mean_modulation_freq = mode_freq_axis[max3_indices].mean()

    max_modulation_freq = mode_freq_axis[max_index]

    print(max_modulation_freq,max3_mean_modulation_freq)

    with open(output_app, mode='a') as outf:
        outf.write(filename+','+"%.2f" % max_modulation_freq+','+"%.2f" % max3_mean_modulation_freq+'\n')
