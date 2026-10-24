# Chlorzoxazone (CZX) body model

Model `chlorzoxazone_body`, SBML Level 3 Version 2, read from chlorzoxazone\_body.xml, written by sbmlode 0.3.0.

Chlorzoxazone (CZX) body model

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vre}$ | `Vre` | rest of body |  | l |  |
| $\mathrm{Vgu}$ | `Vgu` | gut |  | l |  |
| $\mathrm{Vki}$ | `Vki` | kidney |  | l |  |
| $\mathrm{Vli}$ | `Vli` | liver |  | l |  |
| $\mathrm{Vlu}$ | `Vlu` | lung |  | l |  |
| $\mathrm{Vve}$ | `Vve` | venous blood |  | l |  |
| $\mathrm{Var}$ | `Var` | arterial blood |  | l |  |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vstomach}$ | `Vstomach` | stomach | $1$ | l | ✓ |
| $\mathrm{Vpo}$ | `Vpo` | portal plasma |  | l |  |
| $\mathrm{Vhv}$ | `Vhv` | hepatic venous plasma |  | l |  |
| $\mathrm{Vki}_{\mathrm{tissue}}$ | `Vki_tissue` | ki tissue |  | l |  |
| $\mathrm{Vki}_{\mathrm{plasma}}$ | `Vki_plasma` | ki plasma |  | l |  |
| $\mathrm{Vli}_{\mathrm{tissue}}$ | `Vli_tissue` | li tissue |  | l |  |
| $\mathrm{Vli}_{\mathrm{plasma}}$ | `Vli_plasma` | li plasma |  | l |  |
| $\mathrm{Vlu}_{\mathrm{tissue}}$ | `Vlu_tissue` | lu tissue |  | l |  |
| $\mathrm{Vlu}_{\mathrm{plasma}}$ | `Vlu_plasma` | lu plasma |  | l |  |
| $\mathrm{Vgu}_{\mathrm{tissue}}$ | `Vgu_tissue` | gu tissue |  | l |  |
| $\mathrm{Vgu}_{\mathrm{plasma}}$ | `Vgu_plasma` | gu plasma |  | l |  |
| $\mathrm{Vre}_{\mathrm{tissue}}$ | `Vre_tissue` | re tissue |  | l |  |
| $\mathrm{Vre}_{\mathrm{plasma}}$ | `Vre_plasma` | re plasma |  | l |  |
| $\mathrm{Vgulumen}$ | `Vgulumen` | gut lumen |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vext}}$ | `GU__Vext` | plasma | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{Cki}_{\mathrm{plasma\_czx}}$ | `Cki_plasma_czx` | chlorzoxazone (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_czx}}$ | `Cli_plasma_czx` | chlorzoxazone (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_czx}}$ | `Clu_plasma_czx` | chlorzoxazone (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_czx}}$ | `Cgu_plasma_czx` | chlorzoxazone (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_czx}}$ | `Cre_plasma_czx` | chlorzoxazone (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{czx}}$ | `Car_czx` | chlorzoxazone (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{czx}}$ | `Cve_czx` | chlorzoxazone (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{czx}}$ | `Cpo_czx` | chlorzoxazone (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{czx}}$ | `Chv_czx` | chlorzoxazone (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{czx}}$ | `Clu_czx` | chlorzoxazone (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{czx}}$ | `Cre_czx` | chlorzoxazone (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Afeces}_{\mathrm{czx}}$ | `Afeces_czx` | chlorzoxazone (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Astomach}_{\mathrm{czx}}$ | `Astomach_czx` | chlorzoxazone (stomach) | $\mathrm{Vstomach}$ |  | mmol | amount, boundary |
| $\mathrm{Cki}_{\mathrm{plasma\_czx6oh}}$ | `Cki_plasma_czx6oh` | 6-hydroxychlorzoxazone (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_czx6oh}}$ | `Cli_plasma_czx6oh` | 6-hydroxychlorzoxazone (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_czx6oh}}$ | `Clu_plasma_czx6oh` | 6-hydroxychlorzoxazone (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_czx6oh}}$ | `Cgu_plasma_czx6oh` | 6-hydroxychlorzoxazone (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_czx6oh}}$ | `Cre_plasma_czx6oh` | 6-hydroxychlorzoxazone (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{czx6oh}}$ | `Car_czx6oh` | 6-hydroxychlorzoxazone (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{czx6oh}}$ | `Cve_czx6oh` | 6-hydroxychlorzoxazone (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{czx6oh}}$ | `Cpo_czx6oh` | 6-hydroxychlorzoxazone (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{czx6oh}}$ | `Chv_czx6oh` | 6-hydroxychlorzoxazone (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_czxoglu}}$ | `Cki_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_czxoglu}}$ | `Cli_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_czxoglu}}$ | `Clu_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_czxoglu}}$ | `Cgu_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_czxoglu}}$ | `Cre_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{czxoglu}}$ | `Car_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{czxoglu}}$ | `Cve_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{czxoglu}}$ | `Cpo_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{czxoglu}}$ | `Chv_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{czxoglu}}$ | `Aurine_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Cki}_{\mathrm{plasma\_ethanol}}$ | `Cki_plasma_ethanol` | ethanol (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_ethanol}}$ | `Cli_plasma_ethanol` | ethanol (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_ethanol}}$ | `Clu_plasma_ethanol` | ethanol (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_ethanol}}$ | `Cgu_plasma_ethanol` | ethanol (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_ethanol}}$ | `Cre_plasma_ethanol` | ethanol (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{ethanol}}$ | `Car_ethanol` | ethanol (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{ethanol}}$ | `Cve_ethanol` | ethanol (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{ethanol}}$ | `Cpo_ethanol` | ethanol (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{ethanol}}$ | `Chv_ethanol` | ethanol (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{ethanol}}$ | `Clu_ethanol` | ethanol (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{ethanol}}$ | `Cre_ethanol` | ethanol (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgulumen}_{\mathrm{czx}}$ | `Cgulumen_czx` | chlorzoxazone (gut lumen) | $\mathrm{Vgulumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cveplasma}_{\mathrm{czx}}$ | `Cveplasma_czx` | chlorzoxazone (venous plasma) | $\mathrm{Vve}$ |  | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_czx}}$ | `LI__czx` | chlorzoxazone (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_czx6oh}}$ | `LI__czx6oh` | 6-hydroxychlorzoxazone (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_czxoglu}}$ | `LI__czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_ethanol}}$ | `LI__ethanol` | ethanol (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_cyp2e1}}$ | `LI__cyp2e1` | CYP2E1 | $\mathrm{Vli}_{\mathrm{tissue}}$ | $1$ | \- | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{lumen}}$ | `f_lumen` | fraction lumen of intestine | $0.9$ | \- | ✓ |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{HEIGHT}$ | `HEIGHT` | height \[cm\] | $170$ | cm | ✓ |
| $\mathrm{HR}$ | `HR` | heart rate \[1/min\] | $70$ | 1/min | ✓ |
| $\mathrm{HRrest}$ | `HRrest` | resting heart rate \[1/min\] | $70$ | 1/min | ✓ |
| $\mathrm{BSA}$ | `BSA` | body surface area \[m^2\] |  | m<sup>2</sup> |  |
| $\mathrm{COBW}$ | `COBW` | cardiac output per bodyweight \[ml/s/kg\] | $1.548$ | ml/s/kg | ✓ |
| $\mathrm{CO}$ | `CO` | cardiac output \[ml/s\] |  | ml/s |  |
| $\mathrm{QC}$ | `QC` | cardiac output \[l/min\] |  | l/min |  |
| $\mathrm{COHRI}$ | `COHRI` | increase of cardiac output per heart beat \[ml\] | $150$ | ml | ✓ |
| $\mathrm{Fblood}$ | `Fblood` | blood fraction of organ volume | $0.02$ | \- |  |
| $\mathrm{HCT}$ | `HCT` | hematocrit | $0.51$ | \- | ✓ |
| $\mathrm{FVgu}$ | `FVgu` | gut fractional tissue volume | $0.0171$ | l/kg | ✓ |
| $\mathrm{FVki}$ | `FVki` | kidney fractional tissue volume | $0.0044$ | l/kg | ✓ |
| $\mathrm{FVli}$ | `FVli` | liver fractional tissue volume | $0.021$ | l/kg | ✓ |
| $\mathrm{FVlu}$ | `FVlu` | lung fractional tissue volume | $0.0076$ | l/kg | ✓ |
| $\mathrm{FVre}$ | `FVre` | rest of body fractional tissue volume |  | l/kg |  |
| $\mathrm{FVve}$ | `FVve` | venous fractional tissue volume | $0.0514$ | l/kg | ✓ |
| $\mathrm{FVar}$ | `FVar` | arterial fractional tissue volume | $0.0257$ | l/kg | ✓ |
| $\mathrm{FVpo}$ | `FVpo` | portal fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FVhv}$ | `FVhv` | hepatic venous fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FQgu}$ | `FQgu` | gut fractional tissue blood flow | $0.18$ | \- | ✓ |
| $\mathrm{FQki}$ | `FQki` | kidney fractional tissue blood flow | $0.19$ | \- | ✓ |
| $\mathrm{FQh}$ | `FQh` | hepatic (venous side) fractional tissue blood flow | $0.215$ | \- | ✓ |
| $\mathrm{FQlu}$ | `FQlu` | lung fractional tissue blood flow | $1$ | \- | ✓ |
| $\mathrm{FQre}$ | `FQre` | rest of body fractional tissue blood flow |  | \- |  |
| $f_{\mathrm{cirrhosis}}$ | `f_cirrhosis` | severity of cirrhosis \[0, 0.95\] | $0$ | \- | ✓ |
| $f_{\mathrm{shunts}}$ | `f_shunts` | fraction of portal venous blood shunted by the liver |  | \- |  |
| $f_{\mathrm{tissue\_loss}}$ | `f_tissue_loss` | fraction of lost parenchymal liver volume |  | \- |  |
| $f_{\mathrm{GFR\_Qki}}$ | `f_GFR_Qki` | relationship GFR and Qki | $76.3105006271061$ | ml/l | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) |  | ml/min |  |
| $\mathrm{Mr}_{\mathrm{czx}}$ | `Mr_czx` | Molecular weight czx \[g/mole\] | $169.565$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{czx}}$ | `ftissue_czx` | tissue distribution czx | $10$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{czx}}$ | `Kp_czx` | tissue/plasma partition coefficient czx | $0.1$ | \- | ✓ |
| $\mathrm{BP}_{\mathrm{czx}}$ | `BP_czx` | blood to plasma ratio czx | $0.51$ | \- | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{czx}}$ | `IVDOSE_czx` | IV bolus dose czx \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{czx}}$ | `ti_czx` | injection time czx \[s\] | $10$ | s | ✓ |
| $\mathrm{Ki}_{\mathrm{czx}}$ | `Ki_czx` | Ki \[1/min\] injection czx |  | 1/min |  |
| $\mathrm{Ri}_{\mathrm{czx}}$ | `Ri_czx` | Ri \[mg/min\] rate of infusion czx | $0$ | mg/min | ✓ |
| $\mathrm{cum}_{\mathrm{dose\_czx}}$ | `cum_dose_czx` | Cumulative dose due to infusion czx | $0$ | mg |  |
| $\mathrm{Mr}_{\mathrm{czx6oh}}$ | `Mr_czx6oh` | Molecular weight czx6oh \[g/mole\] | $185.56$ | g/mol | ✓ |
| $\mathrm{Mr}_{\mathrm{czxoglu}}$ | `Mr_czxoglu` | Molecular weight czxoglu \[g/mole\] | $361.69$ | g/mol | ✓ |
| $\mathrm{Mr}_{\mathrm{ethanol}}$ | `Mr_ethanol` | Molecular weight ethanol \[g/mole\] | $46.07$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{ethanol}}$ | `ftissue_ethanol` | tissue distribution ethanol | $1000$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{ethanol}}$ | `Kp_ethanol` | tissue/plasma partition coefficient ethanol | $0.504394256443696$ | \- | ✓ |
| $\mathrm{application}_{\mathrm{form}}$ | `application_form` | application form: 1 solution, otherwise tablet | $0$ | \- | ✓ |
| $\mathrm{PODOSE}_{\mathrm{czx}}$ | `PODOSE_czx` | oral dose czx \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_tablet\_czx}}$ | `Ka_dis_tablet_czx` | dissolution rate czx tablet | $0.564877474211489$ | 1/hr | ✓ |
| $\mathrm{Ka}_{\mathrm{dis\_solution\_czx}}$ | `Ka_dis_solution_czx` | dissolution rate czx solution | $1000$ | 1/hr | ✓ |
| $\mathrm{Qgu}$ | `Qgu` | gut blood flow |  | l/min |  |
| $\mathrm{Qki}$ | `Qki` | kidney blood flow |  | l/min |  |
| $\mathrm{Qh}$ | `Qh` | hepatic (venous side) blood flow |  | l/min |  |
| $\mathrm{Qha}$ | `Qha` | hepatic artery blood flow |  | l/min |  |
| $\mathrm{Qlu}$ | `Qlu` | lung blood flow |  | l/min |  |
| $\mathrm{Qre}$ | `Qre` | rest of body blood flow |  | l/min |  |
| $\mathrm{Qpo}$ | `Qpo` | portal blood flow |  | l/min |  |
| $\mathrm{Aki}_{\mathrm{plasma\_czx}}$ | `Aki_plasma_czx` | chlorzoxazone amount (kidney) \[mmole\] |  | mmol |  |
| $\mathrm{Xki}_{\mathrm{plasma\_czx}}$ | `Xki_plasma_czx` | chlorzoxazone amount (kidney) \[mg\] |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_czx}}$ | `Mki_plasma_czx` | chlorzoxazone concentration (kidney) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_czx}}$ | `Ali_plasma_czx` | chlorzoxazone amount (liver) \[mmole\] |  | mmol |  |
| $\mathrm{Xli}_{\mathrm{plasma\_czx}}$ | `Xli_plasma_czx` | chlorzoxazone amount (liver) \[mg\] |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_czx}}$ | `Mli_plasma_czx` | chlorzoxazone concentration (liver) \[mg/l\] |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_czx}}$ | `Alu_plasma_czx` | chlorzoxazone amount (lung) \[mmole\] |  | mmol |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_czx}}$ | `Xlu_plasma_czx` | chlorzoxazone amount (lung) \[mg\] |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_czx}}$ | `Mlu_plasma_czx` | chlorzoxazone concentration (lung) \[mg/l\] |  | mg/l |  |
| $\mathrm{Agu}_{\mathrm{plasma\_czx}}$ | `Agu_plasma_czx` | chlorzoxazone amount (gut) \[mmole\] |  | mmol |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_czx}}$ | `Xgu_plasma_czx` | chlorzoxazone amount (gut) \[mg\] |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_czx}}$ | `Mgu_plasma_czx` | chlorzoxazone concentration (gut) \[mg/l\] |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_czx}}$ | `Are_plasma_czx` | chlorzoxazone amount (rest) \[mmole\] |  | mmol |  |
| $\mathrm{Xre}_{\mathrm{plasma\_czx}}$ | `Xre_plasma_czx` | chlorzoxazone amount (rest) \[mg\] |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_czx}}$ | `Mre_plasma_czx` | chlorzoxazone concentration (rest) \[mg/l\] |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{czx}}$ | `Aar_czx` | chlorzoxazone amount (arterial blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{czx}}$ | `Xar_czx` | chlorzoxazone amount (arterial blood) \[mg\] |  | mg |  |
| $\mathrm{Mar}_{\mathrm{czx}}$ | `Mar_czx` | chlorzoxazone concentration (arterial blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{czx}}$ | `Ave_czx` | chlorzoxazone amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{czx}}$ | `Xve_czx` | chlorzoxazone amount (venous blood) \[mg\] |  | mg |  |
| $\mathrm{Mve}_{\mathrm{czx}}$ | `Mve_czx` | chlorzoxazone concentration (venous blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{czx}}$ | `Apo_czx` | chlorzoxazone amount (portal vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{czx}}$ | `Xpo_czx` | chlorzoxazone amount (portal vein) \[mg\] |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{czx}}$ | `Mpo_czx` | chlorzoxazone concentration (portal vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{czx}}$ | `Ahv_czx` | chlorzoxazone amount (hepatic vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{czx}}$ | `Xhv_czx` | chlorzoxazone amount (hepatic vein) \[mg\] |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{czx}}$ | `Mhv_czx` | chlorzoxazone concentration (hepatic vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Xfeces}_{\mathrm{czx}}$ | `Xfeces_czx` | chlorzoxazone amount (feces) |  | mg |  |
| $\mathrm{Aki}_{\mathrm{plasma\_czx6oh}}$ | `Aki_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (kidney) \[mmole\] |  | mmol |  |
| $\mathrm{Xki}_{\mathrm{plasma\_czx6oh}}$ | `Xki_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (kidney) \[mg\] |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_czx6oh}}$ | `Mki_plasma_czx6oh` | 6-hydroxychlorzoxazone concentration (kidney) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_czx6oh}}$ | `Ali_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (liver) \[mmole\] |  | mmol |  |
| $\mathrm{Xli}_{\mathrm{plasma\_czx6oh}}$ | `Xli_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (liver) \[mg\] |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_czx6oh}}$ | `Mli_plasma_czx6oh` | 6-hydroxychlorzoxazone concentration (liver) \[mg/l\] |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_czx6oh}}$ | `Alu_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (lung) \[mmole\] |  | mmol |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_czx6oh}}$ | `Xlu_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (lung) \[mg\] |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_czx6oh}}$ | `Mlu_plasma_czx6oh` | 6-hydroxychlorzoxazone concentration (lung) \[mg/l\] |  | mg/l |  |
| $\mathrm{Agu}_{\mathrm{plasma\_czx6oh}}$ | `Agu_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (gut) \[mmole\] |  | mmol |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_czx6oh}}$ | `Xgu_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (gut) \[mg\] |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_czx6oh}}$ | `Mgu_plasma_czx6oh` | 6-hydroxychlorzoxazone concentration (gut) \[mg/l\] |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_czx6oh}}$ | `Are_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (rest) \[mmole\] |  | mmol |  |
| $\mathrm{Xre}_{\mathrm{plasma\_czx6oh}}$ | `Xre_plasma_czx6oh` | 6-hydroxychlorzoxazone amount (rest) \[mg\] |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_czx6oh}}$ | `Mre_plasma_czx6oh` | 6-hydroxychlorzoxazone concentration (rest) \[mg/l\] |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{czx6oh}}$ | `Aar_czx6oh` | 6-hydroxychlorzoxazone amount (arterial blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{czx6oh}}$ | `Xar_czx6oh` | 6-hydroxychlorzoxazone amount (arterial blood) \[mg\] |  | mg |  |
| $\mathrm{Mar}_{\mathrm{czx6oh}}$ | `Mar_czx6oh` | 6-hydroxychlorzoxazone concentration (arterial blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{czx6oh}}$ | `Ave_czx6oh` | 6-hydroxychlorzoxazone amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{czx6oh}}$ | `Xve_czx6oh` | 6-hydroxychlorzoxazone amount (venous blood) \[mg\] |  | mg |  |
| $\mathrm{Mve}_{\mathrm{czx6oh}}$ | `Mve_czx6oh` | 6-hydroxychlorzoxazone concentration (venous blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{czx6oh}}$ | `Apo_czx6oh` | 6-hydroxychlorzoxazone amount (portal vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{czx6oh}}$ | `Xpo_czx6oh` | 6-hydroxychlorzoxazone amount (portal vein) \[mg\] |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{czx6oh}}$ | `Mpo_czx6oh` | 6-hydroxychlorzoxazone concentration (portal vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{czx6oh}}$ | `Ahv_czx6oh` | 6-hydroxychlorzoxazone amount (hepatic vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{czx6oh}}$ | `Xhv_czx6oh` | 6-hydroxychlorzoxazone amount (hepatic vein) \[mg\] |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{czx6oh}}$ | `Mhv_czx6oh` | 6-hydroxychlorzoxazone concentration (hepatic vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Aki}_{\mathrm{plasma\_czxoglu}}$ | `Aki_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (kidney) \[mmole\] |  | mmol |  |
| $\mathrm{Xki}_{\mathrm{plasma\_czxoglu}}$ | `Xki_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (kidney) \[mg\] |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_czxoglu}}$ | `Mki_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (kidney) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_czxoglu}}$ | `Ali_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (liver) \[mmole\] |  | mmol |  |
| $\mathrm{Xli}_{\mathrm{plasma\_czxoglu}}$ | `Xli_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (liver) \[mg\] |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_czxoglu}}$ | `Mli_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (liver) \[mg/l\] |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_czxoglu}}$ | `Alu_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (lung) \[mmole\] |  | mmol |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_czxoglu}}$ | `Xlu_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (lung) \[mg\] |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_czxoglu}}$ | `Mlu_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (lung) \[mg/l\] |  | mg/l |  |
| $\mathrm{Agu}_{\mathrm{plasma\_czxoglu}}$ | `Agu_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (gut) \[mmole\] |  | mmol |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_czxoglu}}$ | `Xgu_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (gut) \[mg\] |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_czxoglu}}$ | `Mgu_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (gut) \[mg/l\] |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_czxoglu}}$ | `Are_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (rest) \[mmole\] |  | mmol |  |
| $\mathrm{Xre}_{\mathrm{plasma\_czxoglu}}$ | `Xre_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (rest) \[mg\] |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_czxoglu}}$ | `Mre_plasma_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (rest) \[mg/l\] |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{czxoglu}}$ | `Aar_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (arterial blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{czxoglu}}$ | `Xar_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (arterial blood) \[mg\] |  | mg |  |
| $\mathrm{Mar}_{\mathrm{czxoglu}}$ | `Mar_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (arterial blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{czxoglu}}$ | `Ave_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{czxoglu}}$ | `Xve_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (venous blood) \[mg\] |  | mg |  |
| $\mathrm{Mve}_{\mathrm{czxoglu}}$ | `Mve_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (venous blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{czxoglu}}$ | `Apo_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (portal vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{czxoglu}}$ | `Xpo_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (portal vein) \[mg\] |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{czxoglu}}$ | `Mpo_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (portal vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{czxoglu}}$ | `Ahv_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (hepatic vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{czxoglu}}$ | `Xhv_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (hepatic vein) \[mg\] |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{czxoglu}}$ | `Mhv_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide concentration (hepatic vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Xurine}_{\mathrm{czxoglu}}$ | `Xurine_czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide amount (urine) \[mg\] |  | mg |  |
| $\mathrm{Aki}_{\mathrm{plasma\_ethanol}}$ | `Aki_plasma_ethanol` | ethanol amount (kidney) \[mmole\] |  | mmol |  |
| $\mathrm{Xki}_{\mathrm{plasma\_ethanol}}$ | `Xki_plasma_ethanol` | ethanol amount (kidney) \[mg\] |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_ethanol}}$ | `Mki_plasma_ethanol` | ethanol concentration (kidney) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_ethanol}}$ | `Ali_plasma_ethanol` | ethanol amount (liver) \[mmole\] |  | mmol |  |
| $\mathrm{Xli}_{\mathrm{plasma\_ethanol}}$ | `Xli_plasma_ethanol` | ethanol amount (liver) \[mg\] |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_ethanol}}$ | `Mli_plasma_ethanol` | ethanol concentration (liver) \[mg/l\] |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_ethanol}}$ | `Alu_plasma_ethanol` | ethanol amount (lung) \[mmole\] |  | mmol |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_ethanol}}$ | `Xlu_plasma_ethanol` | ethanol amount (lung) \[mg\] |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_ethanol}}$ | `Mlu_plasma_ethanol` | ethanol concentration (lung) \[mg/l\] |  | mg/l |  |
| $\mathrm{Agu}_{\mathrm{plasma\_ethanol}}$ | `Agu_plasma_ethanol` | ethanol amount (gut) \[mmole\] |  | mmol |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_ethanol}}$ | `Xgu_plasma_ethanol` | ethanol amount (gut) \[mg\] |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_ethanol}}$ | `Mgu_plasma_ethanol` | ethanol concentration (gut) \[mg/l\] |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_ethanol}}$ | `Are_plasma_ethanol` | ethanol amount (rest) \[mmole\] |  | mmol |  |
| $\mathrm{Xre}_{\mathrm{plasma\_ethanol}}$ | `Xre_plasma_ethanol` | ethanol amount (rest) \[mg\] |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_ethanol}}$ | `Mre_plasma_ethanol` | ethanol concentration (rest) \[mg/l\] |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{ethanol}}$ | `Aar_ethanol` | ethanol amount (arterial blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{ethanol}}$ | `Xar_ethanol` | ethanol amount (arterial blood) \[mg\] |  | mg |  |
| $\mathrm{Mar}_{\mathrm{ethanol}}$ | `Mar_ethanol` | ethanol concentration (arterial blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{ethanol}}$ | `Ave_ethanol` | ethanol amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{ethanol}}$ | `Xve_ethanol` | ethanol amount (venous blood) \[mg\] |  | mg |  |
| $\mathrm{Mve}_{\mathrm{ethanol}}$ | `Mve_ethanol` | ethanol concentration (venous blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{ethanol}}$ | `Apo_ethanol` | ethanol amount (portal vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{ethanol}}$ | `Xpo_ethanol` | ethanol amount (portal vein) \[mg\] |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{ethanol}}$ | `Mpo_ethanol` | ethanol concentration (portal vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{ethanol}}$ | `Ahv_ethanol` | ethanol amount (hepatic vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{ethanol}}$ | `Xhv_ethanol` | ethanol amount (hepatic vein) \[mg\] |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{ethanol}}$ | `Mhv_ethanol` | ethanol concentration (hepatic vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Cve}_{\mathrm{czx6oh\_all}}$ | `Cve_czx6oh_all` | total 6-hydroxychlorzoxazone (free and glucuronide) |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_f\_renal\_function}}$ | `KI__f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_CZXOGLU\_EX\_f}}$ | `KI__CZXOGLU_EX_f` | renal clearance of the glucuronide relative to the GFR | $14.6084423962984$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR}}$ | `KI__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}}$ | `LI__cf_units_per_mmole` | conversion factor for dimensionless species | $1$ | 1/mmol | ✓ |
| $\mathrm{LI}_{\mathrm{\_cyp2e1\_thalf}}$ | `LI__cyp2e1_thalf` | CYP2E1 half life | $2592$ | min | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZX\_k\_IM}}$ | `LI__CZX_k_IM` | rate constant for chlorzoxazone import into the liver | $100$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZX\_F\_EX}}$ | `LI__CZX_F_EX` | liver partition of chlorzoxazone (inverse) | $1.59$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZX6OH\_k\_EX}}$ | `LI__CZX6OH_k_EX` | rate constant for 6-hydroxychlorzoxazone export | $100$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZX6OH\_F\_IM}}$ | `LI__CZX6OH_F_IM` | liver to plasma ratio of 6-hydroxychlorzoxazone | $0.221$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZXOGLU\_k\_EX}}$ | `LI__CZXOGLU_k_EX` | rate constant for 6-hydroxychlorzoxazone-O-glucuronide export | $100$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZXOGLU\_F\_IM}}$ | `LI__CZXOGLU_F_IM` | liver to plasma ratio of 6-hydroxychlorzoxazone-O-glucuronide | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_cyp2e1}}$ | `LI__f_cyp2e1` | CYP2E1 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_cyp2e1\_Km}}$ | `LI__f_cyp2e1_Km` | factor of the Km of CYP2E1 | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZXOX\_Vmax}}$ | `LI__CZXOX_Vmax` | Vmax of the chlorzoxazone 6-hydroxylation | $0.0071748083525124$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZXOX\_Km}}$ | `LI__CZXOX_Km` | Km of the chlorzoxazone 6-hydroxylation | $0.00990140603641784$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_czxother}}$ | `LI__f_czxother` | activity of the CYP2E1 independent elimination | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZXOTHER\_k}}$ | `LI__CZXOTHER_k` | rate constant of the CYP2E1 independent elimination | $0.263160773946114$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_CZXOGLU\_k}}$ | `LI__CZXOGLU_k` | rate constant of the glucuronidation of 6-hydroxychlorzoxazone | $42.7782424502833$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_GLU}}$ | `LI__f_GLU` | UGT activity (6-hydroxychlorzoxazone glucuronidation) | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_ETH\_k\_IM}}$ | `LI__ETH_k_IM` | rate constant for ethanol import into the liver | $100$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_ETHEL\_VMAX}}$ | `LI__ETHEL_VMAX` | rate of ethanol elimination | $0.0485245432051771$ | mmol/min/kg | ✓ |
| $\mathrm{LI}_{\mathrm{\_ETHEL\_KM}}$ | `LI__ETHEL_KM` | Km of the ethanol elimination | $2.17$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_k\_cyp2e1\_prod}}$ | `LI__k_cyp2e1_prod` | rate constant for CYP2E1 production |  | mmol/min/l |  |
| $\mathrm{LI}_{\mathrm{\_k\_cyp2e1\_deg}}$ | `LI__k_cyp2e1_deg` | rate constant for CYP2E1 degradation |  | mmol/min/l |  |
| $\mathrm{LI}_{\mathrm{\_Ki\_cyp2e1\_deg\_ethanol}}$ | `LI__Ki_cyp2e1_deg_ethanol` | stabilization constant (inhibition degradation) | $10^{-5}$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_kd\_cyp2e1}}$ | `LI__kd_cyp2e1` |  |  | mmol/min/l |  |
| $\mathrm{GU}_{\mathrm{\_PODOSE\_ethanol}}$ | `GU__PODOSE_ethanol` | oral ethanol dose \[mg\] | $0$ | mg |  |
| $\mathrm{GU}_{\mathrm{\_F\_czx\_abs}}$ | `GU__F_czx_abs` | fraction absorbed chlorzoxazone | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ka\_abs\_czx}}$ | `GU__Ka_abs_czx` | absorption rate chlorzoxazone | $1.17342368845129$ | 1/hr | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_Ka\_czx}}$ | `GU__f_Ka_czx` | scaling factor of the absorption rate of chlorzoxazone | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ka\_abs\_eth}}$ | `GU__Ka_abs_eth` | absorption rate ethanol | $2.47394678419484$ | 1/hr | ✓ |
| $\mathrm{GU}_{\mathrm{\_absorption}}$ | `GU__absorption` | transport of chlorzoxazone out of the lumen |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{Afeces}_{\mathrm{czx}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{Astomach}_{\mathrm{czx}} &= 1 \cdot \mathrm{Vstomach} \\[1ex]
\mathrm{Aurine}_{\mathrm{czxoglu}} &= 0 \cdot \mathrm{Vurine}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
f_{\mathrm{shunts}} &= f_{\mathrm{cirrhosis}} \\[1ex]
f_{\mathrm{tissue\_loss}} &= f_{\mathrm{cirrhosis}} \\[1ex]
\mathrm{FVre} &= 1 - \mathrm{FVgu} - \mathrm{FVki} - \mathrm{FVli} \\
&\quad {} - \mathrm{FVlu} - \mathrm{FVve} - \mathrm{FVar} \\[1ex]
\mathrm{FQre} &= 1 - \mathrm{FQki} - \mathrm{FQh} \\[1ex]
\mathrm{BSA} &= 0.024265 \cdot \mathopen{}\left(\frac{\mathrm{BW}}{1}\right)^{0.5378} \cdot \mathopen{}\left(\frac{\mathrm{HEIGHT}}{1}\right)^{0.3964} \\[1ex]
\mathrm{CO} &= \mathrm{BW} \cdot \mathrm{COBW} + \frac{\mathopen{}\left(\mathrm{HR} - \mathrm{HRrest}\right) \cdot \mathrm{COHRI}}{60} \\[1ex]
\mathrm{QC} &= \frac{\mathrm{CO}}{1000} \cdot 60 \\[1ex]
\mathrm{Vgu} &= \mathrm{BW} \cdot \mathrm{FVgu} \\[1ex]
\mathrm{Vgulumen} &= f_{\mathrm{lumen}} \cdot \mathrm{Vgu} \\[1ex]
\mathrm{Vki} &= \mathrm{BW} \cdot \mathrm{FVki} \\[1ex]
\mathrm{Vli} &= \mathrm{BW} \cdot \mathrm{FVli} \\[1ex]
\mathrm{Vlu} &= \mathrm{BW} \cdot \mathrm{FVlu} \\[1ex]
\mathrm{Vre} &= \mathrm{BW} \cdot \mathrm{FVre} \\[1ex]
\mathrm{Vve} &= \mathrm{BW} \cdot \mathrm{FVve} - \frac{\mathrm{FVve}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Var} &= \mathrm{BW} \cdot \mathrm{FVar} - \frac{\mathrm{FVar}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Vpo} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVpo} - \frac{\mathrm{FVpo}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Vhv} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVhv} - \frac{\mathrm{FVhv}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Qgu} &= \mathrm{QC} \cdot \mathrm{FQgu} \\[1ex]
\mathrm{Qki} &= \mathrm{QC} \cdot \mathrm{FQki} \\[1ex]
\mathrm{Qh} &= \mathrm{QC} \cdot \mathrm{FQh} \\[1ex]
\mathrm{Qha} &= \mathrm{Qh} - \mathrm{Qgu} \\[1ex]
\mathrm{Qlu} &= \mathrm{QC} \cdot \mathrm{FQlu} \\[1ex]
\mathrm{Qre} &= \mathrm{QC} \cdot \mathrm{FQre} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qgu} \\[1ex]
\mathrm{GFR}_{\mathrm{base}} &= f_{\mathrm{GFR\_Qki}} \cdot \mathrm{Qki} \\[1ex]
\mathrm{Vki}_{\mathrm{plasma}} &= \mathrm{Vki} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vki}_{\mathrm{tissue}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{plasma}} &= \mathrm{Vli} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{tissue}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - f_{\mathrm{tissue\_loss}}\right) \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{plasma}} &= \mathrm{Vlu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{tissue}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{plasma}} &= \mathrm{Vgu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{tissue}} &= \mathrm{Vgu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{plasma}} &= \mathrm{Vre} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{tissue}} &= \mathrm{Vre} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Ki}_{\mathrm{czx}} &= \frac{0.693}{\mathrm{ti}_{\mathrm{czx}}} \cdot 60 \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_czx}} &= \mathrm{Cki}_{\mathrm{plasma\_czx}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_czx}} &= \mathrm{Aki}_{\mathrm{plasma\_czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_czx}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_czx}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_czx}} &= \mathrm{Cli}_{\mathrm{plasma\_czx}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_czx}} &= \mathrm{Ali}_{\mathrm{plasma\_czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_czx}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_czx}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_czx}} &= \mathrm{Clu}_{\mathrm{plasma\_czx}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_czx}} &= \mathrm{Alu}_{\mathrm{plasma\_czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_czx}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_czx}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_czx}} &= \mathrm{Cgu}_{\mathrm{plasma\_czx}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_czx}} &= \mathrm{Agu}_{\mathrm{plasma\_czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_czx}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_czx}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_czx}} &= \mathrm{Cre}_{\mathrm{plasma\_czx}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_czx}} &= \mathrm{Are}_{\mathrm{plasma\_czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_czx}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_czx}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Aar}_{\mathrm{czx}} &= \mathrm{Car}_{\mathrm{czx}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{czx}} &= \mathrm{Aar}_{\mathrm{czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mar}_{\mathrm{czx}} &= \frac{\mathrm{Aar}_{\mathrm{czx}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Ave}_{\mathrm{czx}} &= \mathrm{Cve}_{\mathrm{czx}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{czx}} &= \mathrm{Ave}_{\mathrm{czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mve}_{\mathrm{czx}} &= \frac{\mathrm{Ave}_{\mathrm{czx}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Apo}_{\mathrm{czx}} &= \mathrm{Cpo}_{\mathrm{czx}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{czx}} &= \mathrm{Apo}_{\mathrm{czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mpo}_{\mathrm{czx}} &= \frac{\mathrm{Apo}_{\mathrm{czx}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Ahv}_{\mathrm{czx}} &= \mathrm{Chv}_{\mathrm{czx}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{czx}} &= \mathrm{Ahv}_{\mathrm{czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Mhv}_{\mathrm{czx}} &= \frac{\mathrm{Ahv}_{\mathrm{czx}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Xfeces}_{\mathrm{czx}} &= \mathrm{Afeces}_{\mathrm{czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Cki}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Aki}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_czx6oh}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_czx6oh}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Cli}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Ali}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_czx6oh}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_czx6oh}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Clu}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Alu}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_czx6oh}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_czx6oh}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Cgu}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Agu}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_czx6oh}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_czx6oh}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Cre}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_czx6oh}} &= \mathrm{Are}_{\mathrm{plasma\_czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_czx6oh}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_czx6oh}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Aar}_{\mathrm{czx6oh}} &= \mathrm{Car}_{\mathrm{czx6oh}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{czx6oh}} &= \mathrm{Aar}_{\mathrm{czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mar}_{\mathrm{czx6oh}} &= \frac{\mathrm{Aar}_{\mathrm{czx6oh}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Ave}_{\mathrm{czx6oh}} &= \mathrm{Cve}_{\mathrm{czx6oh}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{czx6oh}} &= \mathrm{Ave}_{\mathrm{czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mve}_{\mathrm{czx6oh}} &= \frac{\mathrm{Ave}_{\mathrm{czx6oh}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Apo}_{\mathrm{czx6oh}} &= \mathrm{Cpo}_{\mathrm{czx6oh}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{czx6oh}} &= \mathrm{Apo}_{\mathrm{czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mpo}_{\mathrm{czx6oh}} &= \frac{\mathrm{Apo}_{\mathrm{czx6oh}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Ahv}_{\mathrm{czx6oh}} &= \mathrm{Chv}_{\mathrm{czx6oh}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{czx6oh}} &= \mathrm{Ahv}_{\mathrm{czx6oh}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Mhv}_{\mathrm{czx6oh}} &= \frac{\mathrm{Ahv}_{\mathrm{czx6oh}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{czx6oh}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Cki}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Aki}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_czxoglu}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_czxoglu}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Cli}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Ali}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_czxoglu}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_czxoglu}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Clu}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Alu}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_czxoglu}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_czxoglu}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Cgu}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Agu}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_czxoglu}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_czxoglu}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Cre}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_czxoglu}} &= \mathrm{Are}_{\mathrm{plasma\_czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_czxoglu}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_czxoglu}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Aar}_{\mathrm{czxoglu}} &= \mathrm{Car}_{\mathrm{czxoglu}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{czxoglu}} &= \mathrm{Aar}_{\mathrm{czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mar}_{\mathrm{czxoglu}} &= \frac{\mathrm{Aar}_{\mathrm{czxoglu}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Ave}_{\mathrm{czxoglu}} &= \mathrm{Cve}_{\mathrm{czxoglu}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{czxoglu}} &= \mathrm{Ave}_{\mathrm{czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mve}_{\mathrm{czxoglu}} &= \frac{\mathrm{Ave}_{\mathrm{czxoglu}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Apo}_{\mathrm{czxoglu}} &= \mathrm{Cpo}_{\mathrm{czxoglu}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{czxoglu}} &= \mathrm{Apo}_{\mathrm{czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mpo}_{\mathrm{czxoglu}} &= \frac{\mathrm{Apo}_{\mathrm{czxoglu}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Ahv}_{\mathrm{czxoglu}} &= \mathrm{Chv}_{\mathrm{czxoglu}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{czxoglu}} &= \mathrm{Ahv}_{\mathrm{czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Mhv}_{\mathrm{czxoglu}} &= \frac{\mathrm{Ahv}_{\mathrm{czxoglu}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Xurine}_{\mathrm{czxoglu}} &= \mathrm{Aurine}_{\mathrm{czxoglu}} \cdot \mathrm{Mr}_{\mathrm{czxoglu}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_ethanol}} &= \mathrm{Cki}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_ethanol}} &= \mathrm{Aki}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_ethanol}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_ethanol}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_ethanol}} &= \mathrm{Cli}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_ethanol}} &= \mathrm{Ali}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_ethanol}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_ethanol}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_ethanol}} &= \mathrm{Clu}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_ethanol}} &= \mathrm{Alu}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_ethanol}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_ethanol}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_ethanol}} &= \mathrm{Cgu}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_ethanol}} &= \mathrm{Agu}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_ethanol}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_ethanol}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_ethanol}} &= \mathrm{Cre}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_ethanol}} &= \mathrm{Are}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_ethanol}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_ethanol}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Aar}_{\mathrm{ethanol}} &= \mathrm{Car}_{\mathrm{ethanol}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{ethanol}} &= \mathrm{Aar}_{\mathrm{ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mar}_{\mathrm{ethanol}} &= \frac{\mathrm{Aar}_{\mathrm{ethanol}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Ave}_{\mathrm{ethanol}} &= \mathrm{Cve}_{\mathrm{ethanol}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{ethanol}} &= \mathrm{Ave}_{\mathrm{ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mve}_{\mathrm{ethanol}} &= \frac{\mathrm{Ave}_{\mathrm{ethanol}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Apo}_{\mathrm{ethanol}} &= \mathrm{Cpo}_{\mathrm{ethanol}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{ethanol}} &= \mathrm{Apo}_{\mathrm{ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mpo}_{\mathrm{ethanol}} &= \frac{\mathrm{Apo}_{\mathrm{ethanol}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Ahv}_{\mathrm{ethanol}} &= \mathrm{Chv}_{\mathrm{ethanol}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{ethanol}} &= \mathrm{Ahv}_{\mathrm{ethanol}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Mhv}_{\mathrm{ethanol}} &= \frac{\mathrm{Ahv}_{\mathrm{ethanol}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \\[1ex]
\mathrm{Cve}_{\mathrm{czx6oh\_all}} &= \frac{\mathrm{Ave}_{\mathrm{czxoglu}} + \mathrm{Ave}_{\mathrm{czx6oh}}}{\mathrm{Vve}} \\[1ex]
\mathrm{Cveplasma}_{\mathrm{czx}} &= \frac{\mathrm{Cve}_{\mathrm{czx}}}{\mathrm{BP}_{\mathrm{czx}}} \\[1ex]
\mathrm{KI}_{\mathrm{\_GFR}} &= \mathrm{KI}_{\mathrm{\_f\_renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
\mathrm{LI}_{\mathrm{\_k\_cyp2e1\_deg}} &= \frac{\frac{1 \cdot 0.693}{\mathrm{LI}_{\mathrm{\_cyp2e1\_thalf}}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_kd\_cyp2e1}} &= \frac{\mathrm{LI}_{\mathrm{\_k\_cyp2e1\_deg}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_ethanol}}}{\mathrm{LI}_{\mathrm{\_Ki\_cyp2e1\_deg\_ethanol}}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_k\_cyp2e1\_prod}} &= \mathrm{LI}_{\mathrm{\_k\_cyp2e1\_deg}} \\[1ex]
\mathrm{GU}_{\mathrm{\_absorption}} &= \frac{\mathrm{GU}_{\mathrm{\_f\_Ka\_czx}} \cdot \mathrm{GU}_{\mathrm{\_Ka\_abs\_czx}}}{60} \cdot \mathrm{Vgu} \cdot \mathrm{Cgulumen}_{\mathrm{czx}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{transport\_lu\_czx}}$ | `transport_lu_czx` | transport chlorzoxazone | $\mathrm{Clu}_{\mathrm{plasma\_czx}} \rightleftharpoons \mathrm{Clu}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{transport\_re\_czx}}$ | `transport_re_czx` | transport chlorzoxazone | $\mathrm{Cre}_{\mathrm{plasma\_czx}} \rightleftharpoons \mathrm{Cre}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{iv\_czx}}$ | `iv_czx` | iv chlorzoxazone | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_czx}}$ | `Flow_ar_ki_czx` | inflow kidney chlorzoxazone | $\mathrm{Car}_{\mathrm{czx}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_czx}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_czx}}$ | `Flow_ki_ve_czx` | outflow kidney chlorzoxazone | $\mathrm{Cki}_{\mathrm{plasma\_czx}} \longrightarrow \mathrm{Cve}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_czx}}$ | `Flow_arli_li_czx` | arterial inflow liver chlorzoxazone | $\mathrm{Car}_{\mathrm{czx}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_czx}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_czx}}$ | `Flow_arli_hv_czx` | flow arterial shunts | $\mathrm{Car}_{\mathrm{czx}} \longrightarrow \mathrm{Chv}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_czx}}$ | `Flow_po_li_czx` | outflow po chlorzoxazone | $\mathrm{Cpo}_{\mathrm{czx}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_czx}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_czx}}$ | `Flow_po_hv_czx` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{czx}} \longrightarrow \mathrm{Chv}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_czx}}$ | `Flow_li_hv_czx` | outflow liver chlorzoxazone | $\mathrm{Cli}_{\mathrm{plasma\_czx}} \longrightarrow \mathrm{Chv}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_czx}}$ | `Flow_hv_ve_czx` | outflow hepatic vein chlorzoxazone | $\mathrm{Chv}_{\mathrm{czx}} \longrightarrow \mathrm{Cve}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_czx}}$ | `Flow_ve_lu_czx` | inflow lung chlorzoxazone | $\mathrm{Cve}_{\mathrm{czx}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_czx}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_czx}}$ | `Flow_lu_ar_czx` | outflow lung chlorzoxazone | $\mathrm{Clu}_{\mathrm{plasma\_czx}} \longrightarrow \mathrm{Car}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_czx}}$ | `Flow_ar_gu_czx` | inflow gut chlorzoxazone | $\mathrm{Car}_{\mathrm{czx}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_czx}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_czx}}$ | `Flow_gu_po_czx` | outflow gut chlorzoxazone | $\mathrm{Cgu}_{\mathrm{plasma\_czx}} \longrightarrow \mathrm{Cpo}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_czx}}$ | `Flow_ar_re_czx` | inflow rest chlorzoxazone | $\mathrm{Car}_{\mathrm{czx}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_czx}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_czx}}$ | `Flow_re_ve_czx` | outflow rest chlorzoxazone | $\mathrm{Cre}_{\mathrm{plasma\_czx}} \longrightarrow \mathrm{Cve}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_czx6oh}}$ | `Flow_ar_ki_czx6oh` | inflow kidney 6-hydroxychlorzoxazone | $\mathrm{Car}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_czx6oh}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_czx6oh}}$ | `Flow_ki_ve_czx6oh` | outflow kidney 6-hydroxychlorzoxazone | $\mathrm{Cki}_{\mathrm{plasma\_czx6oh}} \longrightarrow \mathrm{Cve}_{\mathrm{czx6oh}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_czx6oh}}$ | `Flow_arli_li_czx6oh` | arterial inflow liver 6-hydroxychlorzoxazone | $\mathrm{Car}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_czx6oh}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_czx6oh}}$ | `Flow_arli_hv_czx6oh` | flow arterial shunts | $\mathrm{Car}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Chv}_{\mathrm{czx6oh}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_czx6oh}}$ | `Flow_po_li_czx6oh` | outflow po 6-hydroxychlorzoxazone | $\mathrm{Cpo}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_czx6oh}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_czx6oh}}$ | `Flow_po_hv_czx6oh` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Chv}_{\mathrm{czx6oh}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_czx6oh}}$ | `Flow_li_hv_czx6oh` | outflow liver 6-hydroxychlorzoxazone | $\mathrm{Cli}_{\mathrm{plasma\_czx6oh}} \longrightarrow \mathrm{Chv}_{\mathrm{czx6oh}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_czx6oh}}$ | `Flow_hv_ve_czx6oh` | outflow hepatic vein 6-hydroxychlorzoxazone | $\mathrm{Chv}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Cve}_{\mathrm{czx6oh}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_czx6oh}}$ | `Flow_ve_lu_czx6oh` | inflow lung 6-hydroxychlorzoxazone | $\mathrm{Cve}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_czx6oh}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_czx6oh}}$ | `Flow_lu_ar_czx6oh` | outflow lung 6-hydroxychlorzoxazone | $\mathrm{Clu}_{\mathrm{plasma\_czx6oh}} \longrightarrow \mathrm{Car}_{\mathrm{czx6oh}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_czx6oh}}$ | `Flow_ar_gu_czx6oh` | inflow gut 6-hydroxychlorzoxazone | $\mathrm{Car}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_czx6oh}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_czx6oh}}$ | `Flow_gu_po_czx6oh` | outflow gut 6-hydroxychlorzoxazone | $\mathrm{Cgu}_{\mathrm{plasma\_czx6oh}} \longrightarrow \mathrm{Cpo}_{\mathrm{czx6oh}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_czx6oh}}$ | `Flow_ar_re_czx6oh` | inflow rest 6-hydroxychlorzoxazone | $\mathrm{Car}_{\mathrm{czx6oh}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_czx6oh}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_czx6oh}}$ | `Flow_re_ve_czx6oh` | outflow rest 6-hydroxychlorzoxazone | $\mathrm{Cre}_{\mathrm{plasma\_czx6oh}} \longrightarrow \mathrm{Cve}_{\mathrm{czx6oh}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_czxoglu}}$ | `Flow_ar_ki_czxoglu` | inflow kidney 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Car}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_czxoglu}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_czxoglu}}$ | `Flow_ki_ve_czxoglu` | outflow kidney 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Cki}_{\mathrm{plasma\_czxoglu}} \longrightarrow \mathrm{Cve}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_czxoglu}}$ | `Flow_arli_li_czxoglu` | arterial inflow liver 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Car}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_czxoglu}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_czxoglu}}$ | `Flow_arli_hv_czxoglu` | flow arterial shunts | $\mathrm{Car}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Chv}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_czxoglu}}$ | `Flow_po_li_czxoglu` | outflow po 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Cpo}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_czxoglu}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_czxoglu}}$ | `Flow_po_hv_czxoglu` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Chv}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_czxoglu}}$ | `Flow_li_hv_czxoglu` | outflow liver 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Cli}_{\mathrm{plasma\_czxoglu}} \longrightarrow \mathrm{Chv}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_czxoglu}}$ | `Flow_hv_ve_czxoglu` | outflow hepatic vein 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Chv}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Cve}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_czxoglu}}$ | `Flow_ve_lu_czxoglu` | inflow lung 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Cve}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_czxoglu}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_czxoglu}}$ | `Flow_lu_ar_czxoglu` | outflow lung 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Clu}_{\mathrm{plasma\_czxoglu}} \longrightarrow \mathrm{Car}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_czxoglu}}$ | `Flow_ar_gu_czxoglu` | inflow gut 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Car}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_czxoglu}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_czxoglu}}$ | `Flow_gu_po_czxoglu` | outflow gut 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Cgu}_{\mathrm{plasma\_czxoglu}} \longrightarrow \mathrm{Cpo}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_czxoglu}}$ | `Flow_ar_re_czxoglu` | inflow rest 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Car}_{\mathrm{czxoglu}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_czxoglu}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_czxoglu}}$ | `Flow_re_ve_czxoglu` | outflow rest 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Cre}_{\mathrm{plasma\_czxoglu}} \longrightarrow \mathrm{Cve}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{transport\_lu\_ethanol}}$ | `transport_lu_ethanol` | transport ethanol | $\mathrm{Clu}_{\mathrm{plasma\_ethanol}} \rightleftharpoons \mathrm{Clu}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{transport\_re\_ethanol}}$ | `transport_re_ethanol` | transport ethanol | $\mathrm{Cre}_{\mathrm{plasma\_ethanol}} \rightleftharpoons \mathrm{Cre}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_ethanol}}$ | `Flow_ar_ki_ethanol` | inflow kidney ethanol | $\mathrm{Car}_{\mathrm{ethanol}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_ethanol}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_ethanol}}$ | `Flow_ki_ve_ethanol` | outflow kidney ethanol | $\mathrm{Cki}_{\mathrm{plasma\_ethanol}} \longrightarrow \mathrm{Cve}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_ethanol}}$ | `Flow_arli_li_ethanol` | arterial inflow liver ethanol | $\mathrm{Car}_{\mathrm{ethanol}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_ethanol}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_ethanol}}$ | `Flow_arli_hv_ethanol` | flow arterial shunts | $\mathrm{Car}_{\mathrm{ethanol}} \longrightarrow \mathrm{Chv}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_ethanol}}$ | `Flow_po_li_ethanol` | outflow po ethanol | $\mathrm{Cpo}_{\mathrm{ethanol}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_ethanol}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_ethanol}}$ | `Flow_po_hv_ethanol` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{ethanol}} \longrightarrow \mathrm{Chv}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_ethanol}}$ | `Flow_li_hv_ethanol` | outflow liver ethanol | $\mathrm{Cli}_{\mathrm{plasma\_ethanol}} \longrightarrow \mathrm{Chv}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_ethanol}}$ | `Flow_hv_ve_ethanol` | outflow hepatic vein ethanol | $\mathrm{Chv}_{\mathrm{ethanol}} \longrightarrow \mathrm{Cve}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_ethanol}}$ | `Flow_ve_lu_ethanol` | inflow lung ethanol | $\mathrm{Cve}_{\mathrm{ethanol}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_ethanol}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_ethanol}}$ | `Flow_lu_ar_ethanol` | outflow lung ethanol | $\mathrm{Clu}_{\mathrm{plasma\_ethanol}} \longrightarrow \mathrm{Car}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_ethanol}}$ | `Flow_ar_gu_ethanol` | inflow gut ethanol | $\mathrm{Car}_{\mathrm{ethanol}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_ethanol}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_ethanol}}$ | `Flow_gu_po_ethanol` | outflow gut ethanol | $\mathrm{Cgu}_{\mathrm{plasma\_ethanol}} \longrightarrow \mathrm{Cpo}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_ethanol}}$ | `Flow_ar_re_ethanol` | inflow rest ethanol | $\mathrm{Car}_{\mathrm{ethanol}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_ethanol}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_ethanol}}$ | `Flow_re_ve_ethanol` | outflow rest ethanol | $\mathrm{Cre}_{\mathrm{plasma\_ethanol}} \longrightarrow \mathrm{Cve}_{\mathrm{ethanol}}$ |  |
| $v_{\mathrm{dissolution\_czx}}$ | `dissolution_czx` | dissolution chlorzoxazone | $\mathrm{Astomach}_{\mathrm{czx}} \longrightarrow \mathrm{Cgulumen}_{\mathrm{czx}}$ |  |
| $v_{\mathrm{KI\_\_CZXOGLU\_EX}}$ | `KI__CZXOGLU_EX` | excretion 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{Cki}_{\mathrm{plasma\_czxoglu}} \longrightarrow \mathrm{Aurine}_{\mathrm{czxoglu}}$ |  |
| $v_{\mathrm{LI\_\_CZXIM}}$ | `LI__CZXIM` | chlorzoxazone import | $\mathrm{Cli}_{\mathrm{plasma\_czx}} \rightleftharpoons \mathrm{LI}_{\mathrm{\_czx}}$ |  |
| $v_{\mathrm{LI\_\_CZX6OHEX}}$ | `LI__CZX6OHEX` | 6-hydroxychlorzoxazone export | $\mathrm{LI}_{\mathrm{\_czx6oh}} \rightleftharpoons \mathrm{Cli}_{\mathrm{plasma\_czx6oh}}$ |  |
| $v_{\mathrm{LI\_\_CZXOGLU\_EX}}$ | `LI__CZXOGLU_EX` | 6-hydroxychlorzoxazone-O-glucuronide export | $\mathrm{LI}_{\mathrm{\_czxoglu}} \rightleftharpoons \mathrm{Cli}_{\mathrm{plasma\_czxoglu}}$ |  |
| $v_{\mathrm{LI\_\_CZXOX}}$ | `LI__CZXOX` | chlorzoxazone 6-hydroxylation (CYP2E1) | $\mathrm{LI}_{\mathrm{\_czx}} \longrightarrow \mathrm{LI}_{\mathrm{\_czx6oh}}$ | $\mathrm{LI}_{\mathrm{\_cyp2e1}}$ |
| $v_{\mathrm{LI\_\_CZXOTHER}}$ | `LI__CZXOTHER` | chlorzoxazone elimination (CYP2E1 independent) | $\mathrm{LI}_{\mathrm{\_czx}} \longrightarrow \varnothing$ |  |
| $v_{\mathrm{LI\_\_CZXOGLU}}$ | `LI__CZXOGLU` | 6-hydroxychlorzoxazone glucuronidation (UGT) | $\mathrm{LI}_{\mathrm{\_czx6oh}} \longrightarrow \mathrm{LI}_{\mathrm{\_czxoglu}}$ |  |
| $v_{\mathrm{LI\_\_ETHIM}}$ | `LI__ETHIM` | ethanol import | $\mathrm{Cli}_{\mathrm{plasma\_ethanol}} \rightleftharpoons \mathrm{LI}_{\mathrm{\_ethanol}}$ |  |
| $v_{\mathrm{LI\_\_ETH\_ELIMINATION}}$ | `LI__ETH_ELIMINATION` | ethanol elimination (ALD) | $\mathrm{LI}_{\mathrm{\_ethanol}} \longrightarrow \varnothing$ |  |
| $v_{\mathrm{LI\_\_CYP2E1\_PROD}}$ | `LI__CYP2E1_PROD` | CYP2E1 production | $\varnothing \longrightarrow \mathrm{LI}_{\mathrm{\_cyp2e1}}$ |  |
| $v_{\mathrm{LI\_\_CYP2E1\_DEG}}$ | `LI__CYP2E1_DEG` | CYP2E1 degradation | $\mathrm{LI}_{\mathrm{\_cyp2e1}} \longrightarrow \varnothing$ | $\mathrm{LI}_{\mathrm{\_ethanol}}$ |
| $v_{\mathrm{GU\_\_CZXABS}}$ | `GU__CZXABS` | absorption chlorzoxazone | $\mathrm{Cgulumen}_{\mathrm{czx}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_czx}}$ |  |
| $v_{\mathrm{GU\_\_ETHABS}}$ | `GU__ETHABS` | absorption ethanol | $\varnothing \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_ethanol}}$ |  |
| $v_{\mathrm{GU\_\_CZXEXC}}$ | `GU__CZXEXC` | excretion chlorzoxazone (feces) | $\mathrm{Cgulumen}_{\mathrm{czx}} \longrightarrow \mathrm{Afeces}_{\mathrm{czx}}$ |  |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{transport\_lu\_czx}} &= \frac{\mathrm{ftissue}_{\mathrm{czx}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\frac{\mathrm{Clu}_{\mathrm{plasma\_czx}} \cdot \mathrm{Kp}_{\mathrm{czx}}}{\mathrm{BP}_{\mathrm{czx}}} - \mathrm{Clu}_{\mathrm{czx}}\right) \\[1ex]
v_{\mathrm{transport\_re\_czx}} &= \frac{\mathrm{ftissue}_{\mathrm{czx}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\frac{\mathrm{Cre}_{\mathrm{plasma\_czx}} \cdot \mathrm{Kp}_{\mathrm{czx}}}{\mathrm{BP}_{\mathrm{czx}}} - \mathrm{Cre}_{\mathrm{czx}}\right) \\[1ex]
v_{\mathrm{iv\_czx}} &= \frac{\mathrm{Ki}_{\mathrm{czx}} \cdot \mathrm{IVDOSE}_{\mathrm{czx}}}{\mathrm{Mr}_{\mathrm{czx}}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_czx}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_czx}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_czx}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_czx}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_czx}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_czx}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_czx}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_czx}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_czx}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_czx}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_czx}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_czx}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_czx}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_czx}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_czx}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_czx}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_czx}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{czx}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_czx}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_czx}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_czx6oh}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_czx6oh}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_czx6oh}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_czx6oh}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_czx6oh}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_czx6oh}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_czx6oh}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_czx6oh}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_czx6oh}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_czx6oh}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_czx6oh}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_czx6oh}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_czx6oh}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_czx6oh}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_czx6oh}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_czx6oh}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_czx6oh}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{czx6oh}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_czx6oh}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_czx6oh}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_czxoglu}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_czxoglu}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_czxoglu}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_czxoglu}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_czxoglu}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_czxoglu}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_czxoglu}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_czxoglu}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_czxoglu}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_czxoglu}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_czxoglu}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_czxoglu}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_czxoglu}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_czxoglu}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_czxoglu}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_czxoglu}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_czxoglu}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{czxoglu}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_czxoglu}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_czxoglu}} \\[1ex]
v_{\mathrm{transport\_lu\_ethanol}} &= \frac{\mathrm{ftissue}_{\mathrm{ethanol}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Kp}_{\mathrm{ethanol}} - \mathrm{Clu}_{\mathrm{ethanol}}\right) \\[1ex]
v_{\mathrm{transport\_re\_ethanol}} &= \frac{\mathrm{ftissue}_{\mathrm{ethanol}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_ethanol}} \cdot \mathrm{Kp}_{\mathrm{ethanol}} - \mathrm{Cre}_{\mathrm{ethanol}}\right) \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_ethanol}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_ethanol}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_ethanol}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_ethanol}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_ethanol}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_ethanol}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_ethanol}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_ethanol}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_ethanol}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_ethanol}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_ethanol}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_ethanol}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_ethanol}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_ethanol}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_ethanol}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_ethanol}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_ethanol}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{ethanol}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_ethanol}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_ethanol}} \\[1ex]
v_{\mathrm{dissolution\_czx}} &= \frac{\frac{\begin{cases} \mathrm{Ka}_{\mathrm{dis\_solution\_czx}} & \text{if } \mathrm{application}_{\mathrm{form}} = 1 \\ \mathrm{Ka}_{\mathrm{dis\_tablet\_czx}} & \text{otherwise} \end{cases}}{60} \cdot \mathrm{PODOSE}_{\mathrm{czx}}}{\mathrm{Mr}_{\mathrm{czx}}} \\[1ex]
v_{\mathrm{KI\_\_CZXOGLU\_EX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{KI}_{\mathrm{\_CZXOGLU\_EX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_czxoglu}} \\[1ex]
v_{\mathrm{LI\_\_CZXIM}} &= \mathrm{LI}_{\mathrm{\_CZX\_k\_IM}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_czx}} - \mathrm{LI}_{\mathrm{\_CZX\_F\_EX}} \cdot \mathrm{LI}_{\mathrm{\_czx}}\right) \\[1ex]
v_{\mathrm{LI\_\_CZX6OHEX}} &= \mathrm{LI}_{\mathrm{\_CZX6OH\_k\_EX}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{LI}_{\mathrm{\_czx6oh}} - \mathrm{LI}_{\mathrm{\_CZX6OH\_F\_IM}} \cdot \mathrm{Cli}_{\mathrm{plasma\_czx6oh}}\right) \\[1ex]
v_{\mathrm{LI\_\_CZXOGLU\_EX}} &= \mathrm{LI}_{\mathrm{\_CZXOGLU\_k\_EX}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{LI}_{\mathrm{\_czxoglu}} - \mathrm{LI}_{\mathrm{\_CZXOGLU\_F\_IM}} \cdot \mathrm{Cli}_{\mathrm{plasma\_czxoglu}}\right) \\[1ex]
v_{\mathrm{LI\_\_CZXOX}} &= \frac{\mathrm{LI}_{\mathrm{\_f\_cyp2e1}} \cdot \mathrm{LI}_{\mathrm{\_cyp2e1}} \cdot \mathrm{LI}_{\mathrm{\_CZXOX\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_czx}}}{\mathrm{LI}_{\mathrm{\_czx}} + \mathrm{LI}_{\mathrm{\_CZXOX\_Km}} \cdot \mathrm{LI}_{\mathrm{\_f\_cyp2e1\_Km}}} \\[1ex]
v_{\mathrm{LI\_\_CZXOTHER}} &= \mathrm{LI}_{\mathrm{\_f\_czxother}} \cdot \mathrm{LI}_{\mathrm{\_CZXOTHER\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_czx}} \\[1ex]
v_{\mathrm{LI\_\_CZXOGLU}} &= \mathrm{LI}_{\mathrm{\_f\_GLU}} \cdot \mathrm{LI}_{\mathrm{\_CZXOGLU\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_czx6oh}} \\[1ex]
v_{\mathrm{LI\_\_ETHIM}} &= \mathrm{LI}_{\mathrm{\_ETH\_k\_IM}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_ethanol}} - \mathrm{LI}_{\mathrm{\_ethanol}}\right) \\[1ex]
v_{\mathrm{LI\_\_ETH\_ELIMINATION}} &= \frac{\mathrm{LI}_{\mathrm{\_ETHEL\_VMAX}} \cdot \mathrm{BW} \cdot \mathrm{LI}_{\mathrm{\_ethanol}}}{\mathrm{LI}_{\mathrm{\_ethanol}} + \mathrm{LI}_{\mathrm{\_ETHEL\_KM}}} \\[1ex]
v_{\mathrm{LI\_\_CYP2E1\_PROD}} &= \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_k\_cyp2e1\_prod}} \\[1ex]
v_{\mathrm{LI\_\_CYP2E1\_DEG}} &= \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_kd\_cyp2e1}} \cdot \mathrm{LI}_{\mathrm{\_cyp2e1}} \\[1ex]
v_{\mathrm{GU\_\_CZXABS}} &= \mathrm{GU}_{\mathrm{\_F\_czx\_abs}} \cdot \mathrm{GU}_{\mathrm{\_absorption}} \\[1ex]
v_{\mathrm{GU\_\_ETHABS}} &= \frac{\frac{\mathrm{GU}_{\mathrm{\_Ka\_abs\_eth}}}{60} \cdot \mathrm{GU}_{\mathrm{\_PODOSE\_ethanol}}}{\mathrm{Mr}_{\mathrm{ethanol}}} \\[1ex]
v_{\mathrm{GU\_\_CZXEXC}} &= \mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_F\_czx\_abs}}\right) \cdot \mathrm{GU}_{\mathrm{\_absorption}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_czx}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_czx}} - v_{\mathrm{Flow\_ki\_ve\_czx}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_czx}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_czx}} + v_{\mathrm{Flow\_po\_li\_czx}} - v_{\mathrm{Flow\_li\_hv\_czx}} - v_{\mathrm{LI\_\_CZXIM}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_czx}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_czx}} + v_{\mathrm{Flow\_ve\_lu\_czx}} - v_{\mathrm{Flow\_lu\_ar\_czx}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_czx}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_czx}} - v_{\mathrm{Flow\_gu\_po\_czx}} + v_{\mathrm{GU\_\_CZXABS}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_czx}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_czx}} + v_{\mathrm{Flow\_ar\_re\_czx}} - v_{\mathrm{Flow\_re\_ve\_czx}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{czx}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_czx}} - v_{\mathrm{Flow\_arli\_li\_czx}} - v_{\mathrm{Flow\_arli\_hv\_czx}} + v_{\mathrm{Flow\_lu\_ar\_czx}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_czx}} - v_{\mathrm{Flow\_ar\_re\_czx}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{czx}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{iv\_czx}} + v_{\mathrm{Flow\_ki\_ve\_czx}} + v_{\mathrm{Flow\_hv\_ve\_czx}} - v_{\mathrm{Flow\_ve\_lu\_czx}} \\
&\quad {} + v_{\mathrm{Flow\_re\_ve\_czx}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{czx}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_czx}} - v_{\mathrm{Flow\_po\_hv\_czx}} + v_{\mathrm{Flow\_gu\_po\_czx}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{czx}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_czx}} + v_{\mathrm{Flow\_po\_hv\_czx}} + v_{\mathrm{Flow\_li\_hv\_czx}} - v_{\mathrm{Flow\_hv\_ve\_czx}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{czx}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_czx}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{czx}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_czx}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{czx}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_CZXEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_czx6oh}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_czx6oh}} - v_{\mathrm{Flow\_ki\_ve\_czx6oh}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_czx6oh}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_czx6oh}} + v_{\mathrm{Flow\_po\_li\_czx6oh}} - v_{\mathrm{Flow\_li\_hv\_czx6oh}} + v_{\mathrm{LI\_\_CZX6OHEX}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_czx6oh}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ve\_lu\_czx6oh}} - v_{\mathrm{Flow\_lu\_ar\_czx6oh}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_czx6oh}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_czx6oh}} - v_{\mathrm{Flow\_gu\_po\_czx6oh}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_czx6oh}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_re\_czx6oh}} - v_{\mathrm{Flow\_re\_ve\_czx6oh}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{czx6oh}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_czx6oh}} - v_{\mathrm{Flow\_arli\_li\_czx6oh}} - v_{\mathrm{Flow\_arli\_hv\_czx6oh}} + v_{\mathrm{Flow\_lu\_ar\_czx6oh}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_czx6oh}} - v_{\mathrm{Flow\_ar\_re\_czx6oh}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{czx6oh}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ki\_ve\_czx6oh}} + v_{\mathrm{Flow\_hv\_ve\_czx6oh}} - v_{\mathrm{Flow\_ve\_lu\_czx6oh}} + v_{\mathrm{Flow\_re\_ve\_czx6oh}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{czx6oh}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_czx6oh}} - v_{\mathrm{Flow\_po\_hv\_czx6oh}} + v_{\mathrm{Flow\_gu\_po\_czx6oh}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{czx6oh}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_czx6oh}} + v_{\mathrm{Flow\_po\_hv\_czx6oh}} + v_{\mathrm{Flow\_li\_hv\_czx6oh}} - v_{\mathrm{Flow\_hv\_ve\_czx6oh}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_czxoglu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_czxoglu}} - v_{\mathrm{Flow\_ki\_ve\_czxoglu}} - v_{\mathrm{KI\_\_CZXOGLU\_EX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_czxoglu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_czxoglu}} + v_{\mathrm{Flow\_po\_li\_czxoglu}} - v_{\mathrm{Flow\_li\_hv\_czxoglu}} + v_{\mathrm{LI\_\_CZXOGLU\_EX}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_czxoglu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ve\_lu\_czxoglu}} - v_{\mathrm{Flow\_lu\_ar\_czxoglu}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_czxoglu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_czxoglu}} - v_{\mathrm{Flow\_gu\_po\_czxoglu}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_czxoglu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_re\_czxoglu}} - v_{\mathrm{Flow\_re\_ve\_czxoglu}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{czxoglu}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_czxoglu}} - v_{\mathrm{Flow\_arli\_li\_czxoglu}} - v_{\mathrm{Flow\_arli\_hv\_czxoglu}} + v_{\mathrm{Flow\_lu\_ar\_czxoglu}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_czxoglu}} - v_{\mathrm{Flow\_ar\_re\_czxoglu}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{czxoglu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ki\_ve\_czxoglu}} + v_{\mathrm{Flow\_hv\_ve\_czxoglu}} - v_{\mathrm{Flow\_ve\_lu\_czxoglu}} + v_{\mathrm{Flow\_re\_ve\_czxoglu}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{czxoglu}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_czxoglu}} - v_{\mathrm{Flow\_po\_hv\_czxoglu}} + v_{\mathrm{Flow\_gu\_po\_czxoglu}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{czxoglu}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_czxoglu}} + v_{\mathrm{Flow\_po\_hv\_czxoglu}} + v_{\mathrm{Flow\_li\_hv\_czxoglu}} - v_{\mathrm{Flow\_hv\_ve\_czxoglu}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{czxoglu}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_CZXOGLU\_EX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_ethanol}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_ethanol}} - v_{\mathrm{Flow\_ki\_ve\_ethanol}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_ethanol}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_ethanol}} + v_{\mathrm{Flow\_po\_li\_ethanol}} - v_{\mathrm{Flow\_li\_hv\_ethanol}} - v_{\mathrm{LI\_\_ETHIM}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_ethanol}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_ethanol}} + v_{\mathrm{Flow\_ve\_lu\_ethanol}} - v_{\mathrm{Flow\_lu\_ar\_ethanol}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_ethanol}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_ethanol}} - v_{\mathrm{Flow\_gu\_po\_ethanol}} + v_{\mathrm{GU\_\_ETHABS}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_ethanol}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_ethanol}} + v_{\mathrm{Flow\_ar\_re\_ethanol}} - v_{\mathrm{Flow\_re\_ve\_ethanol}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{ethanol}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_ethanol}} - v_{\mathrm{Flow\_arli\_li\_ethanol}} - v_{\mathrm{Flow\_arli\_hv\_ethanol}} + v_{\mathrm{Flow\_lu\_ar\_ethanol}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_ethanol}} - v_{\mathrm{Flow\_ar\_re\_ethanol}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{ethanol}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ki\_ve\_ethanol}} + v_{\mathrm{Flow\_hv\_ve\_ethanol}} - v_{\mathrm{Flow\_ve\_lu\_ethanol}} + v_{\mathrm{Flow\_re\_ve\_ethanol}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{ethanol}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_ethanol}} - v_{\mathrm{Flow\_po\_hv\_ethanol}} + v_{\mathrm{Flow\_gu\_po\_ethanol}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{ethanol}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_ethanol}} + v_{\mathrm{Flow\_po\_hv\_ethanol}} + v_{\mathrm{Flow\_li\_hv\_ethanol}} - v_{\mathrm{Flow\_hv\_ve\_ethanol}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{ethanol}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_ethanol}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{ethanol}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_ethanol}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgulumen}_{\mathrm{czx}}}{\mathrm{d} t} &= \frac{v_{\mathrm{dissolution\_czx}} - v_{\mathrm{GU\_\_CZXABS}} - v_{\mathrm{GU\_\_CZXEXC}}}{\mathrm{Vgulumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_czx}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_CZXIM}} - v_{\mathrm{LI\_\_CZXOX}} - v_{\mathrm{LI\_\_CZXOTHER}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_czx6oh}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{LI\_\_CZX6OHEX}} + v_{\mathrm{LI\_\_CZXOX}} - v_{\mathrm{LI\_\_CZXOGLU}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_czxoglu}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{LI\_\_CZXOGLU\_EX}} + v_{\mathrm{LI\_\_CZXOGLU}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ethanol}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_ETHIM}} - v_{\mathrm{LI\_\_ETH\_ELIMINATION}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_cyp2e1}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_CYP2E1\_PROD}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_CYP2E1\_DEG}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{czx}}}{\mathrm{d} t} &= -v_{\mathrm{iv\_czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} + \mathrm{Ri}_{\mathrm{czx}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cum}_{\mathrm{dose\_czx}}}{\mathrm{d} t} &= \mathrm{Ri}_{\mathrm{czx}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{czx}}}{\mathrm{d} t} &= -v_{\mathrm{dissolution\_czx}} \cdot \mathrm{Mr}_{\mathrm{czx}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_PODOSE\_ethanol}}}{\mathrm{d} t} &= -v_{\mathrm{GU\_\_ETHABS}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \qquad \text{(rate rule)}
\end{aligned}
$$
