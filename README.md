# Machine-Learning-Integrated-Multi-Objective-Simulation-based-Optimization

## Article 
Machine learning integrated multi-objective simulation-based optimization for a personnel planning, asset management and fleet renewal problem

## Description
The complexity of personnel planning, asset management, and fleet renewal interconnections can result in multi-objective
problems. To address these problems, a novel hybrid solution, QLFPEM-MOSO, is proposed. QLFPEM-MOSO integrates two machine learning (ML) models – Q-learning (a kind of reinforcement learning algorithm) and a frequent pattern extraction method (FPEM) – into a multi-objective simulation-based optimization method (MOSO). The core innovation lies in enhancing the performance of the optimization algorithm in MOSO—NSGA-III joined with a system dynamics (SD) simulation. Q-learning adaptively chooses the most effective crossover operator for NSGA-III. FPEM injects patterns from high-quality solutions into the search process of NSGA-III to direct it toward higher performance. This multiple-ML improvement of the multi-objective optimization algorithm substantially decreases personnel costs (PC), asset management costs (AMC), and fleet unavailability (FU) compared to MOSO and FPEM-MOSO. MOSO lacks ML models. FPEM-MOSO contains only one ML model as FPEM. As a result, QFPEM-MOSO is highly beneficial for organizations seeking considerable reductions in PC, AMC, and FU. 

This repository contains the source codes for the implementation of QLFPEM-MOSO, FPEM-MOSO and MOSO presented in the article.

## Experiments
The folders of QLFPEM_MOSO, FPEM_MOSO and MOSO contain the source codes of QLFPEM_MOSO, FPEM_MOSO and MOSO, respectively. 

## Code Developer
**Name:** Fatemeh Jalalvand

**Email:** fateme.jalalvand@gmail.com 

## Citation
If you use the codes or data in your work, please cite the following paper:

Jalalvand, F., Turan, H. H., & Elsawah, S. (2026). Machine learning integrated multi-objective simulation-based optimization for a personnel planning, asset management and fleet renewal problem. *Computers & Industrial Engineering*, 211, 111564. doi: https://doi.org/10.1016/j.cie.2025.111564

BibTeX format:

@article{JALALVAND2026machine,

title = {Machine learning integrated multi-objective simulation-based optimization for a personnel planning, asset management and fleet renewal problem},

journal = {Computers & Industrial Engineering},

volume = {211},

pages = {111564},

year = {2026},

doi = {https://doi.org/10.1016/j.cie.2025.111564},

author = {Fatemeh Jalalvand and Hasan Hüseyin Turan and Sondoss Elsawah}
}

