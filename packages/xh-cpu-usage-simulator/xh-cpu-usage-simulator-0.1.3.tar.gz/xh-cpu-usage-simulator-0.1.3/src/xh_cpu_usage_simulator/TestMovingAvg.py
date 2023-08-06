import unittest

from xh_cpu_usage_simulator.MovingAvg import MovingAvg


class TestMovingAvg(unittest.TestCase):
    def test_mv(self):
        m_avg = MovingAvg(3)
        m_avg.insert(6)
        self.assertEquals(2, m_avg.avg)
        m_avg.insert(1)
        self.assertEquals(7/3, m_avg.avg)
        self.assertEquals(6, m_avg.data[0])
        self.assertEquals(1, m_avg.data[1])
        self.assertEquals(0, m_avg.data[2])

        m_avg.insert(3)
        self.assertEquals(10/3, m_avg.avg)
        self.assertEquals(6, m_avg.data[0])
        self.assertEquals(1, m_avg.data[1])
        self.assertEquals(3, m_avg.data[2])

        m_avg.insert(4)
        self.assertEquals(8/3, m_avg.avg)
        self.assertEquals(4, m_avg.data[0])
        self.assertEquals(1, m_avg.data[1])
        self.assertEquals(3, m_avg.data[2])
