# Collector: Measuring Performance over Configurations

### 1. Select a scenario and setup the environment
- If the scenario for ADIOS1-coupled applications is selected, follow README in the directory adios1-coupled to setup the environment.
- If the scenario for ADIOS2-coupled applications is selected, follow README in the directory adios2-coupled to setup the environment.

### 2. Launch the collector in the directory collector
```
./workflow [App/Workflow_Name] [No_of_Nodes] [Experiment_ID]
```
App/Workflow_Name:

- lmp: LAMMPS;
- vr: Voro++;
- lvi: LAMMPS and Voro++ coupled (LV).

- ht: Heat-transfer;
- sw: Stage-write;
- hsi: Heat-transfer and Stage-write coupled (HS).

- gs: Gray-Scott;
- pdf: PDF Calculator;
- pplot: PDF Plot;
- gplot: Gray Plot;
- gp: Gray-Scott and PDF Calculator coupled;
- gv: Gray-Scott and Gray Plot coupled;
- gpv: Gray-Scott, PDF Calculator, and PDF Plot coupled;
- wf: Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot coupled.

No_of_Nodes: the number of computing nodes requested

### 3. Collect the measured configuration-performance samples
```
./collect.sh [Experiment_ID] [No_of_Components]
```
The path of collect.sh is 
- For LAMMPS, Voro++, LV, Heat-transfer, Stage-write, and HS: collector/collect.sh
- For Gray-Scott, PDF Calculator, PDF Plot, Gray Plot: collector/bp4/collect.sh
- For any applications coupled from Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot: collector/sst/collect.sh

The collected data is Experiment_ID/time_list.csv .
