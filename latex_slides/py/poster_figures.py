#import recipy
import sys
import numpy as np
sys.path.append("/Users/ahagen/code");
from pynk import ndata as ahs
from pym import func as ahm
from pymf import soa as ahsoa
'''
E_high = 6.00;

E_v,phi_v = np.loadtxt("spectrum_varian.txt",delimiter=',',skiprows=1,unpack=True);
E,phi = np.loadtxt("spectrum_bremsstrahlung.txt",delimiter=',',
	skiprows=1,unpack=True);
#E,phi = np.loadtxt("l3_spectrum.txt",delimiter=',',skiprows=1,unpack=True);
spectrum = ahm.curve(E,phi,name='$6\,MeV$ bremsstrahlung');

spectrum_v = ahm.curve(E_v,phi_v,name='CLINAC 6Ex');
spectrum_v.normalize(norm='int');
spectrum_v_plot = spectrum_v.plot(linestyle='-',linecolor='#E3AE24');
spectrum.normalize(norm='int');
spectrum_v_plot = spectrum.plot(addto=spectrum_v_plot,linestyle='-',linecolor='#7299C6');
spectrum_v_plot.markers_off();
spectrum_v_plot.lines_on();
spectrum_v_plot.legend();
# varian spectrum expected end 5.7513
spectrum_v_plot.add_data_pointer(5.7513,point=0.0,
	place=(2.0,0.3),
	string='Spectrum end\nat energy $ %5.3f \,MeV$' % (5.7513));
spectrum_v_plot.xlim(0.0,7.7614444);
spectrum_v_plot.xlabel('Energy ($E$) [$\mathrm{MeV}$]');
spectrum_v_plot.ylabel('Relative Intensity ($\\theta \left( E \\right)$) [ ]');
spectrum_v_plot.export('../img/spectra',formats=['png','pgf'],sizes=['cs'],
	customsize=[2.5,1.75]);

(E_d,sigma_d) = ahs.import_endf("h2_gnon_endf.txt");
# calculate the percentage of the spectrum above the d threshold
d_xs = ahm.curve(E_d,sigma_d,name='H-2');
perc = spectrum.integrate(2.226,E_high)/spectrum.integrate(0,E_high);
print "Fraction of spectrum above deuterium threshold %f" % \
	( perc );
# calculate the average cross sections, energy weighted
sigma_E_d = [ spectrum.at(E_d[i])*sigma_d[i] for i in range(0,23) ];
d_E_xs = ahm.curve(E_d[:23],sigma_E_d,'E times sigma for d');
xs_gn_d = d_E_xs.integrate(2.226,6)/spectrum.integrate(2.226,6);
print "Average cross section for deuterium (g,n) interaction %f b" % \
	( xs_gn_d );
d_xs_plot = d_xs.plot();
d_xs_plot.markers_off();
d_xs_plot.lines_on();
d_xs_plot.xlim(0,9.0);
d_xs_plot.ylim(0,0.005);
d_xs_plot.xlabel('Energy ($E$) [$\mathrm{MeV}$]');
d_xs_plot.ylabel('Cross Section ($\sigma_{\gamma,n}$) [$\mathrm{b}$]')
d_xs_plot.fill_between(E_d[E_d<=E_high],np.zeros_like(E_d[E_d<=E_high]),
	sigma_d[E_d<=E_high],fc='#E3AE24',
	name='$\int{\sigma_{\left(\gamma,n\\right)}dE}$');
d_xs_plot.add_data_pointer(4.0,point=0.001,
	string="$ \sigma_{sa} = %f\,\mathrm{b}$" % \
	(xs_gn_d),place=(0.5,0.003));
d_xs_plot.legend();
d_xs_plot.export('../img/d_xs',legloc=1,formats=['png','pgf'],sizes=['cs'],customsize=[3.25,2.0]);

(E_be,sigma_be) = ahs.import_endf("be9_gnon_endf.txt");
# calculate the percentage above the Be threshold
be_xs = ahm.curve(E_be,sigma_be,name='Be');
# calculate the average cross sections, energy weighted
(x,) = np.where(E_be <=E_high);
sigma_E_be = [ spectrum.at(E_be[i])*sigma_be[i] for i in x ];
be_E_xs = ahm.curve(E_be[x],sigma_E_be,'E times sigma for be');
xs_gn_be = be_E_xs.integrate(1.666,E_high)/spectrum.integrate(1.666,6);
be_xs_plot = be_xs.plot();
be_xs_plot.markers_off();
be_xs_plot.lines_on();
be_xs_plot.xlim(0,9.0);
be_xs_plot.ylim(0,0.005);
be_xs_plot.xlabel('Energy ($E$) [$\mathrm{MeV}$]');
be_xs_plot.ylabel('Cross Section ($\sigma_{\gamma,n}$) [$\mathrm{b}$]')
be_xs_plot.fill_between(E_be[E_be<=E_high],np.zeros_like(E_be[E_be<=E_high]),
	sigma_be[E_be<=E_high],fc='#E3AE24',
	name='$\int{\sigma_{\left(\gamma,n\\right)}dE}$');
be_xs_plot.add_data_pointer(3.0,point=0.0005,
	string="$ \sigma_{sa} = %f\,\mathrm{b}$" % \
	(xs_gn_be),place=(1,0.003));
be_xs_plot.legend();
be_xs_plot.export('../img/be_xs',legloc=1,formats=['png','pgf'],sizes=['cs'],customsize=[3.25,2.0]);

(E_heu,sigma_heu) = ahs.import_endf("u235_gx_endf.txt");
(E_heu_gf,sigma_heu_gf) = ahs.import_endf("u235_gf_endf.txt");
# calculate the percentage above the heu threshold
heu_xs = ahm.curve(E_heu,sigma_heu,name='U-235 $\left(\gamma,n\\right)$');
heu_xs_gf = ahm.curve(E_heu_gf,sigma_heu_gf,name='U-235 gf');
total = ahm.curve(E_heu_gf,sigma_heu_gf+[heu_xs.at(erg) for erg in E_heu_gf],
	name='U-235 $\left(\gamma,f\\right)$');
# calculate the average cross sections, energy weighted
(x,) = np.where(E_heu <= E_high);
sigma_E_heu = [ spectrum.at(E_heu[i])*sigma_heu[i] for i in x ];
heu_E_xs = ahm.curve(E_heu[x],sigma_E_heu,'E times sigma for heu');
xs_gn_heu = heu_E_xs.integrate(5.25,E_high)/spectrum.integrate(5.25,6);
heu_xs_plot = heu_xs.plot();
heu_xs_plot.xlim(0,9.0);
heu_xs_plot.ylim(1.0E-6,0.02);
heu_xs_plot.xlabel('Energy ($E$) [$\mathrm{MeV}$]');
heu_xs_plot.ylabel('Cross Section ($\sigma_{\gamma,n}$) [$\mathrm{b}$]')
heu_xs_plot.fill_between(E_heu[E_heu<=E_high],np.zeros_like(E_heu[E_heu<=E_high]),
	sigma_heu[E_heu<=E_high],fc='#746C66',
	name='$\int{\sigma_{\left(\gamma,n\\right)}dE}$');
heu_xs_plot.add_data_pointer(5.75,point=0.002,
	string="$ \sigma_{sa,\gamma,n} = %f\,\mathrm{b}$" % \
	(xs_gn_heu),place=(1.0,0.0045));
(x,) = np.where(E_heu_gf <= E_high);
sigma_E_heu_gf = [ spectrum.at(E_heu_gf[i])*sigma_heu_gf[i] for i in x ];
heu_E_xs_gf = ahm.curve(E_heu_gf[x],sigma_E_heu_gf,'E times sigma for heu');
xs_gf_heu = heu_E_xs_gf.integrate(5.0,E_high)/spectrum.integrate(5.0,E_high);
heu_xs_plot = total.plot(addto=heu_xs_plot);
heu_xs_plot.fill_between(E_heu[E_heu<=E_high],
	sigma_heu[E_heu<=E_high],
	[total.at(erg) for erg in E_heu[E_heu<=E_high]],fc='#E3AE24',
	name='$\int{\sigma_{\left(\gamma,f\\right)}dE}$');
heu_xs_plot.add_data_pointer(5.90,point=0.006,
	string="$ \sigma_{sa,\gamma,f} = %f\,\mathrm{b}$" % \
	(xs_gf_heu),place=(1.0,0.008));
heu_xs_plot.markers_off();
heu_xs_plot.lines_on();
heu_xs_plot.legend();
heu_xs_plot.export('../img/heu_xs',legloc=2,formats=['png','pgf'],sizes=['cs'],customsize=[3.25,2.0]);

(E_c,sigma_c) = ahs.import_endf("c13_gx_endf.txt");
# calculate the average cross sections, energy weighted
sigma_E_c = [ spectrum.at(E_c[i])*sigma_c[i] for i in range(0,23) ];
c_E_xs = ahm.curve(E_c[:23],sigma_E_c,'E times sigma for c');
xs_gn_c = c_E_xs.integrate(4.946,6)/spectrum.integrate(4.946,6);
c_xs = ahm.curve(E_c,sigma_c,name='C-13 $\left(\gamma,n\\right)$');
c_xs_plot = c_xs.plot();
c_xs_plot.markers_off();
c_xs_plot.lines_on();
c_xs_plot.xlim(0,9.0);
c_xs_plot.ylim(0,0.001);
c_xs_plot.xlabel('Energy ($E$) [$\mathrm{MeV}$]');
c_xs_plot.ylabel('Cross Section ($\sigma_{\gamma,n}$) [$\mathrm{b}$]')
c_xs_plot.fill_between(E_c[E_c<=E_high],np.zeros_like(E_c[E_c<=E_high]),
	sigma_c[E_c<=E_high],fc='#E3AE24',
	name='$\int{\sigma_{\left(\gamma,n\\right)}dE}$');
c_xs_plot.add_data_pointer(5.5,point=0.0001,
	string="$ \sigma_{sa} = %f\,\mathrm{b}$" % \
	(xs_gn_c),place=(0.5,0.0005));
c_xs_plot.legend();
c_xs_plot.export('../img/c_xs',legloc=1,formats=['png','pgf'],sizes=['cs'],customsize=[3.25,2.0]);


# Now, we plot the r^2 for the spinner as it moves outwards
p = [5.0,6.0,7.0,10.0];
wt = [186.31,4.53,2.81,0.00];
wt_err = [0.00,4.53,1.99,0.00];
p_u = [5.0];
wt_u = [46.216];
wt_u_err = [20.668];
p_be = [5.0];
wt_be = [6.882];
wt_be_err = [3.07];

detection = ahm.curve(p,wt,name='control',u_y=wt_err);
detection_plot = detection.plot();
detection_plot.lines_off();
detection_plot.fill_between(p,wt,200.0*np.ones_like(wt),fc='#A7A9AC',
	name='background');
detection_plot.add_label(7.0,85,'Control/Background')
u_det = ahm.curve(p_u,wt_u,name='U-235',u_y=wt_u_err);
be_det = ahm.curve(p_be,wt_be,name='Be',u_y=wt_be_err);
detection_plot = u_det.plot(addto=detection_plot,linecolor='#E3AE24');
detection_plot = be_det.plot(addto=detection_plot,linecolor='#7299C6');
detection_plot.markers_on();
detection_plot.lines_off();
detection_plot.ylim(0,200.0);
detection_plot.xlim(0,10.0);
detection_plot.add_data_pointer(p_u[0],point=wt_u[0],
	string="NU Detection",place=(1.0,100.0));
detection_plot.add_data_pointer(p_be[0],point=wt_be[0],
	string="Be Detection",place=(2.5,40.0));
detection_plot.xlabel('Pressure ($p$) [$bar$]');
detection_plot.ylabel('Waiting Time ($t_{wait}$) [$s$]');
detection_plot.legend();
detection_plot.export('../img/detection',sizes=['cs'],
	formats=['png','pgf'],customsize=[7.5,2.25]);

x = [];
y = np.zeros((10000,1));
t = np.array([]);
w_f = np.array([]);

num_val = 0;

f = open("cav_signal_8_3_15_4.dat", 'r');

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
waveform.decimate(50.0);
waveform_plot = waveform.plot(linestyle='-',linecolor='#E3AE24');
waveform_plot.add_data_pointer(12000,curve=waveform,
	string="Speed Up $\\rightarrow$ Capactive Charging",place=(30000,50));
waveform_plot.add_data_pointer(17050,curve=waveform,
	string="Cavitation",place=(35000,250));
waveform_plot.add_data_pointer(27000,curve=waveform,
	string="Slow Down $\\rightarrow$ Capacitive Discharing",place=(40000,450));
waveform_plot.lines_on();
waveform_plot.markers_off();
waveform_plot.xlim(10000.0,65000.0);
waveform_plot.xlabel('Time ($t$) [$ms$]');
waveform_plot.ylabel('ADC Reading ($\\frac{1024\cdot V}{5.0}$) [ ]');
waveform_plot.export('../img/unfiltered',sizes=['cs'],formats=['png','pgf'],
	customsize=[7.5,2.25]);
'''
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
waveform_plot = waveform.plot(linestyle='-',linecolor='#E3AE24');
waveform_plot.lines_on();
waveform_plot.markers_off();
waveform_plot.xlim(15010,15025);
waveform_plot.xlabel('Time ($t$) [$ms$]');
waveform_plot.ylabel('ADC Reading ($\\frac{1024\cdot V}{5.0}$) [ ]');
waveform_plot.export('../img/filtered',sizes=['cs'],formats=['png','pgf'],
	customsize=[4.25,2.25]);
