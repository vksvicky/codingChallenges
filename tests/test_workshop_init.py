import unittest
from unittest.mock import Mock, patch
from threading import Lock, Semaphore
from src.santa_workshop import SantaWorkshop

class TestWorkshopInitialization(unittest.TestCase):
    def setUp(self):
        self.workshop = SantaWorkshop()

    def test_counter_initialization(self):
        """Test initial counter values"""
        self.assertEqual(self.workshop.reindeer_count, 0)
        self.assertEqual(self.workshop.elf_count, 0)

    def test_mutex_initialization(self):
        """Test mutex initialization"""
        self.assertIsInstance(self.workshop.mtx, Lock)
        self.assertIsInstance(self.workshop.print_mutex, Lock)
        
        # Verify locks can be acquired and released
        acquired = self.workshop.mtx.acquire(timeout=1)
        self.assertTrue(acquired)
        self.workshop.mtx.release()
        
        acquired = self.workshop.print_mutex.acquire(timeout=1)
        self.assertTrue(acquired)
        self.workshop.print_mutex.release()

    def test_semaphore_initialization(self):
        """Test semaphore initialization"""
        # Test instance types
        self.assertIsInstance(self.workshop.santa_sem, Semaphore)
        self.assertIsInstance(self.workshop.reindeer_sem, Semaphore)
        self.assertIsInstance(self.workshop.only_elves, Semaphore)
        # self.assertIsInstance(self.workshop.santa_signal, Semaphore)
        # self.assertIsInstance(self.workshop.problem, Semaphore)
        self.assertIsInstance(self.workshop.elf_done, Semaphore)
        self.assertIsInstance(self.workshop.last_reindeer_sem, Semaphore)
        
        # Test initial values
        self.assertEqual(self.workshop.santa_sem._value, 0)
        self.assertEqual(self.workshop.reindeer_sem._value, 0)
        self.assertEqual(self.workshop.only_elves._value, 3)
        # self.assertEqual(self.workshop.santa_signal._value, 0)
        # self.assertEqual(self.workshop.problem._value, 0)
        self.assertEqual(self.workshop.elf_done._value, 0)
        self.assertEqual(self.workshop.last_reindeer_sem._value, 0)

    @patch('src.santa_workshop.Lock')
    def test_lock_creation(self, mock_lock):
        """Test locks are created properly"""
        workshop = SantaWorkshop()
        self.assertEqual(mock_lock.call_count, 2)  # One for mtx, one for print_mutex

    @patch('src.santa_workshop.Semaphore')
    def test_semaphore_creation(self, mock_semaphore):
        """Test semaphores are created with correct initial values"""
        workshop = SantaWorkshop()
        
        # Verify individual semaphore creation calls
        expected_calls = [
            (0,),  # santa_sem
            (0,),  # reindeer_sem
            (3,),  # only_elves
            (0,),  # santa_signal
            (0,),  # problem
            (0,),  # elf_done
            (0,),  # last_reindeer_sem
        ]
        
        # Verify all calls were made with correct arguments
        self.assertEqual(mock_semaphore.call_count, 7)
        mock_semaphore.assert_has_calls([
            unittest.mock.call(args[0]) for args in expected_calls
        ], any_order=True)

    def test_thread_safety(self):
        """Test thread safety of counter operations"""
        with self.workshop.mtx:
            self.workshop.reindeer_count += 1
            self.assertEqual(self.workshop.reindeer_count, 1)
            
        with self.workshop.mtx:
            self.workshop.elf_count += 1
            self.assertEqual(self.workshop.elf_count, 1)

if __name__ == '__main__':
    unittest.main()