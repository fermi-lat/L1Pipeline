#!/bin/bash
export PIPELINE_MODE=prod
singularity exec --bind /sdf/group/fermi/a:/afs/slac/g/glast --bind /sdf:/sdf /sdf/group/fermi/sw/containers/fermi-rhel6.sif ./install.py
#/sdf/home/g/glast/a/pipeline-II/prod/pipeline load -m DEV xml/L1ProcS3DF-6.1.xml
