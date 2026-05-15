import tkinter as tk
import customtkinter as ctk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math

                                                                            
def build_fuzzy_system():
    load = ctrl.Antecedent(np.arange(0, 12.1, 0.1), 'load')
    dirt = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'dirt')
    fabric = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'fabric')

    wash_time = ctrl.Consequent(np.arange(0, 61, 1), 'wash_time')
    water_level = ctrl.Consequent(np.arange(0, 101, 1), 'water_level')

    load['S'] = fuzz.trimf(load.universe, [0, 3, 5])
    load['M'] = fuzz.trimf(load.universe, [4, 7, 9.5])
    load['L'] = fuzz.trimf(load.universe, [9, 12, 12])

    dirt['L'] = fuzz.trimf(dirt.universe, [0, 0, 2])
    dirt['M'] = fuzz.trimf(dirt.universe, [1, 5, 7])
    dirt['H'] = fuzz.trimf(dirt.universe, [6, 10, 10])

    fabric['D'] = fuzz.trapmf(fabric.universe, [0, 0, 2.5, 3.5])
    fabric['N'] = fuzz.trapmf(fabric.universe, [2.5, 3.5, 6.5, 7.5])
    fabric['H'] = fuzz.trapmf(fabric.universe, [6.5, 7.5, 10, 10])

    wash_time['S'] = fuzz.trimf(wash_time.universe, [0, 3, 22])
    wash_time['M'] = fuzz.trimf(wash_time.universe, [12, 18, 40])
    wash_time['L'] = fuzz.trimf(wash_time.universe, [35, 58, 60])

    water_level['L'] = fuzz.trimf(water_level.universe, [0, 15, 20])
    water_level['M'] = fuzz.trimf(water_level.universe, [35, 40, 70])
    water_level['H'] = fuzz.trimf(water_level.universe, [75, 85, 90])

    rules = [
        ctrl.Rule(load['S'] & dirt['L'] & fabric['D'], (water_level['L'], wash_time['S'])),
        ctrl.Rule(load['S'] & dirt['M'] & fabric['D'], (water_level['L'], wash_time['S'])),
        ctrl.Rule(load['S'] & dirt['H'] & fabric['D'], (water_level['L'], wash_time['M'])),
        ctrl.Rule(load['M'] & dirt['L'] & fabric['D'], (water_level['M'], wash_time['S'])),
        ctrl.Rule(load['M'] & dirt['M'] & fabric['D'], (water_level['M'], wash_time['M'])),
        ctrl.Rule(load['M'] & dirt['H'] & fabric['D'], (water_level['M'], wash_time['M'])),
        ctrl.Rule(load['L'] & dirt['L'] & fabric['D'], (water_level['H'], wash_time['M'])),
        ctrl.Rule(load['L'] & dirt['M'] & fabric['D'], (water_level['H'], wash_time['M'])),
        ctrl.Rule(load['L'] & dirt['H'] & fabric['D'], (water_level['H'], wash_time['M'])),

        ctrl.Rule(load['S'] & dirt['L'] & fabric['N'], (water_level['L'], wash_time['S'])),
        ctrl.Rule(load['S'] & dirt['M'] & fabric['N'], (water_level['L'], wash_time['M'])),
        ctrl.Rule(load['S'] & dirt['H'] & fabric['N'], (water_level['L'], wash_time['M'])),
        ctrl.Rule(load['M'] & dirt['L'] & fabric['N'], (water_level['M'], wash_time['M'])),
        ctrl.Rule(load['M'] & dirt['M'] & fabric['N'], (water_level['M'], wash_time['M'])),
        ctrl.Rule(load['M'] & dirt['H'] & fabric['N'], (water_level['M'], wash_time['L'])),
        ctrl.Rule(load['L'] & dirt['L'] & fabric['N'], (water_level['H'], wash_time['M'])),
        ctrl.Rule(load['L'] & dirt['M'] & fabric['N'], (water_level['H'], wash_time['L'])),
        ctrl.Rule(load['L'] & dirt['H'] & fabric['N'], (water_level['H'], wash_time['L'])),

        ctrl.Rule(load['S'] & dirt['L'] & fabric['H'], (water_level['L'], wash_time['M'])),
        ctrl.Rule(load['S'] & dirt['M'] & fabric['H'], (water_level['L'], wash_time['M'])),
        ctrl.Rule(load['S'] & dirt['H'] & fabric['H'], (water_level['L'], wash_time['L'])),
        ctrl.Rule(load['M'] & dirt['L'] & fabric['H'], (water_level['M'], wash_time['M'])),
        ctrl.Rule(load['M'] & dirt['M'] & fabric['H'], (water_level['M'], wash_time['L'])),
        ctrl.Rule(load['M'] & dirt['H'] & fabric['H'], (water_level['M'], wash_time['L'])),
        ctrl.Rule(load['L'] & dirt['L'] & fabric['H'], (water_level['H'], wash_time['L'])),
        ctrl.Rule(load['L'] & dirt['M'] & fabric['H'], (water_level['H'], wash_time['L'])),
        ctrl.Rule(load['L'] & dirt['H'] & fabric['H'], (water_level['H'], wash_time['L']))
    ]

    washing_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(washing_ctrl), load, dirt, fabric


               
