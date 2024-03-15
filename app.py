import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

class PayrollCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Sueldo")

        # Variables
        self.employee_name = tk.StringVar()
        self.worked_hours = tk.DoubleVar(value=0)
        self.hourly_rate = tk.DoubleVar(value=0)
        self.deductions = {}

        # Widgets
        tk.Label(root, text="Nombre del Empleado:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.employee_name).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Horas Trabajadas:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.worked_hours).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Tarifa por Día (MXN):").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.hourly_rate).grid(row=2, column=1, padx=10, pady=5)

        self.add_deduction_button = tk.Button(root, text="Agregar Deducción", command=self.add_deduction)
        self.add_deduction_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.calculate_button = tk.Button(root, text="Calcular Sueldo", command=self.calculate_pay)
        self.calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.deduction_frame = tk.Frame(root)
        self.deduction_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.report_text = tk.Text(root, width=70, height=20)
        self.report_text.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def add_deduction(self):
        deduction_name = simpledialog.askstring("Nueva Deducción", "Nombre de la Deducción:")
        if deduction_name:
            deduction_amount = simpledialog.askfloat("Nueva Deducción", "Cantidad de la Deducción:")
            if deduction_amount is not None:
                self.deductions[deduction_name] = deduction_amount
                self.update_deduction_list()

    def remove_deduction(self, deduction_name):
        if deduction_name in self.deductions:
            del self.deductions[deduction_name]
            self.update_deduction_list()

    def update_deduction_list(self):
        for widget in self.deduction_frame.winfo_children():
            widget.destroy()

        row = 0
        for deduction, amount in self.deductions.items():
            label = tk.Label(self.deduction_frame, text=f"{deduction}: {amount:.2f} MXN")
            label.grid(row=row, column=0, sticky="w")
            remove_button = tk.Button(self.deduction_frame, text="Eliminar", command=lambda d=deduction: self.remove_deduction(d))
            remove_button.grid(row=row, column=1, sticky="w")
            row += 0

    def calculate_pay(self):
        try:
            name = self.employee_name.get()
            hours = self.worked_hours.get()
            rate = self.hourly_rate.get()

            if hours <= 0 or rate <= 0:
                raise ValueError("Las horas y la tarifa deben ser mayores que cero.")

            base_pay = min(hours, 48) * rate
            overtime_hours = max(0, hours - 48)
            overtime_pay = overtime_hours * rate * 2  # Pago por horas extras (doble tarifa)

            total_pay = base_pay + overtime_pay

            total_deductions = sum(self.deductions.values())

            report = f"Reporte de Sueldo\n"
            report += f"Fecha y Hora de Generación: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n"
            report += f"Nombre del Empleado: {name}\n"
            report += f"Horas Trabajadas: {hours} (Horas Extras: {overtime_hours})\n"
            report += f"Tarifa por Día: {rate} MXN\n"
            report += f"\n"
            report += f"Sueldo Base: {base_pay:.2f} MXN\n"
            report += f"Sueldo por Horas Extras: {overtime_pay:.2f} MXN\n"
            report += f"\n"
            report += f"Deducciones:\n"
            for deduction, amount in self.deductions.items():
                report += f"- {deduction}: {amount:.2f} MXN\n"
            report += f"\n"
            report += f"Sueldo Neto: {total_pay - total_deductions:.2f} MXN\n"

            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, report)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollCalculator(root)
    root.mainloop()
