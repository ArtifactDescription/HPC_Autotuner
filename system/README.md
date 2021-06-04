# Integrated Autotuner System
This Autotuner System integrates a collector, a modeler, and a searcher. The modeler incorporates multiple auto-tuning algorithms.

### 1. Select a scenario and setup the environment
- If the scenario for ADIOS1-coupled applications is selected, follow README in the directory adios1-coupled to setup the environment.

### 2. Launch the autotuner
```
./workflow [App/Workflow_Name] [Algorithm_Name] [Experiment_ID]
```
- [App/Workflow_Name] is listed above;
- [Algorithm_Name] is the name of the auto-tuning algorithm used in the autotuner;
- [Experiment_ID] should be a unique ID for each experiment.

