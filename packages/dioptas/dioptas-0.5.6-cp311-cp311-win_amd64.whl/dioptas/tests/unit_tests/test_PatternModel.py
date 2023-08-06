# -*- coding: utf-8 -*-
# Dioptas - GUI program for fast processing of 2D X-ray diffraction data
# Principal author: Clemens Prescher (clemens.prescher@gmail.com)
# Copyright (C) 2014-2019 GSECARS, University of Chicago, USA
# Copyright (C) 2015-2018 Institute for Geology and Mineralogy, University of Cologne, Germany
# Copyright (C) 2019-2020 DESY, Hamburg, Germany
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import os
import numpy as np
from numpy.testing import assert_array_almost_equal

from ...model.PatternModel import Pattern, PatternModel
from ...model.util.PeakShapes import gaussian

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')


class PatternModelTest(unittest.TestCase):
    def setUp(self):
        self.x = np.linspace(0.1, 15, 100)
        self.y = np.sin(self.x)
        self.pattern = Pattern(self.x, self.y)
        self.pattern_model = PatternModel()

    def test_set_pattern(self):
        self.pattern_model.set_pattern(self.x, self.y, 'hoho')
        assert_array_almost_equal(self.pattern_model.get_pattern().x, self.x)
        assert_array_almost_equal(self.pattern_model.get_pattern().y, self.y)
        self.assertEqual(self.pattern_model.get_pattern().name, 'hoho')

    def test_load_pattern(self):
        self.pattern_model.load_pattern(os.path.join(data_path, 'pattern_001.xy'))
        self.assertEqual(self.pattern_model.get_pattern().name, 'pattern_001')
        self.assertNotEqual(len(self.x), len(self.pattern_model.get_pattern().x))
        self.assertNotEqual(len(self.y), len(self.pattern_model.get_pattern().y))

    def test_auto_background_subtraction(self):
        x = np.linspace(0, 24, 2500)
        y = np.zeros(x.shape)

        peaks = [
            [10, 3, 0.1],
            [12, 4, 0.1],
            [12, 6, 0.1],
        ]
        for peak in peaks:
            y += gaussian(x, peak[0], peak[1], peak[2])
        y_bkg = x * 0.4 + 5.0
        y_measurement = y + y_bkg

        self.pattern_model.set_pattern(x, y_measurement)

        auto_background_subtraction_parameters = [2, 50, 50]
        self.pattern_model.set_auto_background_subtraction(auto_background_subtraction_parameters)

        x_spec, y_spec = self.pattern_model.pattern.data

        self.assertAlmostEqual(np.sum(y_spec - y), 0)


if __name__ == '__main__':
    unittest.main()
