# DrosWAFO-py
Data analysis tool for calculating Wall Falling Behavior (WAFO) in drosophila from frame-by-frame x-y positions. Outputs a .csv file containing average Distance From Center (aDFC), which is a metric for determining WAFO.

---

### **Usage Guide**

1. **Prepare Input Files**:
   - Ensure that your input files are tab-delimited `.txt` files containing columns for `Pos. X (mm)` and `Pos. Y (mm)`.

2. **Run the Program**:
   - Launch the program in your Python environment.
   - Use the slider at the top to select how many flies you want to process. (Max 10)
   - Click the 'Select File #" to upload your .txt file/directory.

3. **Specify Center Points**:
   - For each file, input the `x` and `y` coordinates of the center point of the arena in the corresponding boxes.

4. **Provide Pixel-to-MM Conversion Ratio**:
   - Input the pixel-to-mm ratio in the format `pixels:mm` (e.g., `224:10`).

5. **View Results**:
   - The program will display the average distance from the center in both pixels and millimeters for each file.
   - At the end of the run, the program will save the data to .csv and prompt you select the save location for the file.

---
