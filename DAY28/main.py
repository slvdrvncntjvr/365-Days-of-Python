import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

DAY_FOLDER = "DAY28"
DATA_FILE = os.path.join(DAY_FOLDER, r"data/world_data.csv")
MAP_FILE = os.path.join(DAY_FOLDER, r"data/10m_admin_0_countries.geojson")  # Updated to GeoJSON file

class WorldDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("World Dashboard")
        self.root.geometry("900x600")
        
        try:
            self.data = pd.read_csv(DATA_FILE)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Data file not found: {DATA_FILE}")
            self.data = pd.DataFrame(columns=["Country", "Population", "GDP", "Continent"])
        
        try:
            self.world_map = gpd.read_file(MAP_FILE)  # Load GeoJSON file
        except Exception as e:
            messagebox.showerror("Error", f"Could not load map file: {e}")
            self.world_map = gpd.GeoDataFrame()

        title = tk.Label(root, text="World Data Dashboard", font=("Arial", 18, "bold"))
        title.pack(pady=10)
        
        self.selected_country = tk.StringVar()
        country_label = tk.Label(root, text="Select a Country:", font=("Arial", 12))
        country_label.pack(pady=5)
        self.country_dropdown = ttk.Combobox(
            root, textvariable=self.selected_country, state="readonly", width=30
        )
        self.country_dropdown["values"] = sorted(self.data["Country"].unique())
        self.country_dropdown.pack(pady=5)
        
        generate_button = ttk.Button(root, text="Generate Data", command=self.show_country_data)
        generate_button.pack(pady=10)
        
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(pady=20)
        
        self.stats_label = tk.Label(root, text="", font=("Arial", 12))
        self.stats_label.pack(pady=10)
    
    def show_country_data(self):
        country = self.selected_country.get()
        if not country:
            messagebox.showerror("Error", "Please select a country!")
            return
        
        country_data = self.data[self.data["Country"] == country]
        if country_data.empty:
            messagebox.showinfo("Info", f"No data found for {country}.")
            return
        
        country_data = country_data.iloc[0]
        country_map = self.world_map[self.world_map["ADMIN"] == country]  # Ensure column name matches
    
        self.ax.clear()
        base_map = self.world_map.plot(ax=self.ax, color="lightgrey", edgecolor="black")
        if not country_map.empty:
            country_map.plot(ax=self.ax, color="dodgerblue")
        self.ax.set_title(f"Map of {country}", fontsize=14)
        self.ax.axis("off")
        
        self.canvas.draw()
        stats_text = (
            f"Country: {country}\n"
            f"Population: {country_data['Population']:,}\n"
            f"GDP (in USD): ${country_data['GDP']:,}\n"
            f"Continent: {country_data['Continent']}\n"
        )
        self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = WorldDashboardApp(root)
    root.mainloop()