# Test Dataset: Measured Configuration-performance Samples

In each .csv file, the test samples consisting of configuration and execution time are collected by the collector and are used as a sample pool/a test dataset by modeler.

### Workflow 1: LV -- LAMMPS and Voro++ coupled by ADIOS 1.
In-situ workflow: lv/lv.csv

Separate components:
- LAMMPS: lv/lmp.csv
- Voro++: lv/vr.csv

### Workflow 2: HS -- Heat-transfer and Stage-write coupled by ADIOS 1
In-situ workflow: hs/hs.csv

Separate components:
- Heat-transfer: hs/ht.csv
- Stage-write: hs/sw.csv

### Workflow 3: GP -- Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot coupled by ADIOS 2
In-situ workflow coupled from Gray-Scott and PDF Calculator: gp/gp.csv
In-situ workflow coupled from Gray-Scott and Gray Plot: gp/gv.csv
In-situ workflow coupled from Gray-Scott, PDF Calculator, and PDF Plot: gp/gpv.csv
In-situ workflow coupled from Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot: gp/gvpv.csv

Separate components:
- Gray-Scott: gp/gs.csv
- PDF Calculator: gp/pdf.csv
- PDF Plot: gp/pplot.csv
- Gray Plot: gp/gplot.csv

