import sys
import numpy as np
sys.path.append("/Users/ahagen/code")
from pym import func as ahf

f = np.array([1., 2., 6., 10., 20., 60., 100., 200., 600., 1E3, 2E3, 6E3, 10E3,
              20E3, 60E3, 100E3, 200E3, 600E3, 1E6, 2E6, 6E6])
v_out = np.array([34E-3, 44E-3, 72E-3, 91E-3, 144E-3, 344E-3, 469E-3, 600E-3,
                  770E-3, 800E-3, 880E-3, 890E-3, 890E-3, 880E-3, 810E-3,
                  730E-3, 580E-3, 359E-3, 259E-3, 147E-3, 63E-3])
v_in = np.array([1.16, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.16, 1.16, 1.16,
                 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.09,
                 1.00])

freq_response = ahf.curve(f, v_out / v_in)
print v_out / v_in
freq_plot = freq_response.plot()
freq_plot.lines_on()
freq_plot.markers_off()
freq_plot.ax.set_xscale("log", nonposx='clip')
freq_plot.ylim(0., 1.)
freq_plot.ax.set_yticks([0.0, 0.5, 1.0])
freq_plot.ax.set_xticks([10.E0, 10.E3, 10.E6])
freq_plot.xlabel(r'Frequency ($f$) [$Hz$]')
freq_plot.ylabel(r'Gain ($A_{V}$) [ ]')
freq_plot.export('../img/filter_frequency_response', sizes=['cs'], formats=['pdf', 'pgf'],
                 customsize=(0.75, 0.75))
freq_plot.show()
