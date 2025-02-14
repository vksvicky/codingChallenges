from threading import Semaphore, Thread, Lock, Event
import time
import random

class SantaWorkshop:
    def __init__(self):
        # Shared state
        self.reindeer_count = 0
        self.elf_count = 0
        self.santa_state = "sleeping"
        
        # Activity counters and goals
        self.total_deliveries = 0
        self.total_helps = 0
        self.required_deliveries = 20  # Set target deliveries
        
        # State events
        self.helping_event = Event()
        self.delivering_event = Event()
        
        # Mutex for counters
        self.mtx = Lock()
        self.print_mutex = Lock()
        
        # Semaphores
        self.santa_sem = Semaphore(0)        # Wake Santa
        self.reindeer_sem = Semaphore(0)     # Signal reindeer
        self.elf_sem = Semaphore(0)          # Signal elves
        self.only_elves = Semaphore(3)       # Max elves that can wait
        self.elf_ready = Semaphore(0)        # Elf ready to ask question
        self.elf_done = Semaphore(0)         # Elf help completion
        self.last_reindeer_sem = Semaphore(0)  # Last reindeer signal
        self.running = True  # Add running flag
        self.speed_scale = 1.0  # Add speed scale variable
        self.log_callback = None  # Add callback for logging
        
    def set_log_callback(self, callback):
        """Set callback function for logging"""
        self.log_callback = callback

    def set_speed(self, speed):
        """Update the simulation speed"""
        self.speed_scale = float(speed)
        
    def shutdown(self):
        """Safely shutdown the workshop"""
        self.running = False
        # Release all semaphores multiple times to ensure all threads are unblocked
        for _ in range(max(10, self.elf_count + self.reindeer_count)):
            self.santa_sem.release()
            self.reindeer_sem.release()
            self.elf_ready.release()
            self.elf_done.release()
            self.last_reindeer_sem.release()
            self.only_elves.release()

    def random_sleep(self, min_ms, max_ms, scale=1.0):
        """Sleep for a random duration between min_ms and max_ms milliseconds"""
        if scale <= 0:
            scale = 1.0  # Use default scale if zero or negative
        ms = random.randint(min_ms, max_ms)
        scaled_ms = ms / scale  # Divide by scale to speed up or slow down
        time.sleep(scaled_ms / 1000.0)  # Convert to seconds

    def reindeer_thread(self, id):
        while self.running:
            # Simulate vacation
            self.random_sleep(10, 20)
            
            with self.mtx:
                self.reindeer_count += 1
                if self.log_callback:
                    self.log_callback(f"Reindeer {id} returned from vacation (Total: {self.reindeer_count} 🦌)")
                if self.reindeer_count == 9:
                    self.santa_sem.release()
            
            # Wait for Santa
            self.reindeer_sem.acquire()
            
            # Get hitched and deliver
            self.random_sleep(10, 30)
            
            # Wait for delivery completion
            if id == 8:  # Last reindeer
                self.last_reindeer_sem.acquire()
                if self.log_callback:
                    self.log_callback("All reindeer finished delivery 🛷")

    def elf_thread(self, id):
        while self.running:
            self.random_sleep(20, 40)
            
            # Ensure max 3 elves waiting
            self.only_elves.acquire()
            
            with self.mtx:
                self.elf_count += 1
                if self.log_callback:
                    self.log_callback(f"Elf {id} needs help (Total waiting: {self.elf_count} 🧝)")
                if self.elf_count == 3:
                    self.santa_sem.release()
            
            # Wait for Santa's help
            self.elf_ready.acquire()
            
            # Get help from Santa
            self.random_sleep(5, 10)
            
            # Signal completion and decrease count
            with self.mtx:
                self.elf_count -= 1
                if self.log_callback:
                    self.log_callback(f"Elf {id} finished getting help (Remaining: {self.elf_count} 🧝)")
                self.elf_done.release()
            
            self.only_elves.release()

    def santa_thread(self):
        while self.running:
            self.santa_sem.acquire()
            
            with self.mtx:
                if self.total_deliveries >= self.required_deliveries:
                    self.santa_state = "sleeping"
                    continue
                    
                if self.reindeer_count >= 9:
                    self.santa_state = "delivering"
                    self.delivering_event.set()
                    
                    # Signal all reindeer
                    for _ in range(9):
                        self.reindeer_sem.release()
                    
                    # Help reindeer
                    self.random_sleep(100, 100)
                    
                    # Reset reindeer count and update state
                    self.reindeer_count = 0
                    self.total_deliveries += 1
                    self.santa_state = "sleeping"
                    self.delivering_event.clear()
                    
                    # Signal completion to last reindeer
                    self.last_reindeer_sem.release()
                    
                elif self.elf_count >= 3:
                    self.santa_state = "helping"
                    self.helping_event.set()
                    
                    # Signal all elves
                    for _ in range(3):
                        self.elf_ready.release()
                    
                    # Help elves
                    self.random_sleep(100, 100)
                    
                    # Signal completion
                    for _ in range(3):
                        self.elf_done.release()
                    
                    self.total_helps += 1
                    self.santa_state = "sleeping"
                    self.helping_event.clear()
                    
                    # Wait for all elves to finish
                    for _ in range(3):
                        self.elf_done.acquire()
                    
                    # Release mutex to allow test to see state change
                    self.mtx.release()
                    
                    # Signal all waiting elves
                    for _ in range(3):
                        self.elf_ready.release()
                    
                    # Help elves
                    time.sleep(0.1)  # Fixed delay for testing
                    
                    # Signal completion
                    for _ in range(3):
                        self.elf_done.release()
                    
                    # Reacquire mutex to change state back
                    self.mtx.acquire()
                    self.santa_state = "sleeping"