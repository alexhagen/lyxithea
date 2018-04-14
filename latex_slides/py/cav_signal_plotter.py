import sys
import numpy as np
sys.path.append("/Users/ahagen/code");
from ah_py.calc import func as ahm
import numpy as np
import matplotlib.pyplot as mpl

x = [];
y = np.zeros((10000,1));
t = np.array([]);
w_f = np.array([]);

num_val = 0;

f = open("cav_signal_8_4_15_1.dat", 'r');

for line in f:

    if 'starttime:' in line:
        t_s = int(line.replace('starttime:',''));
        #print "the start time is %10.4e" % (t_s);
        # line here includes the start time for a run of 10000 reads
        #print line
    elif 'endtime:' in line:

        t_e = int(line.replace('endtime:',''));
        #print "the end time is %10.4e" % (t_e);
        x = np.linspace(t_s, t_e, 10000);
        t=np.append(t,x);
        w_f = np.append(w_f,y);
        num_val=0;
        # line here includes the end time for a run of 10000 reads
        #print line
    else:
        # line here includes the reading from the adc
        val = int(line);
        y[num_val] = val;
        num_val = num_val+1;

waveform = ahm.curve(t,w_f);
waveform_plot = waveform.plot();
waveform_plot.lines_on();
waveform_plot.markers_off();
waveform_plot.xlim(15010,15025);
waveform_plot.xlabel('Time ($t$) [$ms$]');
waveform_plot.ylabel('ADC Reading ($\\frac{1024\cdot V}{5.0}$) [ ]');
waveform_plot.export('cavitation_with_pzt',sizes=['fp't],formats=['png']);

f.close();
