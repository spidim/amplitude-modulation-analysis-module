#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from am_analysis.explore_stfft_ama_gui import calculate_stfft_ama_features
import librosa
import numpy
import sys
import csv
import yaml

def update_rates(rates_to_update,fname,mod_spec):
    for key,value in rates_to_update.items():
        if fname in key:
            rates_to_update[key].update({'modulation_peak_freq':mod_spec})
            print("Updated with modulation spec")

if __name__ == "__main__":
    filename = ""
    output_app = ""
    if len(sys.argv) == 4:
        filename = sys.argv[1]
        output_app = sys.argv[2]
        outfilename = sys.argv[3]
    else:
        raise AssertionError('Please provide first argument with mod_spec csv \
                             and second the rate yaml file to update')
    print("Will open "+filename)
    with open(output_app) as yamlfile:
        rates_to_update=yaml.load(yamlfile)
    with open(filename) as csvfile:
        lreader = csv.reader(csvfile, delimiter=',')
        for row in lreader:
            fname='/'.join(row[0].split('/')[5:])
            #print(fname)
            mod_spec = row[1]
            update_rates(rates_to_update,fname,mod_spec)
    print(rates_to_update)
    with open(outfilename,'w+') as outfile:
        outfile.write(yaml.dump(rates_to_update))
