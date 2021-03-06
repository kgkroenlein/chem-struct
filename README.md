# Chem-Struct

### [A Web Application for relating chemical properties to underlying structure](http://www.chem-struct.info/)

### Table of Contents
0. [Table of Contents](#table-of-contents)
1. [Background](#background)
2. [Data](#data)
2. [Approach](#approach)
2. [Installation](#installation)
4. [Future Work](#future-work)
5. [References](#references)

## Background
The goal of this project is to explore choices of feature sets and similarity metrics in the field of cheminformatics for building to-purpose hierarchical clustering classifiers and regressors. A broad range of challenges facing US society, including forensic analysis fighting the designer drug epidemic, design of efficient chemical manufacturing processes, and drug design in the pharmacological industry, and a direct need to obtain information about the properties and activities of compounds that have never been measured and could plausibly never existed in macroscopic quantities<sup>[1][#OBoyle-and-Sayle-2016]</sup>.

## Data
A molecular fingerprint is simply a bit vector generated from a large feature set of a two-dimensional chemical structure (a graph with a small amount of 3-dimensional orientation disambiguation). Examples of features might include 'has 5 carbons in a row' or 'has a chlorine two atoms away from a carbon.'  Using molecular fingerprints as the bases for clustering, we can evaluate whether the concepts of chemical relationship as perceived by chemists align with the clustering reported by the algorithm. Further, from a practical perspective, this should allow for rapid determination of whether particular predictive models are likely or unlikely to yield reasonable results for a given molecule.

Obtaining chemical structures is straight-forward; for example, [emolecules](https://www.emolecules.com/) makes 17 million (probably) chemically stable structures freely available.  However, with nothing more than a graph representation of the molecule, these become useful only for large searches against a given model.  Indeed, emolecules business model is selling the metadata associated with those compounds on a compound-by-compound basis.

The bigger challenge is finding reliable labels -- in this case, physical property data.  In general, any given property will only have on order one thousand data points; far fewer than we would want to apply many machine learning techniques. While physical models exist for computing many of these properties, the uncertainty on the computations tends to be an order of magnitude larger than on an experiment, and may require months on very expensive hardware to evaluate a single point.  Combining this with the knowledge that experimental approaches are costly and time-consuming, even a structure-driven model of limited reliability has substantial value.

## Approach
In addition to the structural information, it is necessary to utilize software libraries to obtain chemical descriptors2.  Beginning with the standard extended molecular fingerprints, candidate subsets and alternative formulations will to evaluated for statistically significant impacts on classification capability.

Finally, it is necessary to identify score functions for how well any given tree conforms to real world applications. In a general sense, different properties depend on different emergent interactions and therefore are likely to depend on different structural elements.  While initial work will follow from ChEMBL data, testing the framework against multiple expressions of chemical functionality will be essential for the utility of the developed models. Fitting a particular system is subordinate to the capability to intelligently discuss appropriateness of a particular formulation of a fingerprint to a particular application.

Due to the size of the necessary hyperparameter grid search, AWS will be necessary in order to explore the space in a time-efficient, highly parallelized manner. scipy.stats and Scikit Learn will provide the statistical analysis and learning packages (e.g., a/b testing, tree construction).

## Installation
The archive should contain everything needed to recreate the tool.  If you are running a new fresh AWS instance (recommended 50 GB attached storage), you can run the following series of commands, presuming you edited your `.ssh/config` file appropriately:

```bash
ssh $YOUR_AWS_INSTANCE sudo yum install git -y
ssh $YOUR_AWS_INSTANCE git clone https://github.com/kgkroenlein/chem-struct.git
ssh $YOUR_AWS_INSTANCE bash chem-struct/aws_docker_init.sh
ssh $YOUR_AWS_INSTANCE bash chem-struct/fetch_s3.sh
ssh $YOUR_AWS_INSTANCE bash chem-struct/init.sh
```        

Those instructions should end up with a web application hosted on port 80 of
your AWS instance.  You may wish to ssh into the instance explicitly and run
`fetch_data.sh` and `init.sh` in a screen session, as it may take a while and
falling prey to a broken pipe would be unfortunate.  Note you must log out of
the instance after running `aws_docker_init.sh` because of user permissions
issues.


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

6. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2750043/

7. https://pubs.acs.org/doi/suppl/10.1021/ci034243x/suppl_file/ci034243xsi20040112_053635.txt

8. <a name="Delaney-2004"></a> Delaney, JS. ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure. J. Chem. Inf. Comput. Sci., 2004, 44 (3), pp 1000–1005, DOI: 10.1021/ci034243x

9. A.P. Bento, A. Gaulton, A. Hersey, L.J. Bellis, J. Chambers, M. Davies, F.A. KrÃ¼ger, Y. Light, L. Mak, S. McGlinchey, M. Nowotka, G. Papadatos, R. Santos & J.P. Overington (2014) 'The ChEMBL bioactivity database: an update' Nucl. Acids Res. Database Issue. 42 D1083-D1090 DOI:10.1093/nar/gkt1031 PMID:24214965

10. Landrum, G. http://www.rdkit.org/docs/Overview.html
