# Modeler: Implementation and Evaluation of Autotuning Algorithms
This offline modeler can run in any computer and uses the measured samples in the directory data as a sample pool/a test dataset.

### 1. Conda, pip, and jupyter installation
```
$ wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
$ ./Anaconda3-2021.05-Linux-x86_64.sh -p [installation_prefix_path]
...
Do you wish the installer to initialize Anaconda3 by running conda init? [yes|no]
[no] >>> yes
modified      /home/tongshu/.bashrc
==> For changes to take effect, close and re-open your current shell. <==
If you'd prefer that conda's base environment not be activated on startup,
   set the auto_activate_base parameter to false:
conda config --set auto_activate_base false
```
### 2. Randomly generate configurations for in-situ workflows LV, HS, GP and their component applications.
```
./gen_smpl.sh
```
Random configurations for in-situ workflows LV, HS, GP and their component applications are in the directory lv, hs, and gp.
### 3. Open modeler.ipynb and run it.
```
$ cd modeler
$ jupyter notebook
```
