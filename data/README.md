# Test Dataset: Measured Configuration-performance Samples

In each .csv file, the test samples consisting of configuration and input parameters and execution time are collected by the collector and are used as a sample pool/a test dataset by modeler.

### Workflow 1: LV -- LAMMPS and Voro++ coupled by ADIOS 1.
In-situ workflow LV (lv/lv.csv): configuration parameters are (lmp--#process, lmp--PPN, lmp--#thread per process, vr--#process, vr--PPN, vr--#thread per process), and input parameters are (lmp--#iterations per output, lmp--#iterations in the phase from liquid to solid, lmp--#iterations in the solid phase); the performance is LV--execution time, which is the maximum of lmp--execution time and vr--execution time

Separate components:
- LAMMPS (lv/lmp.csv): configuration parameters are (lmp--#process, lmp--PPN, lmp--#thread per process), and input parameters are (lmp--#iterations per output, lmp--#iterations in the phase from liquid to solid, lmp--#iterations in the solid phase; the performance is lmp--execution time.
- Voro++ (lv/vr.csv): configuration parameters are (vr--#process, vr--PPN, vr--#thread per process), and input parameters are (lmp--#iterations per output, lmp--#iterations in the phase from liquid to solid, lmp--#iterations in the solid phase); the performance is vr--execution time.

### Workflow 2: HS -- Heat-transfer and Stage-write coupled by ADIOS 1
In-situ workflow HS (hs/hs.csv): configuration parameters are (ht--#process in X, ht--#process in Y, ht--PPN, ht--buffer size, sw--#process, sw--PPN), and input parameters are (ht--#outputs, ht--X dimension size, ht--Y dimension size, ht--#iterations); the performance is HS--execution time, which is the maximum of ht--execution time and sw--execution time.

Separate components:
- Heat-transfer (hs/ht.csv): configuration parameters are (ht--#process in X, ht--#process in Y, ht--PPN, ht--buffer size), and input parameters are (ht--#outputs, ht--X dimension size, ht--Y dimension size, ht--#iterations); the performance is ht--execution time.
- Stage-write (hs/sw.csv): configuration parameters are (sw--#process, sw--PPN), and input parameters are (ht--#outputs, ht--X dimension size, ht--Y dimension size, ht--#iterations); the performance is sw--execution time.

### Workflow 3: GP -- Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot coupled by ADIOS 2
- In-situ workflow coupled from Gray-Scott and PDF Calculator (gp/gp.csv): (gs--#process, gs--PPN, pdf--#process, pdf--PPN, gs--edge length of a cube, gs--#simulation steps, gp--execution time, gs-execution time, pdf--execution time)
- In-situ workflow coupled from Gray-Scott and Gray Plot (gp/gv.csv): (gs--#process, gs--PPN, gs--edge length of a cube, gs--#simulation steps, gv--execution time, gs--execution time, gplot--execution time)
- In-situ workflow coupled from Gray-Scott, PDF Calculator, and PDF Plot (gp/gpv.csv): (gs--#process, gs--PPN, pdf--#process, pdf--PPN, gs--edge length of a cube, gs--#simulation steps, gpv--execution time, gs-execution time, pdf--execution time, pplot--execution time)
- In-situ workflow coupled from Gray-Scott, PDF Calculator, PDF Plot, and Gray Plot (gp/gvpv.csv): configuration parameters are (gs--#process, gs--PPN, pdf--#process, pdf--PPN), and input parameters are (gs--edge length of a cube, gs--#simulation steps); the performance is gvpv--execution time, which is the maximum of (gs-execution time, gplot--execution time, pdf--execution time, pplot--execution time)

Separate components:
- Gray-Scott (gp/gs.csv): configration parameters are (gs--#process, gs--PPN), and input parameters are (gs--edge length of a cube, gs--#simulation steps); the performance is gs--execution time.
- PDF Calculator (gp/pdf.csv): configuration parameters are (pdf--#process, pdf--PPN), and input parameters are (gs--edge length of a cube, gs--#simulation steps); the performance is pdf-execution time.
- PDF Plot (gp/pplot.csv): input parameters are (gs--edge length of a cube, gs--#simulation steps); the performance is pplot--execution time.
- Gray Plot (gp/gplot.csv): input parameters are (gs--edge length of a cube, gs--#simulation steps); the performance is gplot--execution time.

