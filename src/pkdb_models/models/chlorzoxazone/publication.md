# Chlorzoxazone simulations
## Figure2 (model performance) 
Figures were created from the base study simulation experiments.\
location: chlorzoxazone/experiments/studies.py
## Figure3 (Prediction of pharmacokinetics based on body weight normalized dose)
Simulation experiment for the dependency of cmax of CZX, 6-OH-CZX and the MR on the CZX dose. \
location: chlorzoxazone/experiments/scans/erstgard2004.py
## Figure4 (Parameter Scans)
Parameter scan for cyp2e1 activity and cyp2e1 Km for doses of 250, 500 and 750 mg. \
location: chlorzoxazone/experiments/scans/pkp_scan.py
## Figure5 (CYP2E1 induction in alcoholic subjects)
Parameter scan for CYP2E1 plotted with data from Girre1994, Lucas1993.\
location: chlorzoxazone/experiments/alcohol_model/girre1994_lucas1993_induction.py
## Figure6 (Predicted pharmacokinetics based in microsomal CYP2E1 concentrations)
Scan for CYP2E1 activity plotted against pkp vs microsmal amount data from Orellana2006, Mishin1998\
locations:\
chlorzoxazone/experiments/scans/orellana2006.py \
chlorzoxazone/experiments/scans/mishin1998.py
## Figure7 (Effect of chronic ethanol consumption on the induction of CYP2E1 and chlorzoxazone pharmacokinetics)
The big alcohol figure consists of ethanol sim experiment Wilkinson1977 (A), The basic alcohol dosing experiment with 
pre, drinking, and withdrawal phase (B, C, D) and Simulation experiments for Mishin1998 (E), Oneta2002 (F, G), and 
Lucas1995 (H).\
locations: \
A: chlorzoxazone/experiments/alcohol_model/wilkinson1977mean.py \
E: chlorzoxazone/experiments/alcohol_model/mishin1998induction.py.py \
B, C, D, F, G, H: chlorzoxazone/experiments/alcohol_model/oneta2002induction.py
## Figure8 (Combined effect of CYP2E1 induction and cirrhosis)
Parameter scans for CYP2E1 activity and the cirrhosis parameter\
locations:\
chlorzoxazone/experiments/scans/cirrhosis_scan.py