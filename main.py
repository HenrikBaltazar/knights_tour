import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
import time
import threading
 
from knight_algo import knight_tour, can_have_solution_size, can_have_solution_pos
 
 
class KnightTourApp:
    def __init__(self):
        self.root = ttk.Window(
            title="Passeio do Cavalo -- Knight's Tour",
            themename="cyborg",
            size=(1100, 750),
            resizable=(True, True),
        )
        self.root.minsize(900, 600)
 
        self.board_size = tk.IntVar(value=8)
        self.speed_ms = tk.IntVar(value=100)
        self.start_pos = None
        self.is_running = False
        self.is_paused = False
        self.result = None
        self.current_step = 0
        self.anim_thread = None
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.cells = {}
 
        self._build_ui()
        self._draw_board()
 
        self.board_size.trace_add("write", lambda *_: self._on_size_change())
 
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=BOTH, expand=True)
 
        header = ttk.Frame(main)
        header.pack(fill=X, pady=(0, 10))
        ttk.Label(
            header,
            text="PASSEIO DO CAVALO",
            font=("Consolas", 18, "bold"),
            bootstyle="info",
        ).pack(side=LEFT)
        ttk.Label(
            header,
            text="M3: Modelagem por Grafos (DFS)",
            font=("Consolas", 9),
            bootstyle="secondary",
        ).pack(side=LEFT, padx=(12, 0), pady=(6, 0))
 
        content = ttk.Frame(main)
        content.pack(fill=BOTH, expand=True)
 
        board_frame = ttk.Labelframe(content, text="Tabuleiro", bootstyle="info", padding=8)
        board_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
 
        self.canvas = tk.Canvas(board_frame, bg="#1a1a2e", highlightthickness=0, cursor="hand2")
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw_board())
        self.canvas.bind("<Button-1>", self._on_canvas_click)
 
        sidebar = ttk.Frame(content, width=280)
        sidebar.pack(side=RIGHT, fill=Y)
        sidebar.pack_propagate(False)
 
        ctrl = ttk.Labelframe(sidebar, text="Controles", bootstyle="info", padding=12)
        ctrl.pack(fill=X, pady=(0, 8))
 
        ttk.Label(ctrl, text="Tamanho do Tabuleiro", font=("Consolas", 9)).pack(anchor=W)
        size_frame = ttk.Frame(ctrl)
        size_frame.pack(fill=X, pady=(2, 8))
        self.size_label = ttk.Label(size_frame, text="8 x 8", font=("Consolas", 11, "bold"), bootstyle="info")
        self.size_label.pack(side=RIGHT)
        ttk.Scale(
            size_frame, from_=5, to=100, variable=self.board_size,
            bootstyle="info", command=lambda _: self._update_size_label(),
        ).pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
 
        ttk.Label(ctrl, text="Velocidade da Animacao", font=("Consolas", 9)).pack(anchor=W)
        speed_frame = ttk.Frame(ctrl)
        speed_frame.pack(fill=X, pady=(2, 8))
        self.speed_label = ttk.Label(speed_frame, text="100 ms", font=("Consolas", 11, "bold"), bootstyle="info")
        self.speed_label.pack(side=RIGHT)
        ttk.Scale(
            speed_frame, from_=0, to=500, variable=self.speed_ms,
            bootstyle="info", command=lambda _: self._update_speed_label(),
        ).pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
 
        self.pos_label = ttk.Label(ctrl, text="Posicao: clique no tabuleiro", font=("Consolas", 9), bootstyle="warning")
        self.pos_label.pack(anchor=W, pady=(0, 8))
 
        btn_frame = ttk.Frame(ctrl)
        btn_frame.pack(fill=X)
        self.start_btn = ttk.Button(btn_frame, text="Iniciar", bootstyle="info", command=self._on_start, width=12)
        self.start_btn.pack(side=LEFT, expand=True, fill=X, padx=(0, 4))
        self.pause_btn = ttk.Button(btn_frame, text="Pausar", bootstyle="warning", command=self._on_pause, width=12, state=DISABLED)
        self.pause_btn.pack(side=LEFT, expand=True, fill=X, padx=(0, 4))
        ttk.Button(btn_frame, text="Reset", bootstyle="danger-outline", command=self._on_reset, width=8).pack(side=LEFT)
 
        self.warn_label = ttk.Label(ctrl, text="", font=("Consolas", 8), bootstyle="danger", wraplength=240)
        self.warn_label.pack(anchor=W, pady=(6, 0))
 
        stats = ttk.Labelframe(sidebar, text="Estatisticas", bootstyle="info", padding=12)
        stats.pack(fill=X, pady=(0, 8))
 
        stat_items = [
            ("Tempo de Execucao", "exec_time", "0.00 ms"),
            ("Passo Atual", "step", "0 / 64"),
            ("Estratégia", "strategy", "-"),
        ]
        self.stat_labels = {}
        for label_text, key, default in stat_items:
            f = ttk.Frame(stats)
            f.pack(fill=X, pady=2)
            ttk.Label(f, text=label_text, font=("Consolas", 8), bootstyle="secondary").pack(anchor=W)
            lbl = ttk.Label(f, text=default, font=("Consolas", 11, "bold"))
            lbl.pack(anchor=W)
            self.stat_labels[key] = lbl
 
        self.status_frame = ttk.Frame(stats)
        self.status_frame.pack(fill=X, pady=(8, 0))
        self.status_dot = ttk.Label(self.status_frame, text="[o]", font=("Consolas", 10), bootstyle="secondary")
        self.status_dot.pack(side=LEFT)
        self.status_text = ttk.Label(self.status_frame, text=" Parado", font=("Consolas", 9), bootstyle="secondary")
        self.status_text.pack(side=LEFT)
 
    def _update_size_label(self):
        n = int(self.board_size.get())
        self.size_label.config(text=f"{n} x {n}")
 
    def _update_speed_label(self):
        self.speed_label.config(text=f"{int(self.speed_ms.get())} ms")
 
    def _cell_size(self):
        n = int(self.board_size.get())
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        return min(w // n, h // n, 72) if w > 1 and h > 1 else 50
 
    def _draw_board(self):
        self.canvas.delete("all")
        self.cells.clear()
        n = int(self.board_size.get())
        cs = self._cell_size()
        total_w = cs * n
        total_h = cs * n
        ox = (self.canvas.winfo_width() - total_w) // 2
        oy = (self.canvas.winfo_height() - total_h) // 2
        ox = max(ox, 2)
        oy = max(oy, 2)
 
        for r in range(n):
            for c in range(n):
                x1 = ox + c * cs
                y1 = oy + r * cs
                x2 = x1 + cs
                y2 = y1 + cs
                dark = (r + c) % 2 == 1
                fill = "#0f0f23" if dark else "#16213e"
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#1a1a3e", width=1)
                
                font_sz = max(cs // 4, 6)
                txt = self.canvas.create_text(
                    x1 + cs // 2, y1 + cs // 2, text="", fill="#e0e0e0",
                    font=("Consolas", font_sz, "bold"),
                )
                self.cells[(r, c)] = (rect, txt)
 
        if self.start_pos and not self.result:
            r, c = self.start_pos
            if (r, c) in self.cells:
                rect, txt = self.cells[(r, c)]
                self.canvas.itemconfig(rect, fill="#0d7377", outline="#00fff5", width=2)
                self.canvas.itemconfig(txt, text="K", font=("Consolas", max(cs // 2, 10), "bold"))
 
    def _on_canvas_click(self, event):
        if self.is_running:
            return
        n = int(self.board_size.get())
        cs = self._cell_size()
        total_w = cs * n
        total_h = cs * n
        ox = (self.canvas.winfo_width() - total_w) // 2
        oy = (self.canvas.winfo_height() - total_h) // 2
        ox = max(ox, 2)
        oy = max(oy, 2)
 
        col = (event.x - ox) // cs
        row = (event.y - oy) // cs
        if 0 <= row < n and 0 <= col < n:
            self.start_pos = (row, col)
            self.result = None
            self.current_step = 0
            self.pos_label.config(text=f"Posicao: ({row}, {col})", bootstyle="info")
            self._draw_board()
 
            if not can_have_solution_size(n):
                self.warn_label.config(text=f"Tabuleiros {n}x{n} nao possuem solucao.")
                self.start_btn.config(state=DISABLED)
            elif not can_have_solution_pos(n, row, col):
                self.warn_label.config(text=f"Posicao: {row},{col} em um tabuleiro {n}x{n} nao possui solucao (paridade).")
                self.start_btn.config(state=DISABLED)
            else:
                self.warn_label.config(text="")
                self.start_btn.config(state=NORMAL)
 
    def _on_size_change(self):
        self._on_reset()
        self._draw_board()
 
    def _on_start(self):
        if not self.start_pos:
            Messagebox.show_warning("Clique em uma casa do tabuleiro primeiro!", "Posicao Inicial")
            return
 
        if self.is_paused:
            self.is_paused = False
            self.pause_event.set()
            self.start_btn.config(text="Iniciar", state=DISABLED)
            self.pause_btn.config(state=NORMAL)
            self._set_status(True)
            return
 
        n = int(self.board_size.get())
        r, c = self.start_pos
 
        self.start_btn.config(state=DISABLED)
        self.pause_btn.config(state=DISABLED)
        self._set_status(True)
 
        def solve_and_animate():
            success, board, path, exec_time, strategy = knight_tour(n, r, c)
            self.result = (success, board, path, exec_time)
            self.root.after(0, lambda: self._after_solve(success, board, path, exec_time, n, strategy))
 
        threading.Thread(target=solve_and_animate, daemon=True).start()
 
    def _after_solve(self, success, board, path, exec_time, n, strategy):
        self.stat_labels["exec_time"].config(text=f"{exec_time:.2f} ms")
        self.stat_labels["strategy"].config(text=strategy)
        self.stat_labels["step"].config(text=f"0 / {n * n}")
 
        if not success:
            Messagebox.show_error(
                f"Nenhuma solucao encontrada para {n}x{n} partindo de ({self.start_pos[0]}, {self.start_pos[1]}).",
                "Sem Solucao",
            )
            self.start_btn.config(state=NORMAL)
            self._set_status(False)
            return
 
        self.is_running = True
        self.is_paused = False
        self.stop_event.clear()
        self.pause_event.set()
        self.pause_btn.config(state=NORMAL)
        self._animate(path, n)
 
    def _animate(self, path, n):
        def run():
            cs = self._cell_size()
            for i, (r, c) in enumerate(path):
                if self.stop_event.is_set():
                    return
                self.pause_event.wait()
 
                self.current_step = i + 1
 
                def update(row=r, col=c, step=i + 1):
                    if (row, col) not in self.cells:
                        return
                    rect, txt = self.cells[(row, col)]
                    progress = step / (n * n)
                    red = int(13 + progress * 130)
                    green = int(115 - progress * 80)
                    blue = int(119 + progress * 100)
                    fill = f"#{red:02x}{green:02x}{blue:02x}"
                    self.canvas.itemconfig(rect, fill=fill, outline="#00fff5", width=1)
                    
                    font_sz = max(cs // 4, 6)
                    self.canvas.itemconfig(txt, text=str(step), font=("Consolas", font_sz, "bold"))
 
                    if step == self.current_step:
                        self.canvas.itemconfig(rect, outline="#00fff5", width=2)
 
                    self.stat_labels["step"].config(text=f"{step} / {n * n}")
 
                self.root.after(0, update)
                time.sleep(self.speed_ms.get() / 1000)
 
            def finish():
                self.is_running = False
                self.start_btn.config(text="Iniciar", state=NORMAL)
                self.pause_btn.config(state=DISABLED)
                self._set_status(False)
                Messagebox.show_info("Passeio completo! Todas as casas foram visitadas.", "Sucesso!")
 
            self.root.after(0, finish)
 
        self.anim_thread = threading.Thread(target=run, daemon=True)
        self.anim_thread.start()
 
    def _on_pause(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_event.clear()
            self.start_btn.config(text="Retomar", state=NORMAL)
            self.pause_btn.config(state=DISABLED)
            self._set_status(False)
        elif self.is_paused:
            self.is_paused = False
            self.pause_event.set()
            self.start_btn.config(state=DISABLED)
            self.pause_btn.config(state=NORMAL)
            self._set_status(True)
 
    def _on_reset(self):
        self.stop_event.set()
        self.pause_event.set()
        self.is_running = False
        self.is_paused = False
        self.current_step = 0
        self.result = None
        self.start_pos = None
        self.start_btn.config(text="Iniciar", state=NORMAL)
        self.pause_btn.config(state=DISABLED)
        self.pos_label.config(text="Posicao: clique no tabuleiro", bootstyle="warning")
        self.warn_label.config(text="")
        self.stat_labels["exec_time"].config(text="0.00 ms")
        self.stat_labels["strategy"].config(text="-")
        n = int(self.board_size.get())
        self.stat_labels["step"].config(text=f"0 / {n * n}")
        self._set_status(False)
        self._draw_board()
 
    def _set_status(self, running: bool):
        if running:
            self.status_dot.config(text="[o]", bootstyle="success")
            self.status_text.config(text=" Executando...", bootstyle="success")
        else:
            self.status_dot.config(text="[o]", bootstyle="secondary")
            self.status_text.config(text=" Parado", bootstyle="secondary")
 
    def run(self):
        self.root.mainloop()
 
if __name__ == "__main__":
    app = KnightTourApp()
    app.run()
