import queue
import time
import unittest
from typing import Generator

import numpy as np

from kmspy.data.prefetch_generator import PrefetchUnit, PrefetchGenerator


def return_values(type=None):
    if type is int:
        return 1
    elif type is tuple:
        return (0, 1,)
    elif type is list:
        return [0, 1]
    elif type is dict:
        return {"0": 0, "1": 1}
    elif type is bool:
        return True
    elif type is np.ndarray:
        return np.array([0, 1])
    elif type is Generator:
        return (i for i in range(2))
    else:
        return None


class TestPrefetchUnit(unittest.TestCase):

    def test_get(self):
        unit = PrefetchUnit(1, 0, False, return_values)
        inputs = [int, tuple, list, dict, bool, np.ndarray, Generator, None]
        for i in inputs:
            unit.put(i)
        i = 0
        while i < len(inputs):
            try:
                item, uid, idx, err = unit.queue.get_nowait()
                self.assertEqual(uid, 0)
                self.assertEqual(idx, i)
                if not err:
                    v = return_values(inputs[i])
                    if isinstance(item, np.ndarray):
                        item = np.mean(item)
                        v = np.mean(item)
                    elif i == 6:  # generater
                        vs = list(v)
                        v = vs[0]
                        _item, _, _, _ = unit.queue.get_nowait()
                        self.assertEqual(_item, vs[1])
                    self.assertEqual(item, v)
                    i += 1
                else:
                    self.assertEqual(item, StopIteration)
            except queue.Empty:
                # unit에서 꺼낼 데이터가 없음
                # 잠깐 대기
                time.sleep(0.01)
            except Exception as e:
                pass


# class TestPrefetchGenerator(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

if __name__ == '__main__':
    unittest.main()