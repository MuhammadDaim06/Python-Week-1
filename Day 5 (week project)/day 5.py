import tkinter as tk
from tkinter import ttk, messagebox

class CampusPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Expansion Planner")
        self.root.geometry("1000x600")
        
        self.buildings = []
        self.next_id = 1
        
        self.create_widgets()
        self.add_sample_data()
        self.refresh_list()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.LabelFrame(main_frame, text="Add New Building", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(left_frame, text="Building Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(left_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(left_frame, text="Area (sq ft):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.area_entry = ttk.Entry(left_frame, width=30)
        self.area_entry.grid(row=1, column=1, pady=5, padx=5)
        self.area_entry.insert(0, "5000")
        
        ttk.Label(left_frame, text="Floors:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.floors_entry = ttk.Entry(left_frame, width=30)
        self.floors_entry.grid(row=2, column=1, pady=5, padx=5)
        self.floors_entry.insert(0, "2")
        
        ttk.Label(left_frame, text="Building Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.type_combo = ttk.Combobox(left_frame, values=["Academic", "Admin", "Residential", "Lab", "Library"], width=27)
        self.type_combo.grid(row=3, column=1, pady=5, padx=5)
        self.type_combo.set("Academic")
        
        ttk.Label(left_frame, text="Cost ($):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.cost_entry = ttk.Entry(left_frame, width=30)
        self.cost_entry.grid(row=4, column=1, pady=5, padx=5)
        self.cost_entry.insert(0, "100000")
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Add Building", command=self.add_building).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_building).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        right_frame = ttk.LabelFrame(main_frame, text="Building List", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Name", "Area", "Floors", "Type", "Cost")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "Name" else 150)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.total_label = ttk.Label(info_frame, text="Total Buildings: 0 | Total Cost: $0", font=("Arial", 10, "bold"))
        self.total_label.pack(side=tk.LEFT)
        
        ttk.Button(info_frame, text="Show Report", command=self.show_report).pack(side=tk.RIGHT, padx=5)
        ttk.Button(info_frame, text="Export Data", command=self.export_data).pack(side=tk.RIGHT, padx=5)
    
    def add_building(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter building name")
            return
        
        try:
            area = float(self.area_entry.get())
            floors = int(self.floors_entry.get())
            cost = float(self.cost_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for area, floors, and cost")
            return
        
        building = {
            "id": self.next_id,
            "name": name,
            "area": area,
            "floors": floors,
            "type": self.type_combo.get(),
            "cost": cost
        }
        
        self.buildings.append(building)
        self.next_id += 1
        
        self.name_entry.delete(0, tk.END)
        self.area_entry.delete(0, tk.END)
        self.area_entry.insert(0, "5000")
        self.floors_entry.delete(0, tk.END)
        self.floors_entry.insert(0, "2")
        self.cost_entry.delete(0, tk.END)
        self.cost_entry.insert(0, "100000")
        
        self.refresh_list()
        messagebox.showinfo("Success", f"Building '{name}' added successfully!")
    
    def delete_building(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a building to delete")
            return
        
        item = self.tree.item(selected[0])
        building_id = int(item["values"][0])
        
        if messagebox.askyesno("Confirm", "Delete this building?"):
            self.buildings = [b for b in self.buildings if b["id"] != building_id]
            self.refresh_list()
    
    def clear_all(self):
        if messagebox.askyesno("Confirm", "Delete all buildings?"):
            self.buildings = []
            self.next_id = 1
            self.refresh_list()
    
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_cost = 0
        for building in self.buildings:
            self.tree.insert("", tk.END, values=(
                building["id"],
                building["name"],
                f"{building['area']:,.0f}",
                building["floors"],
                building["type"],
                f"${building['cost']:,.2f}"
            ))
            total_cost += building["cost"]
        
        self.total_label.config(text=f"Total Buildings: {len(self.buildings)} | Total Cost: ${total_cost:,.2f}")
    
    def show_report(self):
        if not self.buildings:
            messagebox.showinfo("Report", "No buildings to display")
            return
        
        report = "=" * 60 + "\n"
        report += "CAMPUS EXPANSION REPORT\n"
        report += "=" * 60 + "\n\n"
        
        total_cost = 0
        for b in self.buildings:
            report += f"ID: {b['id']}\n"
            report += f"Name: {b['name']}\n"
            report += f"Type: {b['type']}\n"
            report += f"Area: {b['area']:,.0f} sq ft\n"
            report += f"Floors: {b['floors']}\n"
            report += f"Cost: ${b['cost']:,.2f}\n"
            report += "-" * 40 + "\n"
            total_cost += b['cost']
        
        report += f"\nTOTAL BUILDINGS: {len(self.buildings)}\n"
        report += f"TOTAL COST: ${total_cost:,.2f}\n"
        report += f"AVERAGE COST: ${total_cost/len(self.buildings):,.2f}\n"
        
        messagebox.showinfo("Campus Expansion Report", report)
    
    def export_data(self):
        if not self.buildings:
            messagebox.showerror("Error", "No data to export")
            return
        
        data = "ID,Name,Area,Floors,Type,Cost\n"
        for b in self.buildings:
            data += f"{b['id']},{b['name']},{b['area']},{b['floors']},{b['type']},{b['cost']}\n"
        
        with open("campus_data.csv", "w") as f:
            f.write(data)
        
        messagebox.showinfo("Success", "Data exported to campus_data.csv")
    
    def add_sample_data(self):
        samples = [
            ("Science Building", 15000, 4, "Lab", 2500000),
            ("Library", 12000, 3, "Library", 1800000),
            ("Admin Block", 8000, 2, "Admin", 1200000),
            ("Student Center", 10000, 2, "Academic", 1500000),
            ("Research Lab", 20000, 5, "Lab", 3500000)
        ]
        
        for name, area, floors, btype, cost in samples:
            self.buildings.append({
                "id": self.next_id,
                "name": name,
                "area": area,
                "floors": floors,
                "type": btype,
                "cost": cost
            })
            self.next_id += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusPlanner(root)
    root.mainloop()