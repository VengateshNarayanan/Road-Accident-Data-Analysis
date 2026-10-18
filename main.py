
import tkinter as tk

from data_loader import load_data
from dashboard import AccidentDashboard


def main():
    data = load_data()

    root = tk.Tk()
    app = AccidentDashboard(root, data)
    root.mainloop()


if __name__ == "__main__":
    main()
