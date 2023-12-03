import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

######################
# EXPERIMENTS
######################


class NN:
    """
    Implementation of simple neural network with two neurons.
    """
    def __init__(self, W: np.array, mi: float) -> None:
        self.mi = mi
        self.W = W

    def forward(self, x: float, y: float) -> np.array:
        new_x = sigmoid(self.W[0][0]*x + self.W[0][1]*y, self.mi)
        new_y = sigmoid(self.W[1][0]*x + self.W[1][1]*y, self.mi)
        return new_x, new_y


def sigmoid(x: float, mi: float) -> float:
    return 1 / (1 + np.exp(-mi*x))


def update_plot(a, b, max_mi):
    """
    Parameters:
        a, b - weights coefficients,
        n - number of mi samples,
        iterations - number of nn epochs,
        last - number of plotted epochs,
        initial x - initial value of x,
        initial y - initial value of y.
    """

    global x, y

    n = 600
    iterations = 200
    last = 100

    initial_x = 0.35 * np.ones(n)
    initial_y = 0.55 * np.ones(n)

    x = np.copy(initial_x)
    y = np.copy(initial_y)

    min_mi = 0
    max_mi = max_mi
    mi = np.linspace(min_mi, max_mi, n)

    ax1.clear()
    ax2.clear()

    w11, w12, w21, w22 = -a, a, -b, b
    W = np.array([[w11, w12], [w21, w22]])

    lyapunov = np.zeros(n)
    plt.style.use('ggplot')

    for i in range(iterations):
        nn = NN(W, mi)
        x, y = nn.forward(x, y)
        lyapunov += np.log(abs(mi - 2 * mi * x))

        if i >= (iterations - last):
            ax1.plot(mi, x, '.', color='#800000', markersize=0.75, alpha=1)
            ax2.plot(mi, y, '.', color='#0A381F', markersize=0.75, alpha=1)

    plt.suptitle(f'A: {round(a, 2)}, B: {round(b, 2)}')

    ax1.set_xlim(min_mi, max_mi)
    ax1.set_title("Bifurkacja X")

    ax2.set_xlim(min_mi, max_mi)
    ax2.set_title("Bifurkacja Y")

    x = np.copy(initial_x)
    y = np.copy(initial_y)

    canvas.draw()


n = 600

a_initial = 5
b_initial = 25
mi_initial = 6


######################
# APP
######################


root = tk.Tk()
root.title('Chaos deterministyczny w prostej sieci neuronowej')

style = ttk.Style()
style.theme_use('aqua')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6), sharex=True)
plt.style.use('ggplot')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

slider_frame = ttk.Frame(root)
slider_frame.pack(side=tk.TOP, pady=20)

a_label = ttk.Label(slider_frame, text='Współczynnik a')
a_label.grid(row=0, column=0)
a_slider = ttk.Scale(slider_frame, from_=1, to=50, orient=tk.HORIZONTAL,
                     length=400, command=lambda val: update_plot(
                        float(val), float(b_slider.get()), float(mi_slider.get())))
a_slider.set(a_initial)
a_slider.grid(row=0, column=1)

b_label = ttk.Label(slider_frame, text='Współczynnik b')
b_label.grid(row=1, column=0)
b_slider = ttk.Scale(slider_frame, from_=1, to=50, orient=tk.HORIZONTAL,
                     length=400, command=lambda val: update_plot(
                        float(a_slider.get()), float(val), float(mi_slider.get())))
b_slider.set(b_initial)
b_slider.grid(row=1, column=1)

mi_label = ttk.Label(slider_frame, text='Zakres μ')
mi_label.grid(row=2, column=0)
mi_slider = ttk.Scale(slider_frame, from_=1, to=50, orient=tk.HORIZONTAL,
                      length=400, command=lambda val: update_plot(
                        float(a_slider.get()), float(b_slider.get()), float(val)))
mi_slider.set(mi_initial)
mi_slider.grid(row=2, column=1)

update_plot(a_initial, b_initial, mi_initial)

width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width, height))
root.mainloop()