BG_COLOR = "#F4F7FB"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1E293B"
TEXT_LIGHT = "#64748B"
PRIMARY_BLUE = "#1A73E8"
ACCENT_BLUE = "#3B82F6"
SLIDER_TRACK = "#E2E8F0"
BORDER_COLOR = "#E2E8F0"

ctk.set_appearance_mode("light")

FABRIC_MAP = {"Mỏng nhẹ (Delicate)": 1.5, "Bình thường (Normal)": 5.0, "Dày dặn (Heavy)": 8.5}

class InputCard(ctk.CTkFrame):
    def __init__(self, master, title, icon_text, min_val, max_val, suffix, initial_val, command=None, **kwargs):
        super().__init__(master, fg_color=CARD_BG, corner_radius=15, border_width=1, border_color=BORDER_COLOR, **kwargs)
        self.suffix = suffix
        self.command = command
        self.max_val = max_val

                
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 0))
        
        icon_lbl = ctk.CTkLabel(header_frame, text=icon_text, font=("Segoe UI", 14), text_color=TEXT_LIGHT)
        icon_lbl.pack(side="left", padx=(0, 5))
        
        title_lbl = ctk.CTkLabel(header_frame, text=title, font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK)
        title_lbl.pack(side="left")

                       
        self.val_lbl = ctk.CTkLabel(self, text=f"{initial_val:.1f} {suffix}", font=("Segoe UI", 24, "bold"), text_color=PRIMARY_BLUE)
        self.val_lbl.pack(pady=(5, 5))

                
        self.slider = ctk.CTkSlider(self, from_=min_val, to=max_val, number_of_steps=100,
                                    button_color=PRIMARY_BLUE, button_hover_color=ACCENT_BLUE,
                                    progress_color=PRIMARY_BLUE, fg_color=SLIDER_TRACK,
                                    command=self._on_slider_change)
        self.slider.set(initial_val)
        self.slider.pack(fill="x", padx=15, pady=(5, 5))

                        
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(footer_frame, text=f"{min_val}{suffix}", font=("Segoe UI", 10), text_color=TEXT_LIGHT).pack(side="left")
        
                                    
        if suffix == "%":
            mid_val = f"{(max_val+min_val)/2:.0f}%"
        else:
            mid_val = f"{(max_val+min_val)/2:.1f} kg"
        
        ctk.CTkLabel(footer_frame, text=mid_val, font=("Segoe UI", 10), text_color=TEXT_LIGHT).pack(side="left", expand=True)
        ctk.CTkLabel(footer_frame, text=f"{max_val}{suffix}", font=("Segoe UI", 10), text_color=TEXT_LIGHT).pack(side="right")

    def _on_slider_change(self, value):
        display_val = f"{value:.1f}" if self.suffix == " kg" else f"{int(value)}"
        self.val_lbl.configure(text=f"{display_val} {self.suffix}")
        if self.command:
            self.command()

    def get_value(self):
        return self.slider.get()

