# Goodman Target Simulator

This is a very simple script that simulates Goodman data. At this moment, it simply generates an image with one or more gaussian 
profiles that mimic observations.

## Use me

The best way to use the Goodman Target Simulator is by installing it and running the `goodsim` script. The installation can be done as follows:

    mkdir $path_to_gts
    cd $path_to_gts
    git clone https://github.com/b1quint/goodman_target_simulator.git .
    pip install .
    
Since any Python installation can update your current packages, I strongly recommend you to use [Virtual Environments](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) or [Anaconda Environments](https://conda.io/docs/using/envs.html).

  Once installed, the `goodsim` script will be installed in your system and you can run it from any terminal (as long as you are within the virtual environment where it was installed). If you want to know more of how it can be run, just type:
  
      goodsim --help 


## To Do

  - [ ] Add distortions.
  - [ ] Poisson noise?
  - [ ] New Blue Camera and Red Camera templates.
  - [ ] Real spectral response?
