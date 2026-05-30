from math import ceil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# =========================
# KLASA PRODUKTU
# =========================

class Product:
    def __init__(
        self,
        name,
        lead_time,
        stock,
        safety_stock=0,
        batch_size=1,
    ):
        self.name = name
        self.lead_time = lead_time
        self.stock = stock
        self.safety_stock = safety_stock
        self.batch_size = batch_size
        self.components = []

    def add_component(self, component, quantity):
        self.components.append((component, quantity))


# =========================
# KLASA ZAPOTRZEBOWANIA
# =========================

class Demand:
    def __init__(self, product, quantity, due_day):
        self.product = product
        self.quantity = quantity
        self.due_day = due_day


# =========================
# SYSTEM MRP
# =========================

class MRPSystem:
    def __init__(self):
        self.results = []

    def calculate(self, demand):

        self.results.clear()

        self._process_product(
            product=demand.product,
            required_quantity=demand.quantity,
            due_day=demand.due_day,
            level=0,
        )

        return self.results

    def _process_product(
        self,
        product,
        required_quantity,
        due_day,
        level,
    ):

        gross_requirement = required_quantity

        available_stock = max(
            0,
            product.stock - product.safety_stock
        )

        net_requirement = max(
            0,
            gross_requirement - available_stock
        )

        if net_requirement > 0:
            planned_order = (                                    ### planowane
                ceil(net_requirement / product.batch_size)
                * product.batch_size
            )
        else:
            planned_order = 0

        if planned_order > 0:
            release_day = due_day - product.lead_time
            due_value = due_day
        else:
            release_day = 0
            due_value = 0

        self.results.append({
            "level": level,
            "name": product.name,
            "gross": gross_requirement,
            "stock": product.stock,
            "safety": product.safety_stock,
            "net": net_requirement,
            "batch": product.batch_size,
            "planned": planned_order,
            "due": due_value,
            "release": release_day,
        })

        for component, quantity in product.components:

            child_requirement = gross_requirement * quantity

            self._process_product(
                product=component,
                required_quantity=child_requirement,
                due_day=release_day,
                level=level + 1,
            )


# =========================
# DEFINICJA PRODUKTÓW
# =========================

bicycle = Product(
    name="Rower",
    lead_time=2,
    stock=5,
    safety_stock=1,
    batch_size=10,
)

frame = Product(
    name="Rama",
    lead_time=3,
    stock=10,
    safety_stock=2,
    batch_size=5,
)

wheel = Product(
    name="Koło",
    lead_time=2,
    stock=20,
    safety_stock=4,
    batch_size=10,
)

tire = Product(
    name="Opona",
    lead_time=1,
    stock=50,
    safety_stock=5,
    batch_size=20,
)

rim = Product(
    name="Obręcz",
    lead_time=1,
    stock=30,
    safety_stock=3,
    batch_size=10,
)


# =========================
# STRUKTURA BOM
# =========================

bicycle.add_component(frame, 1)
bicycle.add_component(wheel, 2)

wheel.add_component(tire, 1)
wheel.add_component(rim, 1)


# =========================
# INTERFEJS GRAFICZNY
# =========================

root = tk.Tk()

root.title("System MRP")
root.geometry("1100x650")


# =========================
# PANEL WEJŚCIOWY
# =========================

input_frame = tk.Frame(root)
input_frame.pack(pady=10)


# ilość produktów

tk.Label(
    input_frame,
    text="Ilość rowerów:"
).grid(row=0, column=0, padx=5)

quantity_entry = tk.Entry(input_frame)
quantity_entry.grid(row=0, column=1, padx=5)

quantity_entry.insert(0, "25")


# dzień realizacji

tk.Label(
    input_frame,
    text="Dzień realizacji:"
).grid(row=0, column=2, padx=5)

day_entry = tk.Entry(input_frame)
day_entry.grid(row=0, column=3, padx=5)

day_entry.insert(0, "10")


# =========================
# TABELA
# =========================

columns = (
    "Poziom",
    "Produkt",
    "Brutto",
    "Stock",
    "Safety",
    "Netto",
    "Partia",
    "Planowane",
    "Termin",
    "Start",
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# =========================
# FUNKCJA OBLICZEŃ
# =========================

def calculate_mrp():

    try:

        quantity = int(quantity_entry.get())
        due_day = int(day_entry.get())

        demand = Demand(
            product=bicycle,
            quantity=quantity,
            due_day=due_day,
        )

        mrp = MRPSystem()

        results = mrp.calculate(demand)

        # usuwanie poprzednich wyników

        for row in tree.get_children():
            tree.delete(row)

        # dodawanie nowych wyników

        for result in results:

            tree.insert(
                "",
                "end",
                values=(
                    result["level"],
                    result["name"],
                    result["gross"],
                    result["stock"],
                    result["safety"],
                    result["net"],
                    result["batch"],
                    result["planned"],
                    result["due"],
                    result["release"],
                )
            )

    except ValueError:

        messagebox.showerror(
            "Błąd",
            "Wprowadź poprawne liczby"
        )


# =========================
# PRZYCISK
# =========================

calculate_button = tk.Button(
    root,
    text="Oblicz MRP",
    command=calculate_mrp,
    font=("Arial", 12),
    height=2,
    width=20,
)

calculate_button.pack(pady=10)


# =========================
# START PROGRAMU
# =========================

root.mainloop()