class SelectCard(ctk.CTkFrame):
    def __init__(self, master, title, icon_text, options, initial_val, command=None, **kwargs):
        fg_color = kwargs.pop('fg_color', CARD_BG)
        border_width = kwargs.pop('border_width', 1)
        super().__init__(master, fg_color=fg_color, corner_radius=15, border_width=border_width, border_color=BORDER_COLOR, **kwargs)
        self.command = command

                
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 0))
        
        icon_lbl = ctk.CTkLabel(header_frame, text=icon_text, font=("Segoe UI", 14), text_color=TEXT_LIGHT)
        icon_lbl.pack(side="left", padx=(0, 5))
        
        title_lbl = ctk.CTkLabel(header_frame, text=title, font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK)
        title_lbl.pack(side="left")

                     
        self.option_menu = ctk.CTkOptionMenu(self, values=options,
                                             fg_color=SLIDER_TRACK, button_color=SLIDER_TRACK,
                                             button_hover_color="#CBD5E1", text_color=TEXT_DARK,
                                             dropdown_fg_color=CARD_BG, dropdown_text_color=TEXT_DARK,
                                             font=("Segoe UI", 16, "bold"),
                                             command=self._on_change)
        self.option_menu.set(initial_val)
        self.option_menu.pack(fill="x", padx=15, pady=(20, 40))

    def _on_change(self, value):
        if self.command:
            self.command()

    def get_value(self):
        return self.option_menu.get()

class OutputCard(ctk.CTkFrame):
    def __init__(self, master, title, icon_text, initial_val, unit, **kwargs):
        super().__init__(master, fg_color=CARD_BG, corner_radius=15, border_width=1, border_color=BORDER_COLOR, **kwargs)

                
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 0))

        icon_lbl = ctk.CTkLabel(header_frame, text=icon_text, font=("Segoe UI", 14), text_color=TEXT_LIGHT)
        icon_lbl.pack(side="left", padx=(0, 5))

        title_lbl = ctk.CTkLabel(header_frame, text=title, font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK)
        title_lbl.pack(side="left")

                       
        val_frame = ctk.CTkFrame(self, fg_color="transparent")
        val_frame.pack(expand=True, pady=(15, 20))

        self.val_lbl = ctk.CTkLabel(val_frame, text=str(initial_val), font=("Segoe UI", 48, "bold"), text_color=PRIMARY_BLUE)
        self.val_lbl.pack(side="left")

        self.unit_lbl = ctk.CTkLabel(val_frame, text=unit, font=("Segoe UI", 16), text_color=TEXT_DARK)
        self.unit_lbl.pack(side="left", padx=(5, 0), pady=(0, 8))

    def set_value(self, val):
        self.val_lbl.configure(text=str(val))

class WashingMachineApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Washing Machine - Fuzzy Control")
        self.geometry("1100x750")
        self.configure(fg_color=BG_COLOR)
        
        self.sim, self.load_ant, self.dirt_ant, self.fabric_ant = build_fuzzy_system()

        self._build_ui()
        self._initial_draw()

    def _build_ui(self):
                            
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(title_frame, text="WASHING MACHINE", font=("Segoe UI", 24, "bold"), text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Xoay núm để điều chỉnh các thông số ⓘ", font=("Segoe UI", 12), text_color=TEXT_LIGHT).pack(anchor="w")

                              
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=10)

                             
        left_panel = ctk.CTkFrame(content, fg_color="transparent", width=280)
        left_panel.pack(side="left", fill="y")
        
        ctk.CTkLabel(left_panel, text="📥 ĐẦU VÀO (INPUT)", font=("Segoe UI", 13, "bold"), text_color=PRIMARY_BLUE).pack(anchor="w", pady=(0, 10))
        
        self.load_card = InputCard(left_panel, "Khối lượng tải (Load)", "⚖️", 1.0, 12.0, " kg", 7.0, command=self._on_input_change)
        self.load_card.pack(fill="x", pady=(0, 15))
        
        self.dirt_card = InputCard(left_panel, "Mức độ bẩn (Dirt Level)", "👕", 0, 100, "%", 60, command=self._on_input_change)
        self.dirt_card.pack(fill="x", pady=(0, 15))
        
        self.fabric_card = SelectCard(left_panel, "Loại vải (Fabric Type)", "🏷️", list(FABRIC_MAP.keys()), "Bình thường (Normal)", command=self._on_input_change)
        self.fabric_card.pack(fill="x", pady=(0, 15))

                             
        center_panel = ctk.CTkFrame(content, fg_color="transparent")
        center_panel.pack(side="left", fill="both", expand=True, padx=20)
        
                       
        center_top = ctk.CTkFrame(center_panel, fg_color="transparent")
        center_top.pack(pady=(0, 10))
        ctk.CTkLabel(center_top, text="NƯỚC DÂNG", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack()
        self.center_water_lbl = ctk.CTkLabel(center_top, text="60 L", font=("Segoe UI", 28, "bold"), text_color=PRIMARY_BLUE)
        self.center_water_lbl.pack()

                         
        self.canvas_size = 400
        self.drum_canvas = tk.Canvas(center_panel, width=self.canvas_size, height=self.canvas_size, bg=BG_COLOR, highlightthickness=0)
        self.drum_canvas.pack(pady=10)
        
        ctk.CTkLabel(center_panel, text="—     XOAY NÚM ĐỂ THAY ĐỔI GIÁ TRỊ     +", font=("Segoe UI", 11), text_color=TEXT_LIGHT).pack(pady=(10, 0))

                               
        right_panel = ctk.CTkFrame(content, fg_color="transparent", width=280)
        right_panel.pack(side="right", fill="y")

        ctk.CTkLabel(right_panel, text="📤 ĐẦU RA (OUTPUT)", font=("Segoe UI", 13, "bold"), text_color=PRIMARY_BLUE).pack(anchor="w", pady=(0, 10))

        self.time_out = OutputCard(right_panel, "THỜI GIAN GIẶT", "🕒", 47, "phút")
        self.time_out.pack(fill="x", pady=(0, 15))

        self.water_out = OutputCard(right_panel, "LƯỢNG NƯỚC", "💧", 60, "Lít")
        self.water_out.pack(fill="x", pady=(0, 15))

                               
        footer = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=15, height=80, border_width=1, border_color=BORDER_COLOR)
        footer.pack(fill="x", padx=30, pady=(0, 20))
        footer.pack_propagate(False)
        
        status_frame = ctk.CTkFrame(footer, fg_color="transparent")
        status_frame.pack(side="left", padx=20, fill="y", pady=15)
        
        icon_bg = ctk.CTkFrame(status_frame, fg_color="#EBF4FF", width=50, height=50, corner_radius=25)
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)
        ctk.CTkLabel(icon_bg, text="📷", font=("Segoe UI", 20)).pack(expand=True)
        
        status_text_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_text_frame.pack(side="left")
        ctk.CTkLabel(status_text_frame, text="Trạng thái", font=("Segoe UI", 11), text_color=TEXT_LIGHT).pack(anchor="w")
        self.status_lbl = ctk.CTkLabel(status_text_frame, text="Sẵn sàng", font=("Segoe UI", 16, "bold"), text_color=PRIMARY_BLUE)
        self.status_lbl.pack(anchor="w")
        
        sep2 = ctk.CTkFrame(footer, fg_color=BORDER_COLOR, width=1)
        sep2.pack(side="left", fill="y", pady=15, padx=20)
        
        desc_frame = ctk.CTkFrame(footer, fg_color="transparent")
        desc_frame.pack(side="left", pady=15)
        ctk.CTkLabel(desc_frame, text="Hệ thống sẵn sàng.", font=("Segoe UI", 12), text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(desc_frame, text="Bấm nút để bắt đầu mô phỏng.", font=("Segoe UI", 12), text_color=TEXT_LIGHT).pack(anchor="w")
        
        self.start_btn = ctk.CTkButton(footer, text="▶ Bắt đầu giặt", font=("Segoe UI", 16, "bold"), 
                                       fg_color=PRIMARY_BLUE, hover_color=ACCENT_BLUE, height=50, width=200,
                                       command=self._calculate)
        self.start_btn.pack(side="right", padx=20)

    def _initial_draw(self):
                                           
        c = self.drum_canvas
        cx, cy = self.canvas_size/2, self.canvas_size/2
        r_outer = 190
        r_inner = 150
        
                               
        c.create_oval(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer, outline="#E2E8F0", width=2)
        
                    
        for i in range(101):
            angle = math.pi * 0.8 + (math.pi * 1.4 * i / 100)                                       
            if i % 10 == 0:
                length = 12
                width = 2
                color = TEXT_LIGHT
            else:
                length = 6
                width = 1
                color = "#CBD5E1"
            
            x1 = cx + (r_outer - 5) * math.cos(angle)
            y1 = cy + (r_outer - 5) * math.sin(angle)
            x2 = cx + (r_outer - 5 - length) * math.cos(angle)
            y2 = cy + (r_outer - 5 - length) * math.sin(angle)
            c.create_line(x1, y1, x2, y2, fill=color, width=width)
            
                    
        c.create_line(cx, cy - r_outer, cx, cy - r_outer + 15, fill=PRIMARY_BLUE, width=4)

                    
        c.create_oval(cx - r_inner - 10, cy - r_inner - 10, cx + r_inner + 10, cy + r_inner + 10, outline="#CBD5E1", width=5)
        c.create_oval(cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner, outline="#F8FAFC", width=8)
        
        self._on_input_change()               

    def _on_input_change(self, *args):
                                                                                                   
        pass

    def _calculate(self):
        load_val = self.load_card.get_value()
        dirt_val = self.dirt_card.get_value()
        fabric_choice = self.fabric_card.get_value()
        fabric_val = FABRIC_MAP[fabric_choice]

                                                 
        self.sim.input['load'] = load_val
        self.sim.input['dirt'] = dirt_val / 10.0
        self.sim.input['fabric'] = fabric_val
        
        self.sim.compute()

        water = int(self.sim.output['water_level'])
        wash_time = int(self.sim.output['wash_time'])

        self.center_water_lbl.configure(text=f"{water} L")
        self.time_out.set_value(wash_time)
        self.water_out.set_value(water)
        self.status_lbl.configure(text="Đang giặt...")

        self._draw_water(water)

    def _draw_water(self, water_level_val):
        c = self.drum_canvas
        c.delete("water")
        
        cx, cy = self.canvas_size/2, self.canvas_size/2
        r_inner = 150
        
        if water_level_val <= 0:
            return
            
                                                               
                                                                            
        visual_pct = min(water_level_val / 80.0, 1.1) 
        
        fill_h = visual_pct * (2 * r_inner)
        y_top = cy + r_inner - fill_h
        
                                                                  
        step = 2
        for y in range(int(y_top), int(cy + r_inner), step):
            dy = y - cy
            if dy**2 >= r_inner**2:
                continue
            half_chord = math.sqrt(r_inner**2 - dy**2)
            x_left = cx - half_chord
            x_right = cx + half_chord
            
                            
            depth_pct = (y - y_top) / max(1, fill_h)
            r = int(26 + depth_pct * (10 - 26))
            g = int(115 + depth_pct * (70 - 115))
            b = int(232 + depth_pct * (150 - 232))
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            c.create_line(x_left, y, x_right, y, fill=color, width=step, tags="water")
            
                       
        wave_points = []
        for i in range(int(cx - r_inner), int(cx + r_inner), 5):
            dx = i - cx
            if dx**2 >= r_inner**2:
                continue
                           
            wy = y_top + math.sin(i/15.0) * 5
            wave_points.append(i)
            wave_points.append(wy)
            
        if len(wave_points) >= 4:
                                                       
            for j in range(0, len(wave_points)-2, 2):
                c.create_line(wave_points[j], wave_points[j+1], wave_points[j+2], wave_points[j+3], 
                              fill="#4DB8FF", width=3, smooth=True, tags="water")
                              
                                    
        c.create_arc(cx - r_inner + 10, cy - r_inner + 10, cx + r_inner - 10, cy + r_inner - 10, 
                     start=30, extent=120, outline="#FFFFFF", width=3, style=tk.ARC, tags="water")

if __name__ == "__main__":
    app = WashingMachineApp()
    app.mainloop()
