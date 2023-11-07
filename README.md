# longterm-coral-imaging
Repository for collecting, analyzing, and interpreting visual (and co-registered) data collected at coral reefs.

## Background and Motivation
During summer 2023, a massive coral bleaching event occurred in the Caribbean Sea. There is interest in understanding the scope/scale of the impact of bleaching events, rate of reef recovery, and assessing restoration interventions. Imaging, with co-registered *in situ* data, is well-suited for biomass estimation and health assessment. For single-shot imaging surveys, modern computer vision tools can recover 3D models of seafloors. Both associating temporal changes measured by *in situ* measurements to singular visual models and co-registering models across multiple surveys across which the reef morphology is expected to undergo subtle changes, are considerably challenging tasks for modern solutions.

This project collects a reef-recovery dataset from Cayo San Cristobal in Puerto Rico from December 2023 through July 2024. Cayo San Cristobal is a reef restoration site adopted by the University of Puerto Rico. While this work stops short of assessing the efficacy of different restoration efforts, this dataset can be used to quantify the efficacy of aggregate efforts and natural recovery over the study period. This data also serves to establish algorithmic prototypes for co-registering visual surveys with and without *in situ* auxiliary data. The products from the perception pipeline/model developed can be subsequently used to inform strategic monitoring tasks or adopted for intervention assessment.


## Hardware Requirements
This repository creates helper scripts for the following instrumentation:
* Allied Vision GigE Prosilica GC series camera
* ...


## Downloading and Initializing the Repository
This code has been tested on Ubuntu 18.04+ and Python 3.7+. For utilization of the Allied Vision cameras, we recommend having the Vimba SDK available on the local computer for manual camera setting, flashing firmware, or debugging camera operations. Image capture, done in this repository, requires installation of the Vimba library from Allied Vision.

For convenience, we recommend using `conda` to manage the repository package. To initialize the environment and dependencies appropriate for this repository, execute:

```conda env create -f environment.yml```

The environment can then be activated using `conda activate corals` to load the appropriate libraries and dependencies. The `environment.yml` script can be used to find the exhaustive list of dependencies, in the event that you would like to run everything as source. 

At the top-level of the repository, it is recommended that you create `data` and `output` folders for storing raw data and product outputs from this repository (`output` will be automatically generated if some analysis scripts are run if it is not already created). Pointers to environment variables, including paths to raw data or a location where output data can be saved, should be adjusted for your particular system in `environment.yml`.

## Data Collection -- Performing a Survey
To acquire data for analysis, you will need to attach a camera and XX *in situ* instruments. Use the specific instrument manuals to appropriate route power and communications cables, affix the sensors to the sampling rig, and performing hardware debugging/systems checks. Once all equipment is powered on, logging can be started by using the scripts under `loci > data_collection`. 


