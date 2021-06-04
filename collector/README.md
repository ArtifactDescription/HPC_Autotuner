# Collector: Measuring Performance over Configurations

### 1. Select a scenario and setup the environment
- If the scenario for ADIOS1-coupled applications is selected, follow README in the directory adios1-coupled to setup the environment.
- If the scenario for ADIOS2-coupled applications is selected, follow README in the directory adios2-coupled to setup the environment.

For example, 
```
cd adios2-coupled
./build.sh
source env.sh
```

### 2. Application/Workflow Name
- lmp: LAMMPS;
- vr: Voro++;
- lv: LAMMPS and Voro++ coupled (LV) with preset input parameters.
- lvi: LAMMPS and Voro++ coupled (LV) with configurable input parameters.

- ht: Heat-transfer;
- sw: Stage-write;
- hs: Heat-transfer and Stage-write coupled (HS) with preset input parameters.
- hsi: Heat-transfer and Stage-write coupled (HS) with configurable input parameters.

- gs: Gray-Scott;
- pdf: PDF Calculator;
- pplot: PDF Plot;
- gplot: Gray Plot;
- gp: Gray-Scott and PDF Calculator coupled;
- gv: Gray-Scott and Gray Plot coupled;
- gpv: Gray-Scott, PDF Calculator, and PDF Plot coupled;
- wf: Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot coupled.

### 2. Inputs
In each input file including configurations to be measured, each line is one configuration and each column is one parameter value separated by '\t'.

The input file for each application/workflow:
- lmp: each line includes (#process, PPN, #thread per process, #iterations per output) in the file lv/conf_lmp_smpls.csv. 
- vr: each line includes (#process, PPN, #thread per process) in the file lv/conf_vr_smpls.csv.
- lv: each line includes (lmp--#process, lmp--PPN, lmp--#thread per process, lmp--#iterations per output, vr--#process, vr--PPN, vr--#thread per process) in the file lv/conf_lv_smpls.csv.
- lvi: each line includes (#iterations in the phase from liquid to solid, #iterations in the solid phase, lmp--#process, lmp--PPN, lmp--#thread per process, lmp--#iterations per output, vr--#process, vr--PPN, vr--#thread per process) in the file lv/conf_lvi_smpls.csv.

- ht: each line includes (#process in X, #process in Y, PPN, #outputs, buffer size) in the file hs/conf_ht_smpls.csv.
- sw: each line includes (#process, PPN) in the file hs/conf_sw_smpls.csv.
- hs: each line includes (ht--#process in X, ht--#process in Y, ht--PPN, ht--#outputs, ht--buffer size, sw--#process, sw--PPN) in the file hs/conf_hs_smpls.csv.
- hsi: each line includes (X dimension size, Y dimension size, #iterations, ht--#process in X, ht--#process in Y, ht--PPN, ht--#outputs, ht--buffer size, sw--#process, sw--PPN) in the file hs/conf_hsi_smpls.csv.

- gs: each line includes (edge length of a cube, #simulation steps, #process, PPN) in the file bp4/smpl_gs.csv.
- pdf: each line includes (edge length of a cube, #simulation steps, #process, PPN) in the file bp4/smpl_pdf.csv.
- pplot/gplot: each line includes (edge length of a cube, #simulation steps) in the file bp4/smpl_plot.csv.
- gp/gpv/wf: each line includes (edge length of a cube, #simulation steps, gs--#process, gs--PPN, pdf--#process, pdf--PPN) in the file sst/smpl_gp.csv.
- gv: each line includes (edge length of a cube, #simulation steps, gs--#process, gs--PPN) in the file sst/smpl_gv.csv.

### 3. Launch the collector
```
./workflow [App/Workflow_Name] [No_of_Nodes] [Experiment_ID]
```
- [App/Workflow_Name] is listed above;
- [No_of_Nodes] is the number of computing nodes requested;
- [Experiment_ID] should be a unique ID for each experiment.

For example, 
```
./workflow wf 6 wf1
```

### 4. Collect the measured configuration-performance samples
```
./collect.sh [Experiment_ID] [No_of_Components]
```
The path of collect.sh is 
- For LAMMPS, Voro++, LV, Heat-transfer, Stage-write, and HS: collector/collect.sh
- For Gray-Scott, PDF Calculator, PDF Plot, Gray Plot: collector/bp4/collect.sh
- For any applications coupled from Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot: collector/sst/collect.sh

The collected data is in Experiment_ID/time_list.csv .

For example,
```
./collect.sh wf1 4
```
