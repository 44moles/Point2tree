micromamba create -y --name pdal-env python=3.8.13
micromamba shell init --shell bash --root-prefix=~/micromamba
eval "$(micromamba shell hook --shell bash)"
micromamba activate pdal-env

pip install -r requirements.txt
micromamba install -y -c conda-forge python-pdal
micromamba install -y numpy==1.22.4