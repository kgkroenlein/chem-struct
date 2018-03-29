# Chem-Struct

### A Web Application for relating chemical properties to underlying structure

### Table of Contents
0. [Table of Contents](#table-of-contents)
1. [Background](#background)
2. [Data](#data)
2. [Approach](#approach)
3. [Examples](#examples)
    1. [Example 1](#example-1)
    2. [Example 2](#example-2)
    3. [Example 3](#example-3)
4. [Future Work](#future-work)
5. [References](#references)

## Background
The goal of this project is to explore choices of feature sets and similarity metrics in the field of cheminformatics for building to-purpose hierarchical clustering classifiers. A broad range of challenges facing US society, including forensic analysis fighting the designer drug epidemic, design of efficient chemical manufacturing processes, and drug design in the pharmacological industry, and a direct need to obtain information about the properties and activities of compounds that have never been measured and could plausibly never existed in macroscopic quantities1.

## Data
A molecular fingerprint is simply a bit vector generated from a large feature set of a two-dimensional chemical structure (a graph with a small amount of 3-dimensional orientation disambiguation). Using molecular fingerprints as the bases for clustering, we can evaluate whether the concepts of chemical relationship as perceived by chemists align with the clustering reported by the algorithm. Further, from a practical perspective, this should allow for rapid determination of whether particular predictive models are likely or unlikely to yield reasonable results for a given molecule.

Regarding data, I presently have access to an archive of around 30 thousand 2-d chemical structures along with well-curated identifiers. Many of those records also have families of optimized 3-d molecular structures (“conformers”), which may be valuable for physical insight but should not be used in the final modeling efforts. Several million additional two-dimensional structures are available from PubChem if the original data proves inadequate and for vetting coverage over chemical similarity hyperspaces.

## Approach
In addition to the structural information, it is necessary to utilize software libraries to obtain chemical descriptors2.  Beginning with the standard extended molecular fingerprints, candidate subsets and alternative formulations will to evaluated for statistically significant impacts on classification capability.

Finally, it is necessary to identify score functions for how well any given tree conforms to real world applications. In a general sense, different properties depend on different emergent interactions and therefore are likely to depend on different structural elements.  While initial work will follow from ChEMBL data, testing the framework against multiple expressions of chemical functionality will be essential for the utility of the developed models. Fitting a particular system is subordinate to the capability to intelligently discuss appropriateness of a particular formulation of a fingerprint to a particular application.

Due to the size of the necessary hyperparameter grid search, AWS will be necessary in order to explore the space in a time-efficient, highly parallelized manner. scipy.stats and Scikit Learn will provide the statistical analysis and learning packages (e.g., a/b testing, tree construction).

kNN combined with Funk SVD, perhaps?

## Examples
### Example 1
### Example 2
### Example 3

## Future Work
* Building out additional predictions
* Testing and including additional similarity metrics
* Using the outputs from standard chemical analytical equipment as the input data, including a structure prediction step

### References
1. <a name="OBoyle-and-Sayle-2016"></a> O’Boyle, NM and Sayle, RA. Comparing structural fingerprints using a literature-based similarity benchmark J. Cheminform 2016 8: 36. doi://10.1186/s13321-016-0148-0.

2. <a name="Riniker-and-Landrum-2013"></a> Riniker S, Landrum GA (2013) Open-source platform to benchmark  fingerprints for ligand-based virtual screening. J. Cheminform 5:26. doi://10.1186/1758-2946-5-26

3. <a name="Ragab-2018"></a>[AWS Machine Learning Blog: Build an online compound solubility prediction workflow with AWS Batch and Amazon SageMaker](https://aws.amazon.com/blogs/machine-learning/build-an-online-compound-solubility-prediction-workflow-with-aws-batch-and-amazon-sagemaker/)

4. <a name="moleculenet"></a>http://moleculenet.ai/

5. <a name="Zhenqin-et-al-2017"></a>Zhenqin Wu, Bharath Ramsundar, Evan N. Feinberg, Joseph Gomes, Caleb Geniesse, Aneesh S. Pappu, Karl Leswing, Vijay Pande, MoleculeNet: A Benchmark for Molecular Machine Learning, arXiv preprint, [arXiv: 1703.00564, 2017](https://arxiv.org/abs/1703.00564).
