> We would like to thank both reviewers and the editor for the time they have taken to consider our work and for providing excellent comments that greatly improved our manuscript.
> We have addressed all comments raised by the referees, and we marked all changes in the revised manuscript. Below each comment, we state our responses starting with '>'. Where applicable, we point to changes in the text, which are all marked in boldface in the re-submitted manuscript.


1) I am skeptical regarding the claim that "Assuming a distribution of water mass fractions instead of a fixed value would thus not significantly change our results." (L. 1360-1362). While I understand that considering a single x_H2O value simplifies the model, assuming that all planets have the same water content is most certainly wrong. One can obviously debate what a realistic water mass fraction would be, and constraining it is beyond the scope of this study, but I think that an important robustness test would be to test at least a (log-)uniform distribution and see how the results change. This might, in turn, call for further discussion. In particular, I am not convinced that planet having a small water mass fraction can simply be absorbed in the dilution factor, because I expect a continuous distribution of x_H2O to have a more complex effect.
> We thank the referee for their suggestion and agree that the underlying water mass fraction of exoplanets is a critical parameter of the exoplanet census, which we believe our predictions will help to constrain. In fact, we chose our initial conditions such as to arrive at the most conservative outcome of the model under the premise that a runaway greenhouse phase exists at all within the exoplanet census.
> To clarify this point, we would first like to point to Figure 7 in the manuscript, which outlines the statistical power (the % of times in a random draw we would correctly reject the null-hypothesis = no runaway greenhouse states) of the model as a function of the water mass fraction. As can be seen, below a water mass fraction of 1e-4 the statistical power is typically less than ~50%. Above that, only very low dilution factors (few planets in a runaway) lead to such low statistical powers. There are three reasons for this: (i) the runaway greenhouse state is a qualitative transition: sub-runaway planets are small, while runaway planets are comparatively *much* larger. (ii) Solubility effects strongly diminish the effect of increasing water mass fraction in a runaway state relative to Turbet+19/20 (see Dorn & Lichtenberg 2021). (iii) We chose highly conservative assumptions that still produce a runaway, especially the bare-rock case, which is a no-iron core silicate model, which is much closer to a runaway planet than an Earth-like core+mantle structure.
> An exploration of an essentially guessed water mass distribution would thus produce a result that is sensitive to the fraction of planets below and above a water mass fraction of 1e-4. However, as planet formation simulations and recent results from a number of systems (Luqe & Pallé 2022; Lacedelli et al. 2022, Piaulet et al. 2022) highlight, large water mass fractions may be common. Thus, from a modeling philosophy point of view, detecting or not detecting the runaway transition is a way of testing the underlying water mass fraction. 
> We now elaborate on these relationships in the discussion of factors influencing tests of the runaway greenhouse hypothesis (Section 6.2.1).


2) the dilution factor is a convenient parameter where a lot of (most?) processes hide, but its meaning is largely glossed over. I think that the manuscript deserves a dedicated section discussing what the main processes affecting the dilution are, i.e. what leads a highly irradiated planet to escape the runaway greenhouse state. No need to be quantitative, but I think it is important to convey a physical sense of what the dilution factor stands for.
> We thank the referee for pointing out that the dilution factor is not well explained. We addressed this comment by expanding the introduction of the dilution factor in Section 3, as well as identifying and discussing processes by which planets may evade runaway greenhouse states and their respective expected impact in Section 6.2.1 "Key factors influencing tests of the runaway greenhouse hypothesis". These text there motivates the conservative use of a parameter with the full range of probabilities (0...1) to reflect the impact of a number of potentially existing, but yet poorly understood processes.


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
> We thank the referee for their suggestion and agree that it is crucial to provide a clear definition of the water mass fraction. 
> We now emphasize better that our parameter refers to the *total* planetary mass fraction of water (when the parameter is introduced and at other places xH2O is mentioned).

2) Line 381, "For runaway planets, all planets receiving a dayside-averaged instellation exceeding a threshold of Sthresh = 280 W m−2"
I think S_thresh needs to be more clearly defined in the paper. The ~280 Wm-2 threshold matches (approximately) the value given by Goldblatt et al 2013, and is the amount of stellar flux absorbed by the planet. It is not strictly the amount "received" by the planet. For instance, the Earth receives ~340 Wm-2 which is already beyond the limit as stated. But I think you mean that 1360./4 * (1-A) > 280 Wm-2, where A is the albedo and is fixed at A=0.3. Doing the math, this would put your runaway greenhouse limit for Earth with a fixed 0.3 albedo at ~1.18 S0, which itself is very reasonable compared to existing studies with climate models on when the runaway greenhouse condition is triggered (e.g. Leconte et al. 2013; Wolf & Toon 2015). I think this is all fine, but should be explained a bit better.
> We agree that our introduction of the threshold instellation does not in a sufficiently clear way convey the nature of this quantity, and we thank the reviewer for pointing out this potential source of confusion. 
> We now state explicitly that this is the flux *absorbed* by the planet. 

