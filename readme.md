# SWC EN Behavior Module Starter Pack

This is a collection of code to help you get started analyzing the data collected by Cristina Mazuski. A subset of the data including the DLC output coordinates is included in this repository (except for Female3.npy which is too large), but you should also check out the original dataset [here](https://www.dropbox.com/sh/dukxar7nv0u2op2/AAACouCTJTr1f0G43p3hHRlXa?dl=0). All code is in Python, easily run through jupyter notebooks. You should be able to run most of this without any problem on a typical laptop. If you want to do some more sophisticated analysis using larger neural nets, you will need to install the GPU versions of the deep learning packages, but this is definitely not necessary. I have tested this on Windows, and also on Linux through WSL, and it _should_ work on Mac, barring minor wrinkles.

## Installation

Follow the simple steps if you just want to get it working as fast as possible. Read the explanations below if you want to learn more, or if something goes wrong and you need to troubleshoot. 

### Steps 
1. Install Anaconda from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Clone or copy this github repository to your local computer. Simplest way is to click on Code > Download Zip on the github web interface, and extract the zip file.
3. Launch Anaconda Prompt if you are on Windows, or just launch a terminal window if you are on Mac. 
4. Navigate to the root folder of the downloaded github repository in the terminal by typing `cd C:\your\path\here\swc-en-social`
5. In the terminal, type `conda env create -f env-cpu.yml` and follow instructions to install all of the required packages. Say yes to whatever conda asks.
6. Activate this environment by typing `conda activate swc-en-social`
7. Launch a jupyter notebook server by typing `jupyter notebook`


### Explanation and Troubleshooting

You should install Python through `conda`, which is a package manager. Conda is very useful tool when developing python code, as it keeps track of all the tens of packages you install and makes sure they are all compatible with each other. You typically create a new conda "environment" which contains a specific version of Python and all of the packages you need for each project. This makes it easier to share your projects, so if you develop something on Windows and you want to run it on a Mac you can share the environment file and the other person can get all of the dependencies easily (usually). Read [this](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) to learn about how to manage conda environments. Anaconda is the full installation with all the bells and whistles, and miniconda is a bare-bones version. I've tested with Anaconda only but Miniconda will probably work too. 

The command `conda env create -f env-basic-cpu.yml` creates a new conda environment based on the requirements that I included in this repository. It should work without a problem, though it's possible that on some platforms there are a few minor wrinkles. If you do encounter this issue, you can create a fresh conda environment and install the required packages by running the following commands (omit `cpuonly` from the last line if you are on Mac):
```
conda create --name swc-en-social numpy matplotlib scikit-learn
conda install -c conda-forge notebook
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

Next, we activate the environment, and launch a `jupyter notebook` server. This is a platform that lets you write and run snippets of python code in browser and see the results immediately, without having to go 