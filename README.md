# Machine-Learning-Integrated-Multi-Objective-Simulation-based-Optimization

## Article 
Machine learning integrated multi-objective simulation-based optimization for a personnel planning, asset management and fleet renewal problem

## Description
The complexity of personnel planning, asset management, and fleet renewal interconnections can result in multi-objective
problems. To address these problems, a novel hybrid solution, QLFPEM-MOSO, is proposed. QLFPEM-MOSO integrates two machine learning (ML) models – Q-learning and a frequent pattern extraction method (FPEM) – into a multi-objective simulation-based optimization method (MOSO). The core innovation lies in enhancing the performance of the optimization algorithm in MOSO—NSGA-III joined with a system dynamics (SD) simulation. Q-learning adaptively chooses the most effective crossover operator for NSGA-III. FPEM injects patterns from high-quality solutions into the search process of NSGA-III to direct it toward higher performance. This multiple-ML improvement of the multi-objective optimization algorithm substantially decreases personnel costs (PC), asset management costs (AMC), and fleet unavailability (FU) against MOSO and FPEM-MOSO. MOSO lacks ML models. FPEM-MOSO contains only one ML model as FPEM. As a result, QFPEM-MOSO is highly beneficial for organizations seeking reductions in PC, AMC, and FU. 

This repository contains the source codes for the implementation of QLFPEM-MOSO, FPEM-MOSO and MOSO presented in the article.

## Experiments
The folders of QLFPEM_MOSO, FPEM_MOSO and MOSO contain the source codes of QLFPEM_MOSO, FPEM_MOSO and MOSO, respectively. 

## Instructions to Run Experiments
- For QLFPEM_MOSO and FPEM_MOSO run the cells of the notebook files sequentially.
- For MOSO, run the 

## Code Developer
**Name:** Fatemeh Jalalvand

**Email:** fateme.jalalvand@gmail.com 

## Citation
If you use the codes or data in your work, please cite the following paper:

Jalalvand, F., Chhetri, M. B., Nepal, S., & Paris, C. (2025). Adaptive alert prioritisation in security operations centres via learning to defer with human feedback. arXiv preprint arXiv:2506.18462, .

BibTeX format:

@article{jalalvand2025adaptive,

title = {Adaptive alert prioritisation in security operations centres via learning to defer with human feedback},

author = {Jalalvand, Fatemeh and Chhetri, Mohan Baruwal and Nepal, Surya and Paris, C{\\'e}cile},

journal = {arXiv preprint arXiv:2506.18462},

year = {2025}

}

## Acknowledgments
This work was supported by CSIRO’s Collaborative Intelligence (CINTEL) Future Science Platform (FSP).

Also, this project was supported by resources provided by CSIRO IMT Scientific Computing.
