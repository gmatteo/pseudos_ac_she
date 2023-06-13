# Finalized

```
# Magnetization taken from Hirshfeld 
# null means that the calculation is still running

{
"92_U": -0.892,   FIXME
"93_Np": -2.695,  FIXME
"94_Pu": -5.785,  OK
"95_Am": -7.321,  OK
"96_Cm": -7.026,  OK
"97_Bk": -5.459,  FIXME
"98_Cf": -4.164,  OK
"99_Es": -2.906,  FIXME  NOW OK WITH Es_5f_origin and NOMAG Reference
"100_Fm": -1.643, FIXME  delta with NM reference is better than previous one but not perfect
"101_Md": -0.419  FIXME  delta with NM reference is better than previous one but not perfect
}
```

Non-magnetic elelements for which we still have strong disagreement between AE and NC PS:

113_Nh
117_Ts
118_Og


TODO: 

1) Check FCC lattice parameters and V0

DONE with abstol 1-e4 

    Inexact a/vol for z: 99: volume from file: 27.76 , volume from a 27.764687391143916 adiff 0.004687391143914255

2) Use nsppol 2 with spinat 6. Usually 8 for all SHEs

```
85_At: OK: Delta=0.5, Delta'=1.58
87_Fr: OK: Delta=0.13, Delta'=1.80
88_Ra: TODO: OK-REASONABLE: Ra_origin without f?
89_Ac: OK: Delta=0.77, Delta'=2.20. my version with projector for empty f makes a huge difference wrt origin.
90_Th: OK: Delta=0.6, Delta'=0.96.

# THESE PSEUDOS WON'T BE REPORTED IN THE PAPER 
    91_Pa: FIXME: AE EOS looks OK but best pseudo has 5.44 df.
           Tested with nsppol 2 and spinat (0 0 8). No significant change
           Now using new AE NOMAG as reference but results do not change.
           Running _new_new with 0.1 e in 5f. Small improvemente. Tried other configurations.

    92_U:  FIXME: AE EOS looks OK but best pseudo has 6.63 df.
           Now using AE NOMAG as reference but results do not change.
    93_Np: FIXME: AE EOS looks OK but best pseudo has 33.67 df
           Now using new AE NOMAG as reference but results do not change. PS EOS significantly overestimates V0.
           RUNNING: Np_5f_new with 1f electron promoted to 6d
    94_Pu: OK: Take my version. Much better.
# END: THESE PSEUDOS WON'T BE REPORTED IN THE PAPER 

95_Am: OK Delta=0.14, Delta'=0.48
       Much better if smaller core radii (FR is problematic to generate)
96_Cm: OK-REASONABLE: Delta=1.27, Delta'=3.61
       NB: very bad if FR wo SOC
97_Bk: OK: Delta=0.24, Delta'=0.43
       NB: excellent agreement with new AE results if NM configuration is used
98_Cf: OK: Delta=0.14, Delta'=0.48
       NB Had to use AE results with magnetic configuration
99_Es: OK: Delta=0.51, Delta'=2.20
       NB: using AE NOMAG as reference. 
100_Fm: FIXME-ACCEPT?: AE EOS now looks OK, pseudo is not optimal but df 3
101_Md: FIXME-ACCEPT AE EOS now looks OK, pseudos is decent with df ~ 1.9
102_No: OK: Delta=0.03, Delta'=0.14
103_Lr: OK: Delta=0.43, Delta'=1.03

=========
Begin_SHE
=========
104_Rf: OK: Delta=1.47, Delta'=1.98
        NB: AE points deviate from the fit
105_Db: OK: Delta=3.43, Delta'=2.8
106_Sg: OK: Delta=1.41, Delta'=0.98
107_Bh: OK: Delta=1.49, Delta'=0.75
108_Hs: OK: Delta=0.65, Delta'=0.31
109_Mt: OK: Delta=2.80, Delta'=1.44
110_Ds: OK: Delta=0.97, Delta'=0.65
111_Rg: OK: Delta=1.87, Delta'=2.16
        NB: AE points deviate from the fit

112_Cn: TODO: Slow ecut conv, df good but there are discrepancies wrt AE. Cn_new.in is the best so far.
113_Nh: TODO: AE EOS looks ok. Using new AE NOMAG as reference. Nh_origin.psp8 gives df 1.18

114_Fl: OK: Delta=0.43, Delta'=1.10
        NB: Take my version with f-projector (0.43 vs 1.25)
115_Mc: OK: Delta=1.56, Delta'=2.78
        NB: Take my version with f-projector (1.56 vs 3.08 origin)
        NB: AE points deviate from the fit
116_Lv: OK-REASONABLE: Delta=2.28, Delta'=3.75

=========================================
THESE PSEUDOS ARE EXCLUDED FROM THE PAPER
=========================================
    117_Ts: FIXME: AE EOS looks ok but pseudos do not get V0 right (underestimated by ~one point)
            tested with nsppol 2 and spinat (0 0 8). No significant change
            Now using AE NOMAG as reference but best df ~ 2.7
            RERUNNING WITH NEW DATA
    118_Og: FIXME: Can't manage to get decent pseudo for this!
            running with nsppol 2 and spinat (0 0 8). No significant change
            Now using AE NOMAG as reference, best df ~ 0.84 but PS EOS is completely off (small b0 here)
            RERUNNING WITH NEW DATA

119_Uue: FIXME: PROBLEMATIC
120_Ubn: OK: Delta=0.29, Delta'=2.29
```

