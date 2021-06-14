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
$ pip3 install xgboost
```

### 2. Randomly generate configurations for in-situ workflows LV, HS, GP and their component applications.
```
./gen_smpl.sh
```
Random configurations for in-situ workflows LV, HS, GP and their component applications are in the directory lv, hs, and gp.


### 3. Auto-tuning algorithms -- RS, GEIST, AL, ALIC/CEAL, ALpH
- sample.py: Take the files in the directory data as inputs and read measured samples as a test dataset.
- modeler.py: Implement various auto-tuning algorithms.

### 4. Show hyperparameter sensitivities of auto-tuning algorithms.
```
./hyperparams.sh workflow_name performance_metric number_of_sample number_of_runs algorithm
```
- python_filename: num_iter, pct_rand, pct_repl
- workflow_name: lv, hs, gvpv
- performance_metric: exec_time, comp_time
- number of samples: 25, 50, 100
- number of runs: 100
- algorithm: al, geist, alic, alich, alph

### 5. Compare the performance of auto-tuning algorithms.
```
./evaluate.sh workflow_name performance_metric number_of_sample number_of_runs"
```
- workflow_name: lv, hs, gvpv
- performance_metric: exec_time, comp_time
- number of samples: 25, 50, 100
- number of runs: 100
