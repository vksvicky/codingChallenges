import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
from src.santa_workshop import SantaWorkshop

class SantaWorkshopGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Santa's Workshop")
        self.root.geometry("1000x800")  # Increased window size
        self.running = True
        self.progress_var = tk.StringVar(value="Progress: 0/20 deliveries")
        
        # Add update queue
        self.update_queue = []
        self.root.after(100, self.process_updates)
        
        # Add activity timing variables
        self.activity_start_time = None
        self.activity_duration = 0
        self.completed = False  # Add completion flag
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Emojis and colors
        self.emojis = {
            "santa_sleeping": "😴",
            "santa_helping": "🎅",
            "santa_delivering": "🛷",
            "elf": "🧝",
            "reindeer": "🦌",
        }
        
        self.colors = {
            "sleeping": "#ADD8E6",  # Light blue
            "helping": "#90EE90",   # Light green
            "delivering": "#FFB6C1", # Light pink
            "background": "#F0F0F0"  # Light gray
        }
        
        self.workshop = SantaWorkshop()
        self.workshop.set_log_callback(self.log_activity)  # Set logging callback
        self.setup_gui()
        self.start_threads()

    def setup_gui(self):
        # Configure grid with weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main frame with padding
        self.main_frame = ttk.Frame(self.root, padding="30")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title with more padding
        title_label = ttk.Label(self.main_frame, 
                               text="Santa's Workshop 🎄", 
                               font=('Arial', 28, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=30)
        
        # Status frame with more height
        status_frame = ttk.LabelFrame(self.main_frame, text="", padding="20")
        status_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=20)
        
        # Status displays
        self.santa_status = tk.StringVar(value=f"Santa is sleeping {self.emojis['santa_sleeping']}")
        self.reindeer_count = tk.StringVar(value=f"Reindeer: 0 {self.emojis['reindeer']}")
        self.elf_count = tk.StringVar(value=f"Elves: 0 {self.emojis['elf']}")
        self.timer = tk.StringVar(value="⏰ 00:00")
        
        # Status labels with larger fonts and padding
        ttk.Label(status_frame, textvariable=self.santa_status, 
                 font=('Arial', 16)).grid(row=0, column=0, pady=5, padx=10)
        ttk.Label(status_frame, textvariable=self.reindeer_count, 
                 font=('Arial', 14)).grid(row=1, column=0, pady=5, padx=10)
        ttk.Label(status_frame, textvariable=self.elf_count, 
                 font=('Arial', 14)).grid(row=2, column=0, pady=5, padx=10)
        ttk.Label(status_frame, textvariable=self.timer, 
                 font=('Arial', 14)).grid(row=3, column=0, pady=5, padx=10)
        
        # Add progress label
        ttk.Label(status_frame, textvariable=self.progress_var, 
                 font=('Arial', 14)).grid(row=4, column=0, pady=5, padx=10)
        
        # Activity Log with increased height
        log_frame = ttk.LabelFrame(self.main_frame, text="Activity Log 📝", padding="20")
        log_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=20)
        
        self.log_text = tk.Text(log_frame, height=15, width=60, font=('Arial', 12))
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=10)
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Button frame moved to right side
        self.button_frame = ttk.Frame(self.main_frame, padding="20")
        self.button_frame.grid(row=2, column=2, sticky="n", padx=20)
        
        # Add speed control above buttons
        speed_frame = ttk.LabelFrame(self.button_frame, text="Simulation Speed", padding="10")
        speed_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_slider = ttk.Scale(speed_frame, from_=0.1, to=1.5, 
                               variable=self.speed_var,
                               orient="horizontal",
                               command=self.update_speed)
        speed_slider.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.grid(row=1, column=0, pady=5)
        
        # Exit and Restart buttons (initially hidden)
        style = ttk.Style()
        style.configure("Exit.TButton", font=('Arial', 12))
        style.configure("Restart.TButton", font=('Arial', 12))
        
        self.exit_btn = ttk.Button(self.button_frame, text="Exit Workshop 🚪", 
                                 command=self.on_closing, style="Exit.TButton",
                                 width=20)
        self.restart_btn = ttk.Button(self.button_frame, text="Restart Workshop 🔄", 
                                    command=self.restart_simulation, style="Restart.TButton",
                                    width=20)

    def show_control_buttons(self):
        """Show the exit and restart buttons when simulation completes"""
        self.restart_btn.grid(row=1, column=0, columnspan=2, pady=(0, 5))
        self.exit_btn.grid(row=2, column=0, columnspan=2)

    def process_updates(self):
        """Process queued updates in the main thread"""
        while self.update_queue:
            func, args = self.update_queue.pop(0)
            func(*args)
        if self.running:
            self.root.after(100, self.process_updates)

    def safe_update(self, func, *args):
        """Queue updates to be processed in main thread"""
        self.update_queue.append((func, args))

    def update_display(self):
        while self.running:
            try:
                # Update counts with emojis using safe update
                self.safe_update(self.reindeer_count.set, 
                    f"Reindeer: {self.workshop.reindeer_count} {self.emojis['reindeer']}")
                self.safe_update(self.elf_count.set,
                    f"Elves: {self.workshop.elf_count} {self.emojis['elf']}")
                
                # Update Santa's status with emoji
                current_state = self.workshop.santa_state
                if current_state == "sleeping":
                    emoji = self.emojis['santa_sleeping']
                    if self.activity_start_time is not None:
                        self.activity_start_time = None
                        self.safe_update(self.timer.set, "⏰ 00:00")
                        
                elif current_state == "helping":
                    emoji = self.emojis['santa_helping']
                    if self.activity_start_time is None:
                        self.activity_start_time = time.time()
                        self.activity_duration = 60
                        self.safe_update(self.log_activity, f"Santa started helping elves {emoji}")
                        
                elif current_state == "delivering":
                    emoji = self.emojis['santa_delivering']
                    if self.activity_start_time is None:
                        self.activity_start_time = time.time()
                        self.activity_duration = 90
                        self.safe_update(self.log_activity, f"Santa started delivering presents {emoji}")
                
                # Update timer if activity is ongoing
                if self.activity_start_time is not None:
                    elapsed = (time.time() - self.activity_start_time) * self.workshop.speed_scale
                    remaining = max(0, self.activity_duration - elapsed)
                    if remaining == 0:
                        self.safe_update(self.timer.set, "⏰ 00:00")
                        self.activity_start_time = None
                    else:
                        minutes = int(remaining // 60)
                        seconds = int(remaining % 60)
                        self.safe_update(self.timer.set, f"⏰ {minutes:02d}:{seconds:02d}")
                
                # Update status and progress
                new_status = f"Santa is {current_state} {emoji}"
                if self.santa_status.get() != new_status:
                    self.safe_update(self.santa_status.set, new_status)
                    self.safe_update(self.log_activity, f"Santa is now {current_state} {emoji}")
                
                self.safe_update(self.progress_var.set, 
                    f"Progress: {self.workshop.total_deliveries}/20 deliveries")
                
                # Check for completion
                if not self.completed and self.workshop.total_deliveries >= 20:
                    self.completed = True
                    self.safe_update(self.log_activity, "Workshop goal reached! 🎉")
                    self.safe_update(self.show_control_buttons)
                    self.workshop.shutdown()  # Stop the workshop when goal is reached
                
                time.sleep(0.1)
            except Exception as e:
                self.safe_update(self.log_activity, f"Error: {str(e)}")
                break

    def start_threads(self):
        """Initialize and start all workshop threads"""
        # Start display update thread
        self.display_thread = threading.Thread(target=self.update_display, daemon=True)
        self.display_thread.start()
        
        # Start Santa thread
        self.santa_thread = threading.Thread(target=self.workshop.santa_thread, daemon=True)
        self.santa_thread.start()
        
        # Start reindeer threads
        self.reindeer_threads = []
        for i in range(9):
            thread = threading.Thread(target=self.workshop.reindeer_thread, args=(i,), daemon=True)
            self.reindeer_threads.append(thread)
            thread.start()
        
        # Start elf threads
        self.elf_threads = []
        for i in range(10):
            thread = threading.Thread(target=self.workshop.elf_thread, args=(i,), daemon=True)
            self.elf_threads.append(thread)
            thread.start()
        
        # Log startup
        self.log_activity("Workshop started! 🎄")

    def on_closing(self):
        """Safely shutdown the application"""
        self.running = False
        self.workshop.shutdown()
        
        def cleanup():
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
        
        # Schedule cleanup after a short delay
        self.root.after(100, cleanup)
        
        # Log closing message
        try:
            self.log_activity("Closing workshop... 🎄")
        except:
            pass

    def restart_simulation(self):
        """Safely restart the simulation"""
        # Stop current workshop
        self.running = False
        self.workshop.shutdown()
        
        # Wait for threads to clean up
        time.sleep(0.2)
        
        # Reset state
        self.running = True
        self.completed = False
        self.workshop = SantaWorkshop()
        self.activity_start_time = None
        self.activity_duration = 0
        
        # Clear UI
        self.safe_update(self.log_activity, "Restarting workshop simulation... 🎄")
        self.exit_btn.grid_remove()
        self.restart_btn.grid_remove()
        
        # Start new threads
        self.start_threads()

    def log_activity(self, message):
        """Thread-safe logging of activities"""
        def _log():
            self.log_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
            self.log_text.see(tk.END)
        
        if threading.current_thread() is threading.main_thread():
            _log()
        else:
            self.safe_update(_log)

    def update_speed(self, value):
        """Update the simulation speed"""
        speed = round(float(value), 2)
        self.speed_label.configure(text=f"{speed}x")
        self.workshop.set_speed(speed)

def run_santa_gui():
    root = tk.Tk()
    app = SantaWorkshopGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_santa_gui()