# AE results

Weird results for AE EOS of 100_Fm  ------> REDONE AND UPDATED #CT

# pseudos_ac_she

5f 91-92 rifare 

118-119 rifare

no5f da 90 a 102 guardare attentamente

no 5f 103 fare 

# MG CHANGELOG

Ac: Add 1 projector for f to improve logder.

Th_5f.in: Decrease rc for d by 0.5
          NB: This pseudos uses a sligly excited configuration with fractional occupancies.

Pa_5f.in: Optimize qcut, now ecut ~58

U_5f.in: Optimize qcut, decrease core radii, now ecut ~58, previously it was ~68

Np_5f.in: Optimize qcut, decrease core radii, now ecut ~58, previously it was ~62

Pu_5f.in: decrease rc for d by 0.1, no change in qcut values. 
          Already very good and similar to Np_5f.in
 
Am_5f.in: decrease rc for d by 0.2, no change in qcut values. ecut ~70

Cm_5f.in: decrease rc for d by 0.2, minor adjustments in qcut values. ecut ~70

Bk_5f.in: decrease rc for d by 0.2. No change in qcut values. ecut ~72

CF_5f.in: decrease rc for d by 0.2. Important optimization of qcut values: from ~105 to ~72

Es_5f.in: decrease rc for d by 0.2. No change in qcut values. ecut ~75

Fm_5f.in: decrease rc for d by 0.2. Minor adjustment in qcut values. ecut ~73

Md_5f.in: decrease rc for d by 0.2. Minor adjustment in qcut values. ecut ~75

No_5f.in: decrease rc for d by 0.2. Minor adjustment in qcut values. ecut ~78

Lr_5f.in: decrease rc for p by 0.2, d by 0.05. Minor adjustment in qcut values. ecut ~95 due to rc 1.2 for 5f.
          BTW: twpo possible configurations: [Rn]5f147s27p1 or 5f146d17s2

Rf: decrease rc for p and d. Minor adjustment in qcut values. ecut ~95, previous one ~105
Fb: decrease rc for p and d. Minor adjustment in qcut values. ecut ~96, previous one ~105
Sg: decrease rc for p and d. Minor adjustment in qcut values. ecut ~98, previous one ~108
Bh: decrease rc for p and d. Minor adjustment in qcut values. ecut ~100, previous one ~108
Hs: decrease rc for p and d. Minor adjustment in qcut values. ecut ~102, previous one ~108
Mt: decrease rc for p and d. Minor adjustment in qcut values
Ds: decrease rc for p and d. Minor adjustment in qcut values, increase qc for f, ecut 120,  previous one ~140
Ds: decrease rc for p and d. Minor adjustment in qcut values, increase qc for f, ecut 120,  previous one ~140
Cn: decrease rc for p and d. Minor adjustment in qcut values, increase qc for f, ecut 120,  previous one ~160
Ng: Minor adjustment in qcut values, ecut 125,  previous one ~128

Fl: Add projector for f with ep = 0.05 to improve f-logder
Mg: Add projector for f with ep = 0.05 to improve f-logder
Lv: Add projector for f with ep = 0.05 to improve f-logder
Ts: Decrease rcs significantly. Add projector for f with ep = 0.05 to improve f-logder
Og: Decrease rcs significantly e.g from 1.6 to 1.4. Add projector for f with ep = 0.05 to improve f-logder


Fr: Add two prrojectos for f to improve logder.  Minor adjustment in qcut values. Ecut now ~35

At: Decrease core radii using my new Po-spd.in as starting point. Add extra projector for f-channel with ep 0.05


### FCC COMPUTATIONAL DETAILS####

Spin Orbit Coupling	no
Spin Polarization	collinear (Z)
Smearing Fermi-Dirac	0.001 Ha
K-points	15 x 15 x 15

### OXIDES COMPUTATIONAL DETAILS

------- WE DO NOT USE THESE RESULTS FOR THE PAPER  #CT
Spin Orbit Coupling no
Spin Polarization   collinear (Z)
Smearing Fermi-Dirac    0.05 Ha
K-points    5 x 5 x 5

### DATA FOR PAPERS

1) Delta-Gauge (meV) (FCC system)
2) Lattice percentage difference between AE and PW (FCC system)
3) Plot of hints
4) Delta-Gauge (meV) vs hints
5) Difference between V0 B0 and B0' obtained with AE and PW (FCC system)

