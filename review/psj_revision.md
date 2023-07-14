
Reviewer Report
Reviewer #1:
This study proposes a procedure to test the existence of a runaway greenhouse state, predicted by models, and supposed to mark the inner edge of the habitable zone. Relying on a model predicting the transit radius of exoplanets in the runaway greenhouse state coupled to a model generating a synthetic exoplanets catalog matching known statistics, the authors use a Bayesian hypothesis testing framework to assess the conclusive power of upcoming observation missions as to the existence of the runaway greenhouse state.

The manuscript is very well written, making a clear point and providing valuable tool for testing model predictions. I have two main points of concern:

1) I am skeptical regarding the claim that "Assuming a distribution of water mass fractions instead of a fixed value would thus not significantly change our results." (L. 1360-1362). While I understand that considering a single x_H2O value simplifies the model, assuming that all planets have the same water content is most certainly wrong. One can obviously debate what a realistic water mass fraction would be, and constraining it is beyond the scope of this study, but I think that an important robustness test would be to test at least a (log-)uniform distribution and see how the results change. This might, in turn, call for further discussion. In particular, I am not convinced that planet having a small water mass fraction can simply be absorbed in the dilution factor, because I expect a continuous distribution of x_H2O to have a more complex effect.

2) the dilution factor is a convenient parameter where a lot of (most?) processes hide, but its meaning is largely glossed over. I think that the manuscript deserves a dedicated section discussing what the main processes affecting the dilution are, i.e. what leads a highly irradiated planet to escape the runaway greenhouse state. No need to be quantitative, but I think it is important to convey a physical sense of what the dilution factor stands for.

Minor comments:

L. 83-87: This sentence is not very clear and quite misleading as it seems to suggest the existence of Venusian meteoritic samples. Besides I don't see how petrological evidence from meteorites can suggest anything about Venus, this would need some more explanation.
> Indeed, in its previous formulation this sentence may suggest that there are meteoritic samples from Venus and can be misleading. We rephrased the sentence to clarify what meteoritic evidence is meant here.
 
L. 274-275: Do you have a reference for the typical values of uncertainties?
> We rearranged this part of the text to make clear that these uncertainties were derived in Hardegree-Ullman et al. 2023.

L. 424: bottem <- bottom
> fixed.

L. 1242-1243: what do you mean by the runaway greenhouse phase of the star? The pre-main sequence phase?
> This sentence was indeed misleading. We mean the extended runaway greenhouse phases of planets orbiting M dwarfs. => We rephrased the sentence to make this clear.

Reviewer #2:
1) Line 376 "its bulk water inventory expressed as a water mass fraction xH2O"
It may be helpful to specify that the water mass fraction stated here and given in Table 1 is the fraction of water relative to the planet mass, and not an atmospheric water mixing ratio.

2) Line 381, "For runaway planets, all planets receiving a dayside-averaged instellation exceeding a threshold of Sthresh = 280 W m−2"
I think S_thresh needs to be more clearly defined in the paper. The ~280 Wm-2 threshold matches (approximately) the value given by Goldblatt et al 2013, and is the amount of stellar flux absorbed by the planet. It is not strictly the amount "received" by the planet. For instance, the Earth receives ~340 Wm-2 which is already beyond the limit as stated. But I think you mean that 1360./4 * (1-A) > 280 Wm-2, where A is the albedo and is fixed at A=0.3. Doing the math, this would put your runaway greenhouse limit for Earth with a fixed 0.3 albedo at ~1.18 S0, which itself is very reasonable compared to existing studies with climate models on when the runaway greenhouse condition is triggered (e.g. Leconte et al. 2013; Wolf & Toon 2015). I think this is all fine, but should be explained a bit better.
> We agree that our introduction of the threshold instellation does not in a sufficiently clear way convey the nature of this quantity, and we thank the reviewer for pointing out this potential source of confusion. 
> We now state explicitly that this is the flux *absorbed* by the planet. 

3) Is the transit depth appears to be tabulated as a broadband quantity of the whole planet's eclipsing of the star, and not a spectrally resolved quantity, which may are may not be problematic. A comment on this may be warranted.

4) Following from point 3, it would seem that clouds in particular would pose a serious uncertainty and challenge for the proposed detection method, not just in cloud's ability to modulate the albedo and thus S_thresh, but in the ability of clouds to obscure transit spectra. For instance, papers like Suissa et al. 2020, Fauchez et al. 2019, and others show that the prevalence of clouds can reduce the transit depth of water vapor features. In the limit of a runaway greenhouse climate, water cloud forming regions would track with atmospheric temperature, still, forming between let's say ~240 and 280 K. Thus runaway greenhouse climates may feature exceedingly high-altitude clouds which could potential mute an transit signal as measured from peak to trough of the spectral line observed. Some of this is hinted at in Suissa et al. 2020 figure 3, which hints that water vapor spectral features may become severely muted in the psuedo runaway atmosphere shown. So understand the role of clouds in this problem may be critical for its real world application.
> Clouds during runaway greenhouse phases should indeed have a non-negligible impact on transit spectra, and also impact the planetary Bond albedo and thus the threshold instellation. While the former effect is less relevant for the method explored here -  which only requires the measurement of bulk properties such as the planet radius as measured via the (wavelength-independent) transit depth - we should mention the potential impact that clouds will have when we discuss the potential of atmospheric spectral signatures in Section 6.2.3.
> We have added a discussion of the role of high-altitude clouds, and how they may obscure features in the observed spectra of individual planets. 

5) section 5.4.2 does not explain what was changed in the model to account for differing runaway greenhouse triggering conditions between F, G, K, and M dwarf stars. This is also relevant to point 2 above in clarifying the S_thresh. Perhaps S_thresh, the absorbed stellar flux by the planet can be kept the same for all stars, but the albedo would be considered to be reduced for lower temperature stars. More explanation required.

6) line 702 "A key constraint resulting from a detection is a measurement of S_thresh."
Yes and no. I would think that the measurement would give you the stellar insolation received by the planet, but would not give the stellar energy absorbed by the planet unless the albedo was also known. The difference between these two definitions is small, but important and should be clarified.

7) Planetary evolution and duration of the steam atmosphere phase:
I think that this is a major uncertainty in the results. The lifetime to lose a planets water is very short compared to the age of stellar systems. Thus, there should be a significant age-dependence in the viability of these observations. Very young systems perhaps would make for the best targets since the planetary water will have had less time to be irreversibly lost. For older systems, such a detection technique might be impossible because all the water has already been lost a long time ago, and no discontinuity would be observed. I think more discussion of how approach this problem should be considered.

8) 6.2.3. Atmospheric spectral signatures
I think that this paper would be relevant to cite here https://arxiv.org/abs/1303.7079
