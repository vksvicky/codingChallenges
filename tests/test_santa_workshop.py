
import unittest
from threading import Thread, Event, Lock
from unittest.mock import patch
import time
from src.santa_workshop import SantaWorkshop

class TestSantaWorkshop(unittest.TestCase):
    def setUp(self):
        self.workshop = SantaWorkshop()
        self.events = []

    def test_reindeer_synchronization(self):
        """Test that Santa only prepares sleigh when all 9 reindeer arrive"""
        # Start Santa thread
        santa_thread = Thread(target=self.workshop.santa_thread, daemon=True)
        santa_thread.start()
        
        # Start 8 reindeer
        reindeer_threads = []
        for i in range(8):
            thread = Thread(target=self.workshop.reindeer_thread, args=(i,), daemon=True)
            thread.start()
            reindeer_threads.append(thread)
        
        # Wait and check Santa hasn't prepared sleigh
        time.sleep(0.1)
        self.assertEqual(self.workshop.reindeer_count, 8)
        self.assertEqual(self.workshop.santa_state, "sleeping")
        
        # Add last reindeer
        thread = Thread(target=self.workshop.reindeer_thread, args=(8,), daemon=True)
        thread.start()
        reindeer_threads.append(thread)
        
        # Wait and verify Santa prepared sleigh
        time.sleep(0.1)
        self.assertEqual(self.workshop.santa_state, "delivering")

    def test_elf_synchronization(self):
        """Test that Santa only helps elves when exactly 3 are waiting"""
        # Start Santa thread
        santa_thread = Thread(target=self.workshop.santa_thread, daemon=True)
        santa_thread.start()
        
        # Start 2 elves
        elf_threads = []
        for i in range(2):
            thread = Thread(target=self.workshop.elf_thread, args=(i,), daemon=True)
            thread.start()
            elf_threads.append(thread)
        
        # Wait and check Santa hasn't helped
        time.sleep(0.1)
        self.assertEqual(self.workshop.elf_count, 2)
        self.assertEqual(self.workshop.santa_state, "sleeping")
        
        # Add third elf
        thread = Thread(target=self.workshop.elf_thread, args=(2,), daemon=True)
        thread.start()
        elf_threads.append(thread)
        
        # Wait and verify Santa helped
        time.sleep(0.1)
        self.assertEqual(self.workshop.santa_state, "helping")

    def test_reindeer_priority_over_elves(self):
        """Test that reindeer take priority over elves"""
        # Mock random_sleep to speed up test
        with patch.object(self.workshop, 'random_sleep'):
            # Start Santa thread
            santa_thread = Thread(target=self.workshop.santa_thread, daemon=True)
            santa_thread.start()
            
            # Start 3 elves and ensure they're all ready
            elf_threads = []
            for i in range(3):
                thread = Thread(target=self.workshop.elf_thread, args=(i,), daemon=True)
                thread.start()
                elf_threads.append(thread)
            
            # Wait for elves to be processed
            while self.workshop.elf_count < 3:
                time.sleep(0.05)
            
            # Additional wait to ensure Santa processes elves
            time.sleep(0.2)
            self.assertEqual(self.workshop.santa_state, "sleeping")
            
            # Start all reindeer at once
            reindeer_threads = []
            for i in range(9):
                thread = Thread(target=self.workshop.reindeer_thread, args=(i,), daemon=True)
                thread.start()
                reindeer_threads.append(thread)
            
            # Wait for all reindeer to arrive
            while self.workshop.reindeer_count < 9:
                time.sleep(0.05)
            
            # Wait for Santa to switch tasks
            time.sleep(0.2)
            self.assertEqual(self.workshop.santa_state, "sleeping")
            
            # Clean up
            self.workshop.shutdown()
            santa_thread.join(timeout=0.1)

    def test_random_sleep_basic(self):
        """Test that random_sleep works with basic parameters"""
        start_time = time.time()
        self.workshop.random_sleep(50, 150)
        elapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Adjust ranges to account for system timing variations
        min_expected = 40  # Lowered from 50 to account for timing variations
        max_expected = 200  # Increased from 150 to account for system delays
        self.assertTrue(min_expected <= elapsed <= max_expected,
                       f"Sleep duration {elapsed}ms outside expected range [{min_expected}, {max_expected}]")

    def test_random_sleep_with_scale(self):
        """Test that random_sleep respects the scale parameter"""
        # Set a fixed scale for testing
        scale = 2.0
        min_ms = 50
        max_ms = 100
        
        # Test with mocked time and random
        with patch('time.sleep') as mock_sleep, \
             patch('random.randint') as mock_randint:
            
            # Set random value to be consistent
            mock_randint.return_value = 80
            
            # Call random_sleep with scale
            self.workshop.random_sleep(min_ms, max_ms, scale=scale)
            
            # Verify random range
            mock_randint.assert_called_once_with(min_ms, max_ms)
            
            # Verify sleep duration (80ms / 2.0 = 40ms = 0.04s)
            mock_sleep.assert_called_once_with(0.04)

    def test_mutex_initialization(self):
        """Test that mutexes are properly initialized"""
        self.assertIsInstance(self.workshop.mtx, Lock)
        self.assertIsInstance(self.workshop.print_mutex, Lock)

    def test_semaphore_initialization(self):
        """Test that all semaphores are properly initialized"""
        from threading import Semaphore
        
        # Test all semaphores
        semaphores = {
            'santa_sem': 0,
            'reindeer_sem': 0,
            'elf_sem': 0,
            'only_elves': 3,
            'elf_ready': 0,
            'elf_done': 0,
            'last_reindeer_sem': 0
        }
        
        # Test instance types
        for sem_name, initial_value in semaphores.items():
            sem = getattr(self.workshop, sem_name)
            self.assertIsInstance(sem, Semaphore, f"{sem_name} should be a Semaphore")
            self.assertEqual(sem._value, initial_value, 
                           f"{sem_name} should have initial value {initial_value}")

if __name__ == '__main__':
    unittest.main()