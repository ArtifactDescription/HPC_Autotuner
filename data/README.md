# Test Dataset: Measured Configuration-performance Samples

In each .csv file, the test samples consisting of configuration and execution time are collected by the collector and are used as a sample pool/a test dataset by modeler.

### Workflow 1: LV -- LAMMPS and Voro++ coupled by ADIOS 1.
In-situ workflow: lmp-vr/wf-LV.csv

Separate components:
- LAMMPS: lmp-vr/lammps.csv
- Voro++: lmp-vr/voro.csv

### Workflow 2: HS -- Heat-transfer and Stage-write coupled by ADIOS 1
In-situ workflow: ht-sw/wf-HS.csv

Separate components:
- Heat-transfer: ht-sw/heatTransfer.csv
- Stage-write: ht-sw/stageWrite.csv

### Workflow 3: GP -- Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot coupled by ADIOS 2
In-situ workflow: gs-pdf/wf-GP.csv

Separate components:
- Gray-Scott: gs-pdf/grayScott.csv
- PDF Calculator: gs-pdf/pdfCalculate.csv
- PDF Plot: gs-pdf/pdfPlot.csv
- Gray Plot: gs-pdf/grayPlot.csv

