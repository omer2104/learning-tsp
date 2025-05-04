
conda create -n learning-tsp python=3.6.7
conda create -p "C:\Users\omers\CodeProjects\learning-tsp\conda_env" python=3.6.7

conda activate "C:\Users\omers\CodeProjects\learning-tsp\conda_env"

conda activate "C:\Users\omers\MegaSync\OS-light\תואר שני\תזה\code\learning-tsp\conda_env"
conda activate ".\.conda_env"
conda activate tsp

conda install pytorch-1.5.1-py3.6_cuda102_cudnn7_0.tar.bz2
conda install pytorch=1.5.1 cudatoolkit=10.1 -c pytorch
conda install pytorch==1.7.1 cudatoolkit=10.1 -c pytorch

conda install pytorch==1.3.1 cudatoolkit=10.1 -c pytorch
conda install pytorch==1.10.2 cudatoolkit=11.8 -c pytorch

conda install -c conda-forge cudatoolkit-dev

conda install numpy scipy cython tqdm scikit-learn matplotlib seaborn tensorboard pandas
conda install jupyterlab

pip install tensorboard_logger




/*
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\libnvvp
*/
Installed:
     - Nsight for Visual Studio 2022
     - Nsight Monitor
Not Installed:
     - Nsight for Visual Studio 2019
       Reason: VS2019 was not found
     - Integrated Graphics Frame Debugger and Profiler
       Reason: see https://developer.nvidia.com/nsight-vstools
     - Integrated CUDA Profilers
       Reason: see https://developer.nvidia.com/nsight-vstools
