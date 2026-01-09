# REDatlas: Mapping the Global Distribution of Repeat Expansion Disorders

**REDatlas** is an interactive resource that visualizes the **geographic distribution** of **Repeat Expansion Disorders (REDs)** worldwide.

[**🌍 View the Interactive Map Here**](https://atlasred.streamlit.app)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Understanding the Map](#understanding-the-map)
- [Data Tables](#data-tables)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Data Sources](#data-sources)
- [Citation](#citation)
- [Authors & Contact](#authors--contact)
- [Acknowledgments](#acknowledgments)

---

## Overview

Repeat Expansion Disorders (REDs) are genetic conditions caused by abnormal expansions of tandem repeat sequences in the genome. REDatlas provides an intuitive platform to explore the global prevalence of REDs and findings from a comprehensive population-scale analysis of **known disease-associated tandem repeat loci** across **2,526 diverse haplotypes derived from long-read sequencing datasets**:

- **Geographic distribution** of REDs across global populations
- **Disorder-specific repeat length thresholds** from peer-reviewed literature
- **Sequence composition analysis** revealing interruptions and novel structures across known disease-associated loci
- **Population-specific allele architectures**
- **Clinical information** with integrated links to [GeneReviews](https://www.ncbi.nlm.nih.gov/books/NBK1116/) and [OMIM](https://www.omim.org/)
- **Ancestry-specific patterns** of repeat variation and disease risk
- **Inferred local ancestry** from RFMix

**Data Sources:** Long-read assemblies from 1000 Genomes Project ONT Consortium, Human Pangenome Reference Consortium (HPRC), Noyvert et al., and Human Genome Structural Variation Consortium.

---

## Features

✨ **Interactive Map Visualization**
- Color-coded markers showing the geographic distribution of specific disorders or repeat loci
- Clickable markers with detailed clinical and genetic information
- Dynamic filtering by disease name or repeat ID (RepID)

📊 **Comprehensive Data Tables**
- **Summary Table**: Curated data for each superpopulation including:
  - Locus and allele class information
  - Average non-canonical base composition across populations (AFR, AMR, EAS, EUR, SAS)
  - Population-specific frequencies
  - Most frequent motifs and their percentages
  - Most frequent repeat counts and ranges
  - Total allele counts per superpopulation
  
- **Population Table**: Detailed genotype, sequence composition, repeat structures, and local ancestry data for known disease-associated tandem repeat loci

🔍 **Flexible Search & Filtering**
- Search by disease name, RepID, or genomic locus
- Filter population data by allele class, superpopulation, and sample
- Multi-criteria filtering for precise data queries

🔗 **Integrated References**
- Direct links to authoritative clinical resources (GeneReviews, OMIM)
- Curated bibliographic references for repeat length thresholds

---

## Understanding the Map

### Map Interface Components

The REDatlas map provides an intuitive interface for exploring the global distribution of repeat expansion disorders:

#### **1. Geographic Markers**
- **Circle Markers**: Each circle represents a geographic location where a specific disorder or repeat expansion has been reported or studied
- **Marker Size**: Indicates the frequency or prevalence of the repeat expansion in that population (larger circles = higher frequency)
- **Marker Color**: Each disease or RepID is assigned a unique color for easy visual distinction

#### **2. Interactive Elements**
- **Click on any marker** to view detailed information:
  - Disease name and associated repeat ID (RepID)
  - Genomic location of the repeat (e.g., gene name, chromosome position)
  - Normal repeat range (unaffected individuals)
  - Intermediate range (gray zone/reduced penetrance)
  - Full mutation range (disease-causing)
  - Direct links to clinical references (GeneReviews, OMIM)

#### **3. Color Legend**
- Located on the left side of the map
- Shows the color-coding for each disease or RepID currently displayed
- Updates dynamically based on your search selections

#### **4. Continental Background**
- Different continents are shaded in distinct colors for geographic context:
  - Africa: Light Green
  - Asia: Light Red
  - Europe: Light Blue
  - North America: Light Purple
  - South America: Light Orange
  - Oceania: Light Pink
  - Antarctica: Light Gray

### How to Use the Map

**To explore specific disorders:**
1. Use the **"Select Disease(s)"** dropdown to choose one or more disorders
2. Alternatively, use the **"Select Repid(s)"** dropdown to explore specific genomic loci
3. Or simply type disease names or RepIDs in the **search box** (comma-separated for multiple terms)

**What the markers tell you:**
- **Geographic clustering** indicates regions where the disorder has been extensively studied or is more prevalent
- **Marker size** reflects the frequency data available for that location—larger markers indicate higher disease prevalence
- **Multiple REDs in one location** will show overlapping markers in different colors

**Interpreting repeat ranges:**
- **Normal Range**: The number of repeats typically found in unaffected individuals
- **Intermediate Range**: A gray zone where individuals may have some symptoms or increased risk; not all disorders have this range
- **Full Mutation Range**: The number of repeats that cause the full disease phenotype

## Data Tables

REDatlas includes two comprehensive data tables derived from the analysis presented in our medRxiv preprint, accessible via the interface:

### Summary Table (`summary_all.tsv`)

Contains curated summary statistics for **66 disease-associated tandem repeat loci** across five superpopulations, including:

**Key Columns:**
- `Locus`: Gene name or genomic locus
- `AlleleClass`: Classification (normal, intermediate, reduced-penetrance, full mutation)
- `Avg_Non_Canonical_Base_[POP]`: Average percentage of non-canonical bases per superpopulation (AFR, AMR, EAS, EUR, SAS)
- `Frequency_[POP]`: Allele frequency in each superpopulation
- `Most_Freq_Motif_[POP]`: Most common motif sequence per superpopulation
- `Most_Freq_Motif_%_[POP]`: Percentage of haplotypes with the most frequent motif in each superpopulation
- `Most_Freq_Repeat_[POP]`: Most common repeat count in each superpopulation
- `Most_Freq_Repeat_%_[POP]`: Percentage of haplotypes with the most frequent repeat count in each superpopulation
- `Repeat_Range_[POP]`: Range of repeat counts observed (min-max) in each superpopulation
- `Total_Allele_Count_[POP]`: Total number of alleles analyzed per superpopulation

**Superpopulations:**
- **AFR**: African
- **AMR**: American (admixed)
- **EAS**: East Asian
- **EUR**: European
- **SAS**: South Asian

### Population Table (`all_REDatlas.tsv`)

Provides detailed haplotype-level data from **2,526 diverse haplotypes** analyzed using long-read genome assemblies, including:

- **Genotype information**: Individual sample genotypes and phasing
- **Repeat length**: Exact repeat counts per allele
- **Motif composition**: Complete sequence composition including interruptions and non-canonical motifs
- **Allele classification**: Based on clinical thresholds (normal, intermediate, reduced-penetrance, full mutation)
- **Local ancestry**: Inferred ancestry at each locus using RFMix
- **Population stratification**: Detailed population and superpopulation labels
- **Sample metadata**: Individual identifiers and biological sex

**Data Sources:**
- 1000 Genomes Project (ONT long-read assemblies)
- Human Pangenome Reference Consortium (HPRC)
- Additional long-read datasets (Noyvery et al., HGSVC2)

**Filtering Options:**
- Search across multiple columns using comma-separated terms (e.g., ATXN1,ATXN2,ATXN3)
- Apply column-specific filters for precise queries (by allele class, locus, population, sample)
- Download filtered results as TSV files for further analysis
- Interactive exploration of complex genomic patterns

---

## Setup & Installation

### Prerequisites

REDatlas requires the following:

- **Python 3.7+**
- **pip** (Python package installer)

### Required Python Packages

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install streamlit pandas folium requests openpyxl
```

**Dependencies:**
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `folium` - Interactive map visualization
- `requests` - HTTP library for fetching geographic data
- `openpyxl` - Excel file reading
- `sqlite3` - Database (included with Python)

---

## Running the Application

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/wf-TRs/REDatlas.git
   cd REDatlas
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit app:**
   ```bash
   streamlit run final_map.py
   ```

4. **Access the application:**
   Open your browser and navigate to: `http://localhost:8501`

### Remote Compute Cluster Access

If running REDatlas on a remote compute cluster (e.g., HPC environment):

1. **Request compute resources and launch the app:**
   ```bash
   salloc --time=2:00:00 --mem=4G --cpus-per-task=2
   streamlit run final_map.py
   ```
   *Note: Adjust resource allocation based on your cluster's requirements*

2. **Set up SSH tunnel from your local machine:**
   ```bash
   ssh -L 8501:localhost:8501 <login-node> -t ssh -L 8501:localhost:8501 <compute-node>
   ```
   Replace `<login-node>` and `<compute-node>` with your cluster's specific node names.

3. **Access the application:**
   Open your browser and navigate to: `http://localhost:8501`

---

## Data Sources

### Primary Dataset

The population-level data presented in REDatlas is derived from our comprehensive analysis published as a preprint:

> Indhu-Shree Rajan-Babu, Readman Chiu, Ben Weisburd, Iris Caglayan, Inanc Birol, Jan M. Friedman. *Population-scale disease-associated tandem repeat analysis reveals locus and ancestry-specific insights.* medRxiv 2025.10.11.25337795 (2025). doi: https://doi.org/10.1101/2025.10.11.25337795

**Analysis Methodology:**
- **66 disease-associated tandem repeat loci** characterized from long-read genome assemblies
- **2,526 diverse haplotypes** from multiple long-read sequencing consortia:
  - 1000 Genomes Project ONT Consortium
  - Human Pangenome Reference Consortium (HPRC)
  - Noyvery et al. datasets
  - Human Genome Structural Variation Consortium 2 (HGSVC2)
- Integration of repeat length, motif composition, local ancestry (RFMix), linkage disequilibrium, and phylogenetic analyses
- Identification of locus-, population-, and allele-specific variation patterns
- Clinical significance assessment of expanded alleles with interrupting motifs

### Clinical & Genetic Information

Repeat length thresholds and clinical data have been curated from peer-reviewed literature, with primary reference to:

> Indhu Shree Rajan Babu, Egor Dolzhenko, Michael A. Eberle, Jan M. Friedman. *Sequence composition changes in short tandem repeats: heterogeneity, detection, mechanisms and clinical implications*. Nature Reviews Genetics, 2024.  
> [https://pubmed.ncbi.nlm.nih.gov/38467784/](https://pubmed.ncbi.nlm.nih.gov/38467784/)

### Additional Genomics Resources

- **gnomAD STR Database**: [gnomad.broadinstitute.org/short-tandem-repeats](https://gnomad.broadinstitute.org/short-tandem-repeats?dataset=gnomad_r3)
- **STRchive**: [strchive.org/loci/](https://strchive.org/loci/)
- **STRipy**: [stripy.org/database](https://stripy.org/database)
- **GeneReviews**: [ncbi.nlm.nih.gov/books/NBK535148/](https://www.ncbi.nlm.nih.gov/books/NBK535148/)
- **OMIM (Online Mendelian Inheritance in Man)**: [omim.org](https://www.omim.org/)

---

## Citation

If you use REDatlas in your research, please cite:

> Indhu-Shree Rajan-Babu, Readman Chiu, Ben Weisburd, Iris Caglayan, Inanc Birol, Jan M. Friedman. *Population-scale disease-associated tandem repeat analysis reveals locus and ancestry-specific insights.* medRxiv 2025.10.11.25337795 (2025). doi: https://doi.org/10.1101/2025.10.11.25337795

---

## Authors & Contact

### Development Team

- **[Iris Caglayan](https://github.com/iriscaglayan)** – Primary developer, software engineering, and data curation
- **Indhu Shree Rajan Babu** – Project lead, data curation, clinical annotation, and supervision

### Contact

For questions, collaborations, or feedback:

**Indhu Shree Rajan Babu**  
📧 [indhu.babu@bcchr.ca](mailto:indhu.babu@bcchr.ca)

### Contributing

We welcome contributions! If you'd like to:
- Report a bug or request a feature → Open an issue on GitHub
- Add new data or improve documentation → Submit a pull request
- Collaborate on research applications → Contact us directly

---

## Acknowledgments

We gratefully acknowledge the following resources and communities that made REDatlas possible:

### Geographic Data
- **Country boundary polygons**: Derived from [Natural Earth](https://www.naturalearthdata.com/)
- **GeoJSON package**: [datasets/geo-boundaries-world-110m](https://github.com/datasets/geo-boundaries-world-110m)
- **License**: [Open Data Commons Public Domain Dedication and License (PDDL)](https://opendatacommons.org/licenses/pddl/)

### Data & Research Communities
- The Genome Aggregation Database (gnomAD) consortium
- The 1000 Genomes Project
- The Human Pangenome Reference Consortium (HPRC)
- The STRchive and STRipy database maintainers
- GeneReviews and OMIM editorial teams

Special thanks to Natural Earth, Lexman, and the Open Knowledge Foundation for making high-quality geographic data openly available.
