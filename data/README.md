# Test Dataset: Measured Configuration-performance Samples

In each .csv file, the test samples consisting of configuration and input parameters and execution time are collected by the collector and are used as a sample pool/a test dataset by modeler.

### Workflow 1: LV -- LAMMPS and Voro++ coupled by ADIOS 1.
In-situ workflow LV (lv/lv.csv): (lmp--#process, lmp--PPN, lmp--#thread per process, vr--#process, vr--PPN, vr--#thread per process, lmp--#iterations per output, lmp--#iterations in the phase from liquid to solid, lmp--#iterations in the solid phase, LV--execution time, lmp--execution time, vr--execution time)

Separate components:
- LAMMPS (lv/lmp.csv): (lmp--#process, lmp--PPN, lmp--#thread per process, lmp--#iterations per output, lmp--#iterations in the phase from liquid to solid, lmp--#iterations in the solid phase, lmp--execution time)
- Voro++ (lv/vr.csv): (vr--#process, vr--PPN, vr--#thread per process, lmp--#iterations per output, lmp--#iterations in the phase from liquid to solid, lmp--#iterations in the solid phase, vr--execution time)

### Workflow 2: HS -- Heat-transfer and Stage-write coupled by ADIOS 1
In-situ workflow HS (hs/hs.csv): (ht--#process in X, ht--#process in Y, ht--PPN, ht--buffer size, sw--#process, sw--PPN, ht--#outputs, ht--X dimension size, ht--Y dimension size, ht--#iterations, HS--execution time, ht--execution time, sw--execution time)

Separate components:
- Heat-transfer (hs/ht.csv): (ht--#process in X, ht--#process in Y, ht--PPN, ht--buffer size, ht--#outputs, ht--X dimension size, ht--Y dimension size, ht--#iterations, ht--execution time)
- Stage-write (hs/sw.csv): (sw--#process, sw--PPN, ht--#outputs, ht--X dimension size, ht--Y dimension size, ht--#iterations, sw--execution time)

### Workflow 3: GP -- Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot coupled by ADIOS 2
- In-situ workflow coupled from Gray-Scott and PDF Calculator (gp/gp.csv): (gs--#process, gs--PPN, pdf--#process, pdf--PPN, gs--edge length of a cube, gs--#simulation steps, gp--execution time, gs-execution time, pdf--execution time)
- In-situ workflow coupled from Gray-Scott and Gray Plot (gp/gv.csv): (gs--#process, gs--PPN, gs--edge length of a cube, gs--#simulation steps, gv--execution time, gs--execution time, gplot--execution time)
- In-situ workflow coupled from Gray-Scott, PDF Calculator, and PDF Plot (gp/gpv.csv): (gs--#process, gs--PPN, pdf--#process, pdf--PPN, gs--edge length of a cube, gs--#simulation steps, gpv--execution time, gs-execution time, pdf--execution time, pplot--execution time)
- In-situ workflow coupled from Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot (gp/gvpv.csv): (gs--#process, gs--PPN, pdf--#process, pdf--PPN, gs--edge length of a cube, gs--#simulation steps, gvpv--execution time, gs-execution time, gplot--execution time, pdf--execution time, pplot--execution time)

Separate components:
- Gray-Scott (gp/gs.csv): (gs--#process, gs--PPN, gs--edge length of a cube, gs--#simulation steps, gs--execution time)
- PDF Calculator (gp/pdf.csv): (pdf--#process, pdf--PPN, gs--edge length of a cube, gs--#simulation steps, pdf-execution time)
- PDF Plot (gp/pplot.csv): (gs--edge length of a cube, gs--#simulation steps, pplot--execution time)
- Gray Plot (gp/gplot.csv): (gs--edge length of a cube, gs--#simulation steps, gplot--execution time)

