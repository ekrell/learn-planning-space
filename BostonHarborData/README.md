# Boston Harbor
## Data generation

This directory includes the scripts used to generate the training data for the Boston Harbor problem.
The final product is a set of training samples stored in `BostHarbor_Samples.npz` on the repo's root.
It is not recommended to use these scripts unless more runs are needed. 
There are some hard-coded paths that may need to be adjusted... 

Solving the paths require installing the `conch` path planning repository: https://github.com/ekrell/conch

### 0. Move to this directory

    cd <...>/learn-planning-space/BostonHarbor

### 1. Generate paths

    bash BostonHarbor_data.bash

### 2. Create list of valid path files

    bash BostonHarbor_ls.bash > BostonHarbor_paths.txt

### 3. Convert the paths, occupancy grid to training samples

    python BostonHarbor_samples.py

### 4. Move to root

    cp BostonHarbor_Data.npz ..