3) Is the transit depth appears to be tabulated as a broadband quantity of the whole planet's eclipsing of the star, and not a spectrally resolved quantity, which may are may not be problematic. A comment on this may be warranted.
> Indeed, our work focuses on inferences based on the total transit radii of planets, as obtained from wavelength-independent photometric measurements. 
> We discuss additional information that may be obtained from wavelength-resolving observations in Section 6.2.3. 

4) Following from point 3, it would seem that clouds in particular would pose a serious uncertainty and challenge for the proposed detection method, not just in cloud's ability to modulate the albedo and thus S_thresh, but in the ability of clouds to obscure transit spectra. For instance, papers like Suissa et al. 2020, Fauchez et al. 2019, and others show that the prevalence of clouds can reduce the transit depth of water vapor features. In the limit of a runaway greenhouse climate, water cloud forming regions would track with atmospheric temperature, still, forming between let's say ~240 and 280 K. Thus runaway greenhouse climates may feature exceedingly high-altitude clouds which could potential mute an transit signal as measured from peak to trough of the spectral line observed. Some of this is hinted at in Suissa et al. 2020 figure 3, which hints that water vapor spectral features may become severely muted in the psuedo runaway atmosphere shown. So understand the role of clouds in this problem may be critical for its real world application.
> Clouds during runaway greenhouse phases should indeed have a non-negligible impact on transit spectra, and also impact the planetary Bond albedo and thus the threshold instellation. While the former effect is less relevant for the method explored here -  which only requires the measurement of bulk properties such as the planet radius as measured via the (wavelength-independent) transit depth - we should mention the potential impact that clouds will have when we discuss the potential of atmospheric spectral signatures in Section 6.2.3.
> We have added a discussion of the role of high-altitude clouds, and how they may obscure features in the observed spectra of individual planets. 

5) section 5.4.2 does not explain what was changed in the model to account for differing runaway greenhouse triggering conditions between F, G, K, and M dwarf stars. This is also relevant to point 2 above in clarifying the S_thresh. Perhaps S_thresh, the absorbed stellar flux by the planet can be kept the same for all stars, but the albedo would be considered to be reduced for lower temperature stars. More explanation required.
> This is a good point. In order to avoid introducing complexity to the model that may not be reflected in the expected quality and detail of future observed data, we decided to set the planetary albedo to a fixed value of 0.3.
> We have added explanations to make clear that we are considering this fixed value and that there is no spectral type dependency.

6) line 702 "A key constraint resulting from a detection is a measurement of S_thresh."
Yes and no. I would think that the measurement would give you the stellar insolation received by the planet, but would not give the stellar energy absorbed by the planet unless the albedo was also known. The difference between these two definitions is small, but important and should be clarified.
> We thank the reviewer for this important comment. We agree that it is important to distinguish between the radiation flux at the planet's orbit and the actually absorbed stellar energy. 
> We have added a sentence to remind the reader that the actual threshold instellation may be shifted because of this.

7) Planetary evolution and duration of the steam atmosphere phase:
I think that this is a major uncertainty in the results. The lifetime to lose a planets water is very short compared to the age of stellar systems. Thus, there should be a significant age-dependence in the viability of these observations. Very young systems perhaps would make for the best targets since the planetary water will have had less time to be irreversibly lost. For older systems, such a detection technique might be impossible because all the water has already been lost a long time ago, and no discontinuity would be observed. I think more discussion of how approach this problem should be considered.
> The finite duration of steam atmosphere phases is indeed a main expected cause for dilution of the discontinuity, and it is one of the processes caught by the dilution factor we introduced in our model. While it has been suggested that runaway greenhouse climates can last hundreds of Myr or even > 1 Gyr under certain conditions (Hamano+2015, Luger & Barnes 2015), it is true that we can expect that a large fraction of highly irradiated planets will already have ended this phase. This should indeed lead to a preference of young systems, which should be mentioned in our paper.
> We added a discussion on the increased likelihood of detecting the demographic trend in younger planetary systems.

8) 6.2.3. Atmospheric spectral signatures
I think that this paper would be relevant to cite here https://arxiv.org/abs/1303.7079
> We now cite this clearly relevant paper in Section 6.2.3. Atmospheric spectral signatures and added a sentence on potentially distinguishing different climate regimes, for example the bistable moist state identified in the paper, through additional spectrally resolved observations. 
