import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class RoundedCanvas(tk.Canvas):
    def round_rect(self, x1, y1, x2, y2, r=20, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class SmartParkingFSMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akıllı Otopark Otomata Simülasyonu")
        self.root.geometry("1280x780")
        self.root.minsize(1160, 720)

        self.colors = {
            "bg": "#07111F",
            "panel": "#0F172A",
            "panel2": "#111C31",
            "panel3": "#172033",
            "card": "#1E293B",
            "card2": "#243247",
            "line": "#334155",
            "text": "#F8FAFC",
            "muted": "#94A3B8",
            "soft": "#CBD5E1",
            "cyan": "#38BDF8",
            "blue": "#60A5FA",
            "green": "#22C55E",
            "red": "#EF4444",
            "yellow": "#F59E0B",
            "purple": "#A78BFA",
            "pink": "#F472B6",
            "orange": "#FB923C",
            "dark": "#020617",
            "white": "#FFFFFF",
        }

        self.operation_var = tk.StringVar(value="Giriş")
        self.plate_var = tk.StringVar(value="16 ABC 123")
        self.plate_read_var = tk.BooleanVar(value=True)
        self.subscriber_var = tk.BooleanVar(value=True)
        self.payment_var = tk.BooleanVar(value=False)
        self.capacity_var = tk.StringVar(value="12")
        self.current_var = tk.StringVar(value="5")

        self.summary_vars = {
            "system": tk.StringVar(value="Hazır"),
            "plate": tk.StringVar(value="Bekliyor"),
            "barrier": tk.StringVar(value="Kapalı"),
            "result": tk.StringVar(value="Simülasyon bekleniyor"),
            "occupancy": tk.StringVar(value="5/12"),
        }

        self.current_path = []
        self.current_outcome = "idle"

        self.configure_styles()
        self.build_ui()
        self.draw_parking_scene("idle")
        self.draw_fsm_diagram([])
        self.write_welcome_log()

    def configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TCombobox",
            fieldbackground=self.colors["card"],
            background=self.colors["card"],
            foreground=self.colors["text"],
            arrowcolor=self.colors["cyan"],
            bordercolor=self.colors["line"],
            lightcolor=self.colors["line"],
            darkcolor=self.colors["line"],
            padding=6,
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.colors["card"])],
            foreground=[("readonly", self.colors["text"])],
        )

        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=self.colors["card"],
            background=self.colors["cyan"],
            bordercolor=self.colors["card"],
            lightcolor=self.colors["cyan"],
            darkcolor=self.colors["cyan"],
        )

    def build_ui(self):
        self.build_header()

        shell = tk.Frame(self.root, bg=self.colors["bg"])
        shell.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.left = tk.Frame(shell, bg=self.colors["panel"], width=330)
        self.left.pack(side="left", fill="y", padx=(0, 14))
        self.left.pack_propagate(False)

        self.right = tk.Frame(shell, bg=self.colors["bg"])
        self.right.pack(side="right", fill="both", expand=True)

        self.build_control_panel()
        self.build_summary_cards()
        self.build_main_panels()

    def build_header(self):
        header = tk.Frame(self.root, bg=self.colors["bg"])
        header.pack(fill="x", padx=18, pady=16)

        left = tk.Frame(header, bg=self.colors["bg"])
        left.pack(side="left")

        tk.Label(
            left,
            text="AKILLI OTOPARK OTOMATA SİMÜLASYONU",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Segoe UI", 23, "bold"),
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Manuel durum seçimi • Bariyer kontrolü • Açık durum geçiş ekranı",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 0))

        badge_box = tk.Frame(header, bg=self.colors["bg"])
        badge_box.pack(side="right")

        self.clock_label = tk.Label(
            badge_box,
            text=datetime.now().strftime("%H:%M"),
            bg=self.colors["bg"],
            fg=self.colors["cyan"],
            font=("Segoe UI", 18, "bold"),
        )
        self.clock_label.pack(anchor="e")

        tk.Label(
            badge_box,
            text="FINITE STATE MACHINE",
            bg=self.colors["cyan"],
            fg=self.colors["dark"],
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=6,
        ).pack(anchor="e", pady=(4, 0))

        self.tick_clock()

    def tick_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.tick_clock)

    def panel_title(self, parent, title, subtitle=None):
        tk.Label(
            parent,
            text=title,
            bg=parent["bg"],
            fg=self.colors["text"],
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w", padx=20, pady=(18, 2))

        if subtitle:
            tk.Label(
                parent,
                text=subtitle,
                bg=parent["bg"],
                fg=self.colors["muted"],
                font=("Segoe UI", 9),
                wraplength=285,
                justify="left",
            ).pack(anchor="w", padx=20, pady=(0, 14))

    def input_label(self, text):
        tk.Label(
            self.left,
            text=text,
            bg=self.colors["panel"],
            fg=self.colors["soft"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=20, pady=(10, 5))

    def build_control_panel(self):
        self.panel_title(
            self.left,
            "Kontrol Paneli",
            "Kullanıcının girdiği değerlere göre otomata hangi durumdan hangi duruma geçeceğini hesaplar.",
        )

        self.input_label("İşlem Türü")
        op = ttk.Combobox(
            self.left,
            textvariable=self.operation_var,
            values=["Giriş", "Çıkış"],
            state="readonly",
            width=28,
            font=("Segoe UI", 10),
        )
        op.pack(fill="x", padx=20, ipady=2)

        self.input_label("Plaka")
        tk.Entry(
            self.left,
            textvariable=self.plate_var,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 12, "bold"),
        ).pack(fill="x", padx=20, ipady=10)

        check_box = tk.Frame(self.left, bg=self.colors["panel"])
        check_box.pack(fill="x", padx=18, pady=(12, 8))

        self.modern_check(check_box, "Plaka okunabildi", self.plate_read_var)
        self.modern_check(check_box, "Araç abone", self.subscriber_var)
        self.modern_check(check_box, "Ödeme yapıldı", self.payment_var)

        number_row = tk.Frame(self.left, bg=self.colors["panel"])
        number_row.pack(fill="x", padx=20, pady=(8, 10))

        cap_box = tk.Frame(number_row, bg=self.colors["panel"])
        cap_box.pack(side="left", fill="x", expand=True, padx=(0, 6))

        cur_box = tk.Frame(number_row, bg=self.colors["panel"])
        cur_box.pack(side="left", fill="x", expand=True, padx=(6, 0))

        tk.Label(
            cap_box,
            text="Kapasite",
            bg=self.colors["panel"],
            fg=self.colors["soft"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        tk.Entry(
            cap_box,
            textvariable=self.capacity_var,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            justify="center",
        ).pack(fill="x", pady=(5, 0), ipady=9)

        tk.Label(
            cur_box,
            text="Mevcut",
            bg=self.colors["panel"],
            fg=self.colors["soft"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        tk.Entry(
            cur_box,
            textvariable=self.current_var,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            justify="center",
        ).pack(fill="x", pady=(5, 0), ipady=9)

        tk.Button(
            self.left,
            text="▶ Simülasyonu Çalıştır",
            command=self.run_simulation,
            bg=self.colors["green"],
            fg="#052E16",
            activebackground="#16A34A",
            activeforeground=self.colors["white"],
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        ).pack(fill="x", padx=20, pady=(15, 8), ipady=12)

        quick = tk.Frame(self.left, bg=self.colors["panel"])
        quick.pack(fill="x", padx=20, pady=(0, 8))

        tk.Button(
            quick,
            text="Başarılı Giriş",
            command=lambda: self.load_scenario("success_entry"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            activebackground=self.colors["card2"],
            activeforeground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=4)

        tk.Button(
            quick,
            text="Plaka Hatası",
            command=lambda: self.load_scenario("plate_error"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            activebackground=self.colors["card2"],
            activeforeground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).grid(row=0, column=1, sticky="ew", padx=(4, 0), pady=4)

        tk.Button(
            quick,
            text="Otopark Dolu",
            command=lambda: self.load_scenario("full"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            activebackground=self.colors["card2"],
            activeforeground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=4)

        tk.Button(
            quick,
            text="Ödeme İhlali",
            command=lambda: self.load_scenario("payment_error"),
            bg=self.colors["card"],
            fg=self.colors["text"],
            activebackground=self.colors["card2"],
            activeforeground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=4)

        quick.grid_columnconfigure(0, weight=1)
        quick.grid_columnconfigure(1, weight=1)

        tk.Button(
            self.left,
            text="Ekranı Temizle",
            command=self.reset_screen,
            bg=self.colors["panel3"],
            fg=self.colors["text"],
            activebackground=self.colors["card2"],
            activeforeground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(fill="x", padx=20, pady=(2, 8), ipady=9)

        tk.Button(
            self.left,
            text="Programdan Çık",
            command=self.root.destroy,
            bg=self.colors["red"],
            fg="#450A0A",
            activebackground="#DC2626",
            activeforeground=self.colors["white"],
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(fill="x", padx=20, pady=(0, 12), ipady=9)

    def modern_check(self, parent, text, variable):
        tk.Checkbutton(
            parent,
            text=text,
            variable=variable,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            selectcolor=self.colors["card"],
            activebackground=self.colors["panel"],
            activeforeground=self.colors["text"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=3)

    def build_summary_cards(self):
        top = tk.Frame(self.right, bg=self.colors["bg"])
        top.pack(fill="x")

        items = [
            ("Sistem", "system", self.colors["cyan"]),
            ("Plaka", "plate", self.colors["blue"]),
            ("Bariyer", "barrier", self.colors["orange"]),
            ("Sonuç", "result", self.colors["green"]),
            ("Doluluk", "occupancy", self.colors["purple"]),
        ]

        for i, (title, key, accent) in enumerate(items):
            card = tk.Frame(top, bg=self.colors["panel"], height=86)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 9, 0))
            top.grid_columnconfigure(i, weight=1)
            card.grid_propagate(False)

            tk.Frame(card, bg=accent, height=4).pack(fill="x")

            tk.Label(
                card,
                text=title,
                bg=self.colors["panel"],
                fg=self.colors["muted"],
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w", padx=12, pady=(10, 2))

            tk.Label(
                card,
                textvariable=self.summary_vars[key],
                bg=self.colors["panel"],
                fg=self.colors["text"],
                font=("Segoe UI", 13, "bold"),
            ).pack(anchor="w", padx=12)

    def build_main_panels(self):
        upper = tk.Frame(self.right, bg=self.colors["bg"])
        upper.pack(fill="both", expand=True, pady=(14, 14))

        self.visual_panel = tk.Frame(upper, bg=self.colors["panel"])
        self.visual_panel.pack(side="left", fill="both", expand=True, padx=(0, 14))
        self.visual_panel.configure(width=430)

        self.fsm_panel = tk.Frame(upper, bg=self.colors["panel"])
        self.fsm_panel.pack(side="right", fill="both", expand=True)
        self.fsm_panel.configure(width=610)

        self.build_visual_panel()
        self.build_fsm_panel()
        self.build_transition_log()

    def section_header(self, parent, title, subtitle):
        box = tk.Frame(parent, bg=parent["bg"])
        box.pack(fill="x", padx=16, pady=(14, 8))

        tk.Label(
            box,
            text=title,
            bg=parent["bg"],
            fg=self.colors["text"],
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")

        tk.Label(
            box,
            text=subtitle,
            bg=parent["bg"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(2, 0))

    def build_visual_panel(self):
        self.section_header(
            self.visual_panel,
            "Canlı Otopark Ekranı",
            "Araç, bariyer ve doluluk durumu görsel olarak gösterilir.",
        )

        self.parking_canvas = RoundedCanvas(
            self.visual_panel,
            bg=self.colors["panel2"],
            highlightthickness=0,
            height=285,
        )
        self.parking_canvas.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def build_fsm_panel(self):
        self.section_header(
            self.fsm_panel,
            "Durum Geçiş Ekranı",
            "Geçilen durumlar parlak renkle vurgulanır; geçiş koşulları okların üzerinde görünür.",
        )

        self.fsm_canvas = RoundedCanvas(
            self.fsm_panel,
            bg=self.colors["panel2"],
            highlightthickness=0,
            height=335,
        )
        self.fsm_canvas.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def build_transition_log(self):
        bottom = tk.Frame(self.right, bg=self.colors["panel"])
        bottom.pack(fill="both", expand=True)

        header = tk.Frame(bottom, bg=self.colors["panel"])
        header.pack(fill="x", padx=16, pady=(14, 8))

        tk.Label(
            header,
            text="Açık Durum Geçiş Listesi",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")

        self.progress = ttk.Progressbar(
            header,
            orient="horizontal",
            length=260,
            mode="determinate",
            maximum=100,
            style="Horizontal.TProgressbar",
        )
        self.progress.pack(side="right", pady=6)

        self.transition_text = tk.Text(
            bottom,
            bg=self.colors["dark"],
            fg=self.colors["soft"],
            insertbackground=self.colors["text"],
            relief="flat",
            font=("Consolas", 10),
            padx=14,
            pady=12,
            height=10,
        )
        self.transition_text.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.transition_text.tag_config("title", foreground=self.colors["white"], font=("Consolas", 11, "bold"))
        self.transition_text.tag_config("info", foreground=self.colors["cyan"])
        self.transition_text.tag_config("success", foreground=self.colors["green"])
        self.transition_text.tag_config("warning", foreground=self.colors["yellow"])
        self.transition_text.tag_config("danger", foreground=self.colors["red"])
        self.transition_text.tag_config("normal", foreground=self.colors["soft"])

    def parse_numbers(self):
        try:
            capacity = int(self.capacity_var.get().strip())
            current = int(self.current_var.get().strip())
        except ValueError:
            messagebox.showerror("Hata", "Kapasite ve mevcut araç sayısı sayı olmalıdır.")
            return None, None

        if capacity <= 0:
            messagebox.showerror("Hata", "Kapasite 0'dan büyük olmalıdır.")
            return None, None

        if current < 0:
            messagebox.showerror("Hata", "Mevcut araç sayısı negatif olamaz.")
            return None, None

        return capacity, current

    def run_simulation(self):
        capacity, current = self.parse_numbers()
        if capacity is None:
            return

        operation = self.operation_var.get()
        plate = self.plate_var.get().strip().upper()
        plate_read = self.plate_read_var.get()
        subscriber = self.subscriber_var.get()
        payment = self.payment_var.get()

        transitions = []
        log_lines = []

        def add(step, state, condition, output, tag="normal"):
            transitions.append(
                {
                    "step": step,
                    "state": state,
                    "condition": condition,
                    "output": output,
                    "tag": tag,
                }
            )

        if operation == "Giriş":
            add("1", "S0", "Başlat", "Sistem giriş işlemi için hazırlandı.", "info")
            add("2", "S1", "Araç algılandı", "Araç giriş noktasına geldi.", "info")
            add("3", "S2", "Kamera aktif", "Plaka okuma işlemi başlatıldı.", "info")

            if not plate_read or plate == "":
                add("4", "S_RED", "Plaka okunamadı", "Bariyer kapalı kaldı, giriş reddedildi.", "danger")
                outcome = "danger"
                result = "Giriş reddedildi"
                path = ["S0", "S1", "S2", "S_RED"]
                self.summary_vars["system"].set("Reddedildi")
                self.summary_vars["plate"].set("Okunamadı")
                self.summary_vars["barrier"].set("Kapalı")
                self.summary_vars["result"].set("Giriş yok")

            elif current >= capacity:
                add("4", "S3", f"Plaka: {plate}", "Plaka başarıyla okundu.", "success")
                add("5", "S_DOLU", "Mevcut araç ≥ kapasite", "Otopark dolu, giriş iptal edildi.", "warning")
                outcome = "warning"
                result = "Otopark dolu"
                path = ["S0", "S1", "S2", "S3", "S_DOLU"]
                self.summary_vars["system"].set("Dolu")
                self.summary_vars["plate"].set("Okundu")
                self.summary_vars["barrier"].set("Kapalı")
                self.summary_vars["result"].set("Giriş iptal")

            else:
                add("4", "S3", f"Plaka: {plate}", "Plaka başarıyla okundu.", "success")
                add("5", "S4", f"{current} < {capacity}", "Otoparkta boş yer bulundu.", "success")
                if subscriber:
                    add("6", "S5", "Araç abone", "Abonelik doğrulandı.", "success")
                else:
                    add("6", "S5", "Araç abone değil", "Misafir araç kaydı oluşturuldu.", "warning")
                add("7", "S6", "Giriş izni verildi", "Bariyer açıldı.", "success")
                add("8", "S7", "Araç geçti", "Araç otoparka giriş yaptı.", "success")
                current += 1
                self.current_var.set(str(current))
                outcome = "success"
                result = "Giriş başarılı"
                path = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"]
                self.summary_vars["system"].set("Aktif")
                self.summary_vars["plate"].set("Okundu")
                self.summary_vars["barrier"].set("Açık")
                self.summary_vars["result"].set("Giriş başarılı")

        else:
            add("1", "S0", "Başlat", "Sistem çıkış işlemi için hazırlandı.", "info")
            add("2", "S1", "Araç algılandı", "Araç çıkış noktasına geldi.", "info")
            add("3", "S2", "Kamera aktif", "Plaka okuma işlemi başlatıldı.", "info")

            if not plate_read or plate == "":
                add("4", "S_RED", "Plaka okunamadı", "Bariyer kapalı kaldı, çıkış reddedildi.", "danger")
                outcome = "danger"
                result = "Çıkış reddedildi"
                path = ["S0", "S1", "S2", "S_RED"]
                self.summary_vars["system"].set("Reddedildi")
                self.summary_vars["plate"].set("Okunamadı")
                self.summary_vars["barrier"].set("Kapalı")
                self.summary_vars["result"].set("Çıkış yok")

            elif subscriber:
                add("4", "S3", f"Plaka: {plate}", "Plaka başarıyla okundu.", "success")
                add("5", "S5", "Araç abone", "Ödeme gerekmeden çıkış izni verildi.", "success")
                add("6", "S6", "Çıkış izni verildi", "Bariyer açıldı.", "success")
                add("7", "S7", "Araç geçti", "Araç otoparktan çıkış yaptı.", "success")
                current = max(0, current - 1)
                self.current_var.set(str(current))
                outcome = "success"
                result = "Çıkış başarılı"
                path = ["S0", "S1", "S2", "S3", "S5", "S6", "S7"]
                self.summary_vars["system"].set("Aktif")
                self.summary_vars["plate"].set("Okundu")
                self.summary_vars["barrier"].set("Açık")
                self.summary_vars["result"].set("Çıkış başarılı")

            else:
                add("4", "S3", f"Plaka: {plate}", "Plaka başarıyla okundu.", "success")
                add("5", "S5", "Araç abone değil", "Ödeme kontrolüne geçildi.", "warning")
                if payment:
                    add("6", "S6", "Ödeme yapıldı", "Bariyer açıldı.", "success")
                    add("7", "S7", "Araç geçti", "Araç otoparktan çıkış yaptı.", "success")
                    current = max(0, current - 1)
                    self.current_var.set(str(current))
                    outcome = "success"
                    result = "Çıkış başarılı"
                    path = ["S0", "S1", "S2", "S3", "S5", "S6", "S7"]
                    self.summary_vars["system"].set("Aktif")
                    self.summary_vars["plate"].set("Okundu")
                    self.summary_vars["barrier"].set("Açık")
                    self.summary_vars["result"].set("Çıkış başarılı")
                else:
                    add("6", "S_IHLAL", "Ödeme yapılmadı", "İhlal kaydı oluşturuldu, bariyer kapalı kaldı.", "danger")
                    outcome = "danger"
                    result = "Ödeme ihlali"
                    path = ["S0", "S1", "S2", "S3", "S5", "S_IHLAL"]
                    self.summary_vars["system"].set("İhlal")
                    self.summary_vars["plate"].set("Okundu")
                    self.summary_vars["barrier"].set("Kapalı")
                    self.summary_vars["result"].set("Çıkış yok")

        self.summary_vars["occupancy"].set(f"{current}/{capacity}")
        self.progress["value"] = min(100, int((current / capacity) * 100))

        self.current_path = path
        self.current_outcome = outcome

        log_lines.append(("DURUM GEÇİŞ RAPORU", "title"))
        log_lines.append((f"Sonuç: {result}", "info"))
        log_lines.append(("-" * 95, "normal"))
        log_lines.append((f"{'Adım':<6}{'Durum':<12}{'Koşul / Girdi':<30}Çıktı", "title"))
        log_lines.append(("-" * 95, "normal"))

        for t in transitions:
            line = f"{t['step']:<6}{t['state']:<12}{t['condition']:<30}{t['output']}"
            log_lines.append((line, t["tag"]))

        log_lines.append(("-" * 95, "normal"))
        log_lines.append((f"Geçilen durum yolu: {' → '.join(path)}", "info"))

        self.write_log(log_lines)
        self.draw_parking_scene(outcome)
        self.draw_fsm_diagram(path)

    def write_log(self, lines):
        self.transition_text.delete("1.0", tk.END)
        for text, tag in lines:
            self.transition_text.insert(tk.END, text + "\n", tag)
        self.transition_text.see(tk.END)

    def write_welcome_log(self):
        lines = [
            ("KULLANIM", "title"),
            ("1. Sol panelden işlem türünü ve araç bilgilerini seç.", "normal"),
            ("2. Simülasyonu Çalıştır butonuna bas.", "normal"),
            ("3. Sağ üstteki Durum Geçiş Ekranı üzerinde aktif durum yolunu izle.", "normal"),
            ("4. Alttaki listede her geçişin koşulu ve çıktısı açıkça gösterilir.", "normal"),
        ]
        self.write_log(lines)

    def draw_parking_scene(self, outcome):
        c = self.colors
        canvas = self.parking_canvas
        canvas.delete("all")

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 200:
            w = 500
        if h < 200:
            h = 285

        capacity, current = self.parse_numbers()
        if capacity is None:
            capacity, current = 10, 0

        canvas.create_rectangle(0, 0, w, h, fill=c["panel2"], outline="")

        # Background glow
        for i, color in enumerate(["#0B2440", "#0A1C33", "#091728"]):
            canvas.create_oval(40 - i * 20, 10 - i * 25, w * 0.75 + i * 40, h * 0.92 + i * 30, fill=color, outline="")

        # Parking building
        canvas.round_rect(24, 38, w - 24, h - 28, 22, fill="#0B1220", outline=c["line"], width=2)
        canvas.create_text(50, 60, text="SMART PARKING", anchor="w", fill=c["cyan"], font=("Segoe UI", 11, "bold"))

        # Road
        road_y1 = h - 82
        road_y2 = h - 40
        canvas.create_rectangle(42, road_y1, w - 42, road_y2, fill="#111827", outline="")
        for x in range(60, int(w - 70), 72):
            canvas.create_line(x, (road_y1 + road_y2) // 2, x + 34, (road_y1 + road_y2) // 2, fill="#64748B", width=2)

        # Parking slots
        max_slots = min(12, capacity)
        start_x = 58
        start_y = 92
        slot_w = max(38, min(58, (w - 130) / max_slots - 8))
        gap = 8
        for i in range(max_slots):
            x1 = start_x + i * (slot_w + gap)
            x2 = x1 + slot_w
            filled = i < min(current, max_slots)
            color = c["orange"] if filled else c["green"]
            canvas.round_rect(x1, start_y, x2, start_y + 54, 8, fill="#111827", outline=color, width=2)
            canvas.create_text((x1 + x2) / 2, start_y + 18, text=str(i + 1), fill=c["muted"], font=("Segoe UI", 8, "bold"))
            canvas.create_text((x1 + x2) / 2, start_y + 38, text="DOLU" if filled else "BOŞ", fill=color, font=("Segoe UI", 8, "bold"))

        # Barrier
        barrier_x = 96
        barrier_y = road_y1 - 18
        barrier_color = c["green"] if outcome == "success" else c["red"]
        canvas.create_rectangle(barrier_x, barrier_y, barrier_x + 13, road_y2 + 6, fill=barrier_color, outline="")
        if outcome == "success":
            canvas.create_line(barrier_x + 8, barrier_y + 10, barrier_x + 80, barrier_y - 25, fill=barrier_color, width=8)
            barrier_label = "BARİYER AÇIK"
        else:
            canvas.create_line(barrier_x + 8, barrier_y + 10, barrier_x + 92, barrier_y + 10, fill=barrier_color, width=8)
            barrier_label = "BARİYER KAPALI"
        canvas.create_text(barrier_x + 55, barrier_y + 45, text=barrier_label, fill=barrier_color, font=("Segoe UI", 10, "bold"))

        # Car
        car_color = {"success": c["green"], "warning": c["yellow"], "danger": c["red"], "idle": c["cyan"]}.get(outcome, c["cyan"])
        car_x = 170 if outcome == "success" else 54
        car_y = road_y1 + 8
        canvas.round_rect(car_x, car_y, car_x + 86, car_y + 26, 8, fill=car_color, outline="")
        canvas.round_rect(car_x + 18, car_y - 18, car_x + 62, car_y + 4, 8, fill=car_color, outline="")
        canvas.create_oval(car_x + 12, car_y + 19, car_x + 30, car_y + 37, fill=c["dark"], outline="")
        canvas.create_oval(car_x + 58, car_y + 19, car_x + 76, car_y + 37, fill=c["dark"], outline="")
        canvas.create_text(car_x + 43, car_y + 12, text="ARAÇ", fill=c["dark"], font=("Segoe UI", 8, "bold"))

        # Result plate
        ratio = 0 if capacity == 0 else min(1, current / capacity)
        canvas.round_rect(w - 190, 50, w - 48, 92, 14, fill="#111827", outline=c["line"], width=1)
        canvas.create_text(w - 178, 65, text="DOLULUK", anchor="w", fill=c["muted"], font=("Segoe UI", 8, "bold"))
        canvas.create_text(w - 178, 82, text=f"%{int(ratio * 100)}  ({current}/{capacity})", anchor="w", fill=c["text"], font=("Segoe UI", 11, "bold"))

    def draw_fsm_diagram(self, active_path):
        c = self.colors
        canvas = self.fsm_canvas
        canvas.delete("all")

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 200:
            w = 610
        if h < 220:
            h = 335

        canvas.create_rectangle(0, 0, w, h, fill=c["panel2"], outline="")
        canvas.create_text(26, 22, text="Aktif geçiş yolu:", anchor="w", fill=c["muted"], font=("Segoe UI", 9, "bold"))

        path_text = " → ".join(active_path) if active_path else "Henüz çalıştırılmadı"
        canvas.create_text(135, 22, text=path_text, anchor="w", fill=c["cyan"], font=("Segoe UI", 9, "bold"))

        # Bu koordinatlar yüzde tabanlıdır. Böylece pencere daralsa bile diyagram kesilmez.
        nodes = {
            "S0":      (0.08, 0.33, "Başlangıç"),
            "S1":      (0.22, 0.33, "Araç"),
            "S2":      (0.36, 0.33, "Plaka"),
            "S3":      (0.50, 0.33, "Onay"),
            "S_RED":   (0.66, 0.20, "Red"),

            "S4":      (0.22, 0.68, "Doluluk"),
            "S_DOLU":  (0.08, 0.68, "Dolu"),
            "S5":      (0.42, 0.68, "Abone/Ödeme"),
            "S_IHLAL": (0.64, 0.68, "İhlal"),
            "S6":      (0.78, 0.68, "Bariyer"),
            "S7":      (0.92, 0.68, "Bitiş"),
        }

        top_margin = 52
        bottom_margin = 26
        usable_h = h - top_margin - bottom_margin

        def px(rx):
            return int(24 + rx * (w - 48))

        def py(ry):
            return int(top_margin + ry * usable_h)

        edges = [
            ("S0", "S1", "araç"),
            ("S1", "S2", "kamera"),
            ("S2", "S3", "okundu"),
            ("S2", "S_RED", "okunamadı"),
            ("S3", "S4", "giriş"),
            ("S4", "S5", "boş"),
            ("S4", "S_DOLU", "dolu"),
            ("S3", "S5", "çıkış"),
            ("S5", "S6", "onay"),
            ("S5", "S_IHLAL", "ödeme yok"),
            ("S6", "S7", "geçiş"),
        ]

        active_edges = set()
        for i in range(len(active_path) - 1):
            active_edges.add((active_path[i], active_path[i + 1]))

        # Ekran genişliğine göre düğüm boyutunu küçült.
        radius = max(22, min(31, int(w / 22)))
        font_state = max(8, min(10, int(w / 62)))
        font_label = max(6, min(8, int(w / 82)))

        def draw_arrow(a, b, label):
            x1, y1, _ = nodes[a]
            x2, y2, _ = nodes[b]
            x1, y1, x2, y2 = px(x1), py(y1), px(x2), py(y2)

            active = (a, b) in active_edges
            color = c["cyan"] if active else c["line"]
            width = 3 if active else 1

            dx = x2 - x1
            dy = y2 - y1
            dist = max((dx * dx + dy * dy) ** 0.5, 1)

            ax = x1 + dx / dist * radius
            ay = y1 + dy / dist * radius
            bx = x2 - dx / dist * radius
            by = y2 - dy / dist * radius

            canvas.create_line(ax, ay, bx, by, fill=color, width=width, arrow=tk.LAST, arrowshape=(9, 11, 5))

            if active:
                mx, my = (ax + bx) / 2, (ay + by) / 2
                canvas.create_rectangle(mx - 30, my - 18, mx + 30, my - 3, fill=c["panel2"], outline="")
                canvas.create_text(mx, my - 11, text=label, fill=c["cyan"], font=("Segoe UI", 7, "bold"))

        # Önce oklar, sonra düğümler çizilir. Böylece düğümler okların üstünde kalır.
        for a, b, label in edges:
            draw_arrow(a, b, label)

        active_set = set(active_path)
        final_states = {
            "S7": c["green"],
            "S_RED": c["red"],
            "S_DOLU": c["yellow"],
            "S_IHLAL": c["red"],
        }

        for state, (rx, ry, label) in nodes.items():
            x, y = px(rx), py(ry)
            active = state in active_set

            fill = "#0B1220"
            outline = c["line"]
            text_color = c["muted"]

            if active:
                outline = final_states.get(state, c["cyan"])
                fill = "#102033"
                text_color = c["white"]

            if state in final_states and active:
                outline = final_states[state]

            canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=fill,
                outline=outline,
                width=3 if active else 1,
            )

            canvas.create_text(
                x,
                y - 6,
                text=state,
                fill=outline if active else c["soft"],
                font=("Segoe UI", font_state, "bold"),
            )

            canvas.create_text(
                x,
                y + 10,
                text=label,
                fill=text_color,
                font=("Segoe UI", font_label, "bold"),
                width=radius * 2,
            )

    def load_scenario(self, name):
        if name == "success_entry":
            self.operation_var.set("Giriş")
            self.plate_var.set("16 ABC 123")
            self.plate_read_var.set(True)
            self.subscriber_var.set(True)
            self.payment_var.set(False)
            self.capacity_var.set("12")
            self.current_var.set("5")

        elif name == "plate_error":
            self.operation_var.set("Giriş")
            self.plate_var.set("")
            self.plate_read_var.set(False)
            self.subscriber_var.set(False)
            self.payment_var.set(False)
            self.capacity_var.set("12")
            self.current_var.set("5")

        elif name == "full":
            self.operation_var.set("Giriş")
            self.plate_var.set("34 XYZ 999")
            self.plate_read_var.set(True)
            self.subscriber_var.set(False)
            self.payment_var.set(False)
            self.capacity_var.set("10")
            self.current_var.set("10")

        elif name == "payment_error":
            self.operation_var.set("Çıkış")
            self.plate_var.set("10 TEST 010")
            self.plate_read_var.set(True)
            self.subscriber_var.set(False)
            self.payment_var.set(False)
            self.capacity_var.set("12")
            self.current_var.set("6")

        self.run_simulation()

    def reset_screen(self):
        self.operation_var.set("Giriş")
        self.plate_var.set("16 ABC 123")
        self.plate_read_var.set(True)
        self.subscriber_var.set(True)
        self.payment_var.set(False)
        self.capacity_var.set("12")
        self.current_var.set("5")

        self.summary_vars["system"].set("Hazır")
        self.summary_vars["plate"].set("Bekliyor")
        self.summary_vars["barrier"].set("Kapalı")
        self.summary_vars["result"].set("Simülasyon bekleniyor")
        self.summary_vars["occupancy"].set("5/12")

        self.progress["value"] = 0
        self.current_path = []
        self.current_outcome = "idle"
        self.draw_parking_scene("idle")
        self.draw_fsm_diagram([])
        self.write_welcome_log()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartParkingFSMApp(root)
    root.mainloop()
