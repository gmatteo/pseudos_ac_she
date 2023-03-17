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
85_At: OK: At-spd. May add At-d version
87_Fr: OK: Take Fr.psp8. Smoother convergence 
88_Ra: OK-Reasonable: Ra_origin ?

89_Ac: OK: my version with projector for empty f makes a huge difference wrt origin.
90_Th: OK: Take my version. Much better


# REMOVE ME
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
# REMOVE ME

95_Am: OK-Reasonable. Take Am_5f_origin?
96_Cm: OK: Take my version. Harder but more accurate.
97_Bk: FIXME AE EOS looks suspicious. 
       TODO: New AE results are needed.
98_Cf: OK: take Cf_5f.psp8, slightly better than Cf_origin_5f.psp8
       Now using new AE NOMAG as reference but MAG VERSION GAVE BETTER RESULTS
       RERUNNING WITH NEW DATA (NO IMPROVEMENT)
99_Es: ITWAS_FIXME: Now using AE NOMAG as reference. Kind of Ok with df 0.51
100_Fm: XXX FIXME: AE EOS now looks good but pseudos are not!
       RERUNNING WITH NEW DATA (NO IMPROVEMENT)
101_Md: FIXME: AE EOS is suspicious and should be recomputed. df 1.41
        ITWAS_FIXME: Now the AE EOS is slightly better (a bit smoother but jumps are still visible) df 0.66.  
        Need new AE results
102_No: OK: All pseudos are good, should find compromise btw accuracy and convergence ratio
103_Lr: OK: Take: my Lr_5f, smoother convergece

Begin_SHE
104_Rf: OK: Take Rf.psp8 (1.47 vs 2.58 from origin)
105_Db: OK: Take Db.psp8
106_Sg: OK: Take Sg_origin.psp8
107_Bh: OK: Take my version (1.50 vs 3.89 from origin)
108_Hs: OK: Take my Hs.psp8: (0.65 vs 2.82 from origin)  Perhaps, one can accelerate a bit the convergence.
109_Mt: OK: Take my Mt.psp8 (2.8 vs 4.99) and improve convergence rate.
110_Ds: OK: Take my version with smoother MCC and 0.93 vs 2.79 from origin
111_Rg: OK: Take my Rg. Much smoother
112_Cn: OK-TODO: Slow ecut conv, df good but there are discrepancies wrt AE. Cn_new.in is the best so far.
113_Nh: AE EOS looks ok but pseudos do not get V0 right (underestimated by ~one point)
        Tested with nsppol 2 and spinat (0 0 8). No significant change
        Now using AE NOMAG as reference but df ~ 1.2
114_Fl: OK: Take my Fl.psp8 with f-projector (0.42 vs 1.25)
115_Mc: OK: Take Mc_new.psp8 with f-projector (1.56 vs 3.08 origin)
116_Lv: OK: Take my version (2.27 vs 3.24 from origin)
117_Ts: FIXME: AE EOS looks ok but pseudos do not get V0 right (underestimated by ~one point)
        tested with nsppol 2 and spinat (0 0 8). No significant change
        Now using AE NOMAG as reference but best df ~ 2.7
        RERUNNING WITH NEW DATA
118_Og: FIXME: Can't manage to get decent pseudo for this!
        running with nsppol 2 and spinat (0 0 8). No significant change
        Now using AE NOMAG as reference, best df ~ 0.84 but PS EOS is completely off (small b0 here)
        RERUNNING WITH NEW DATA

119: TODO: Change pymatgen
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

