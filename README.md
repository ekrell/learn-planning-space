# Learning Planning Spaces

PyTorch implementation of `LearnedSamplingDistributions` by Brian Ichter, James Harrison, Marco Pavone

Here, the focus is on learning focused search spaces for path planning applications

[Ichter et al. Github link](https://github.com/StanfordASL/LearnedSamplingDistributions)

Their paper: https://ieeexplore.ieee.org/abstract/document/8460730

    Ichter, B., Harrison, J., & Pavone, M. (2018, May). 
    Learning sampling distributions for robot motion planning. 
    In 2018 IEEE International Conference on Robotics and Automation (ICRA) (pp. 7087-7094). IEEE.

## Examples

**Linear Narrow Passages:** reproducing the example by Brian Ichter, James Harrison, Marco Pavone. Given an occupancy grid with small passages and a start and stop location, predict a focused search space for shortest-distance planning

- Notebook: [LinearNarrowPassages_Train.ipynb](LinearNarrowPassages_Train.ipynb)
- Ichter et al.'s original (tensorflow): https://github.com/StanfordASL/LearnedSamplingDistributions

**Boston Harbor:** given start, goal locations in a static environment, predict a focused search space for shortest-distance plannng

- Notebook: [BostonHarbor.ipynb](BostonHarbor.ipynb)
- Note: data too large for GitHub. Will upload somewhere soon and provide link

**Boston Harbor Water Currents:** given start, goal locations and water current predictions, predict a focused search space for energy-efficient planning

- Coming soon!
