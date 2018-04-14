import sys
import numpy as np
sys.path.append("/Users/ahagen/code");
from pymf import ctmfd as ahi
from pyg import twod as ahp
from pym import func as ahm

E = np.linspace(0,20,num=1000);
phi = 0.64*np.multiply(np.exp(-E/1.175),np.sinh(np.sqrt(1.0401*E)));
a = 1;
b = 2.45;
c = 0.1;
phi_dd = a*np.exp(-np.multiply((E-b),(E-b))/(2.0*c*c));
dd_curve = ahm.curve(E,phi_dd);
a = dd_curve.integrate(0,20);
phi_dd = a*np.exp(-np.multiply((E-b),(E-b))/(2.0*c*c));

fiss_curve = ahm.curve(E,np.multiply(E,phi),name='$^{252}Cf$');
dd_curve = ahm.curve(E,np.multiply(E,phi_dd),name='$DD$');

figure = fiss_curve.plot();
figure = dd_curve.plot(addto=figure);
figure.lines_on();
figure.markers_off();
figure.legend();
figure.xlim(0,15);
figure.fill_between(E[E>2.6],np.zeros(np.size(E[E>2.6])),
	np.multiply(E[E>2.6],phi[E>2.6]),fc='#E3AE24');
figure.add_data_pointer(4.5,fiss_curve,'$25\%$ of Fission Signal',place=(6.5,0.3));
figure.xlabel('Energy ($E$) [$MeV$]');
figure.ylabel('Relative Flux '
	+'($E \\varphi \left( E \\right)$) [ ]');
figure.export('../img/p_discrim',sizes=['cs'],
	formats=['pdf', 'pgf'],customsize=[7.25, 5.])
