import customtkinter
import pandas as pd
import numpy as np
from tkinter import filedialog

#Function to calculate the average distance from the center.
def average_distance_from_center(file_path, center_x, center_y, px_to_mm_ratio):
    data = pd.read_csv(file_path, delimiter="\t")
    x_positions = data["Pos. X (mm)"]
    y_positions = data["Pos. Y (mm)"]
    distances = np.sqrt((x_positions - center_x)**2 + (y_positions - center_y)**2)
    average_distance_px = distances.mean()
    average_distance_mm = average_distance_px * px_to_mm_ratio
    return average_distance_px, average_distance_mm

# Multiple File Processing
def process_files(file_paths, center_coords, px_to_mm_ratio):
    results = []
    for i, file_path in enumerate(file_paths):
        center_x, center_y = center_coords[i]
        avg_distance_px, avg_distance_mm = average_distance_from_center(file_path, center_x, center_y, px_to_mm_ratio)
        results.append((file_path, avg_distance_px, avg_distance_mm))
    return results

#GUI (CustomTkinter)
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("DrosWAFO")
        self.geometry("800x600")

        # grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Dark mode switch
        self.theme_switch = customtkinter.CTkSwitch(self, text="Light Mode", command=self.change_mode)
        self.theme_switch.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # number of files slider
        self.file_count_slider = customtkinter.CTkSlider(self, from_=1, to=10, number_of_steps=9, command=self.update_file_inputs)
        self.file_count_slider.grid(row=1, column=0, pady=10, sticky="n")
        self.file_count_label = customtkinter.CTkLabel(self, text="Number of files: 1")
        self.file_count_label.grid(row=2, column=0, pady=10, sticky="n")

    
        self.textbox_frame = customtkinter.CTkFrame(self)
        self.textbox_frame.grid(row=3, column=0, pady=10, sticky="nsew")
        self.textbox_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Ratio Converter input
        self.conversion_ratio_entry = customtkinter.CTkEntry(self, placeholder_text="Enter conversion ratio (pixels:mm)")
        self.conversion_ratio_entry.grid(row=4, column=0, pady=10, sticky="ew")

        # Process button
        self.process_button = customtkinter.CTkButton(self, text="Process", command=self.process)
        self.process_button.grid(row=5, column=0, pady=10, sticky="n")

        # Results label
        self.results_label = customtkinter.CTkLabel(self, text="Results will be displayed here")
        self.results_label.grid(row=6, column=0, pady=10, sticky="n")

        # Initialize textboxes
        self.textboxes = []
        self.center_entries = []
        self.update_file_inputs(1)

    def change_mode(self):
        if self.theme_switch.get():
            customtkinter.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Dark Mode")
        else:
            customtkinter.set_appearance_mode("Light")
            self.theme_switch.configure(text="Light Mode")


    
    def update_file_inputs(self, value):
        num_files = int(value)
        self.file_count_label.configure(text=f"Number of files: {num_files}")
        for widget in self.textbox_frame.winfo_children():
            widget.destroy()
        self.textboxes.clear()
        self.center_entries.clear()

        for i in range(num_files):
            file_button = customtkinter.CTkButton(self.textbox_frame, text=f"Select File {i+1}", command=lambda i=i: self.select_file(i))
            file_button.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            center_x_entry = customtkinter.CTkEntry(self.textbox_frame, placeholder_text=f"Center X for File {i+1}")
            center_y_entry = customtkinter.CTkEntry(self.textbox_frame, placeholder_text=f"Center Y for File {i+1}")
            center_x_entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            center_y_entry.grid(row=i, column=2, padx=10, pady=10, sticky="ew")
            self.textboxes.append(file_button)
            self.center_entries.append((center_x_entry, center_y_entry))

    def select_file(self, index):
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            self.textboxes[index].configure(text=file_path)

    def process(self):
        file_paths = [textbox.cget("text") for textbox in self.textboxes if textbox.cget("text")]
        center_coords = []
        for center_x_entry, center_y_entry in self.center_entries:
            try:
                center_x = float(center_x_entry.get())
                center_y = float(center_y_entry.get())
                center_coords.append((center_x, center_y))
            except ValueError:
                self.results_label.configure(text="Invalid center coordinates.")
                return

        try:
            pixels, mm = map(float, self.conversion_ratio_entry.get().split(":"))
            px_to_mm_ratio = mm / pixels
        except ValueError:
            self.results_label.configure(text="Invalid conversion ratio. Use 'pixels:mm' format.")
            return

        if len(file_paths) != len(center_coords):
            self.results_label.configure(text="Mismatch between files and coordinates.")
            return

        results = process_files(file_paths, center_coords, px_to_mm_ratio)
        result_text = "\n".join([f"{file}: {px:.2f}px, {mm:.2f}mm" for file, px, mm in results])
        self.results_label.configure(text=result_text)

        # CSV save
        self.save_to_csv(results)

    def save_to_csv(self, results):
        """Save results to a CSV file."""
        # Format to .CSV file
        df = pd.DataFrame(results, columns=["File Path", "Average Distance (px)", "Average Distance (mm)"])
        
        # Ask user for file directory to save to
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            df.to_csv(save_path, index=False)
            self.results_label.configure(text=f"Results saved to {save_path}")



if __name__ == "__main__":
    app = App()
    app.mainloop()
