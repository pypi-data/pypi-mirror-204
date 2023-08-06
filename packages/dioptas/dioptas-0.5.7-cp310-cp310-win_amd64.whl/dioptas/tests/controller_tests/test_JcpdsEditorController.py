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
from ..utility import QtTest
from qtpy.QtTest import QTest
from qtpy import QtCore, QtGui
import os
import gc
from qtpy import QtWidgets

from mock import MagicMock
import numpy as np

from ..utility import click_button, enter_value_into_text_field, delete_if_exists
from ...controller.integration import JcpdsEditorController
from ...model.DioptasModel import DioptasModel
from ...widgets.integration import IntegrationWidget

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')
jcpds_path = os.path.join(data_path, 'jcpds')


class JcpdsEditorControllerTest(QtTest):
    # SETUP
    #######################
    def setUp(self) -> None:
        self.model = DioptasModel()
        self.model.calibration_model.is_calibrated = True
        self.model.calibration_model.pattern_geometry.wavelength = 0.31E-10
        self.model.calibration_model.integrate_1d = MagicMock(return_value=(self.model.calibration_model.tth,
                                                                            self.model.calibration_model.int))

        self.phase_model = self.model.phase_model

        self.widget = IntegrationWidget()

        self.controller = JcpdsEditorController(self.widget, self.model)
        self.model.pattern_model.load_pattern(os.path.join(data_path, 'pattern_001.xy'))

        self.jcpds_widget = self.controller.jcpds_widget
        self.phase_widget = self.widget.phase_widget

        self.load_phases()
        self.controller.active = True
        self.controller.show_view()

        self.setup_selected_row(5)
        click_button(self.phase_widget.edit_btn)

    def tearDown(self) -> None:
        del self.controller
        del self.widget
        self.model.delete_configurations()
        del self.model
        delete_if_exists(os.path.join(jcpds_path, 'dummy.jcpds'))
        delete_if_exists(os.path.join(data_path, 'reflection_table.txt'))
        gc.collect()

    # Utility Functions
    #######################
    def load_phase(self, filename):
        self.model.phase_model.add_jcpds(os.path.join(jcpds_path, filename))

    def load_phases(self):
        self.load_phase('ar.jcpds')
        self.load_phase('ag.jcpds')
        self.load_phase('au_Anderson.jcpds')
        self.load_phase('mo.jcpds')
        self.load_phase('pt.jcpds')
        self.load_phase('re.jcpds')

    def setup_selected_row(self, ind):
        self.phase_widget.get_selected_phase_row = MagicMock(return_value=ind)

    def send_phase_tw_select_signal(self, ind):
        self.phase_widget.phase_tw.currentCellChanged.emit(ind, 0, 0, 0)

    def set_symmetry(self, symmetry):
        self.jcpds_widget.symmetry_cb.setCurrentIndex(self.jcpds_widget.symmetries.index(symmetry))
        QtWidgets.QApplication.processEvents()

    # Tests
    #######################
    def test_edit_button_shows_correct_phase(self):
        self.assertEqual(self.jcpds_widget.filename_txt.text(), self.phase_model.phases[5].filename)

    def test_selection_changed_shows_correct_phase(self):
        self.send_phase_tw_select_signal(3)
        self.assertEqual(self.jcpds_widget.filename_txt.text(), self.phase_model.phases[3].filename)

    def test_updating_the_gui_after_external_change(self):
        previous_a = self.jcpds_widget.lattice_eos_a_txt.text()
        self.phase_model.set_pressure(5, 20)
        self.assertNotEqual(previous_a, self.jcpds_widget.lattice_eos_a_txt.text())

    def test_updating_volume_after_changing_a(self):
        previous_volume = self.jcpds_widget.lattice_volume_txt.text()
        self.jcpds_widget.lattice_a_sb.setValue(3)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_volume_txt.text())

    def test_updating_volume_after_changing_c(self):
        previous_volume = self.jcpds_widget.lattice_volume_txt.text()
        self.jcpds_widget.lattice_c_sb.setValue(3)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_volume_txt.text())

    def test_updating_volume_after_changing_ca_ratio(self):
        previous_volume = self.jcpds_widget.lattice_volume_txt.text()
        self.jcpds_widget.lattice_c_sb.setValue(3)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_volume_txt.text())

    def test_updating_k0_parameter(self):
        self.phase_model.set_pressure(5, 30)
        previous_volume = self.jcpds_widget.lattice_eos_volume_txt.text()
        enter_value_into_text_field(self.jcpds_widget.eos_K_txt, 300)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_eos_volume_txt.text())

    def test_updating_kp_parameter(self):
        self.phase_model.set_pressure(5, 30)
        previous_volume = self.jcpds_widget.lattice_eos_volume_txt.text()
        enter_value_into_text_field(self.jcpds_widget.eos_Kp_txt, 5)
        self.assertNotEqual(previous_volume, self.jcpds_widget.lattice_eos_volume_txt.text())

    def test_adding_a_reflection(self):
        num_phase_reflections = len(self.phase_model.phases[5].reflections)
        num_table_reflections = self.jcpds_widget.reflection_table_model.rowCount()
        self.assertEqual(num_phase_reflections, num_table_reflections)

        click_button(self.jcpds_widget.reflections_add_btn)

        self.assertEqual(len(self.phase_model.phases[5].reflections),
                         num_phase_reflections + 1)
        self.assertEqual(self.jcpds_widget.reflection_table_model.rowCount(),
                         num_table_reflections + 1)

    def test_adding_two_reflections(self):
        num_phase_reflections = len(self.phase_model.phases[5].reflections)
        num_table_reflections = self.jcpds_widget.reflection_table_model.rowCount()
        self.assertEqual(num_phase_reflections, num_table_reflections)

        click_button(self.jcpds_widget.reflections_add_btn)
        click_button(self.jcpds_widget.reflections_add_btn)

        self.assertEqual(len(self.phase_model.phases[5].reflections),
                         num_phase_reflections + 2)
        self.assertEqual(self.jcpds_widget.reflection_table_model.rowCount(),
                         num_table_reflections + 2)

    def test_removing_one_reflection(self):
        num_phase_reflections = len(self.phase_model.phases[5].reflections)
        num_table_reflections = self.jcpds_widget.reflection_table_model.rowCount()
        self.assertEqual(num_phase_reflections, num_table_reflections)

        self.jcpds_widget.get_selected_reflections = MagicMock(return_value=[3])

        click_button(self.jcpds_widget.reflections_delete_btn)

        self.assertEqual(self.jcpds_widget.reflection_table_model.rowCount(),
                         num_table_reflections - 1)
        self.assertEqual(len(self.phase_model.phases[5].reflections),
                         num_phase_reflections - 1)

    def test_removing_multiple_reflections(self):
        num_phase_reflections = len(self.phase_model.phases[5].reflections)
        num_table_reflections = self.jcpds_widget.reflection_table_model.rowCount()
        self.assertEqual(num_phase_reflections, num_table_reflections)

        self.jcpds_widget.reflection_table_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for ind in [3, 1, 5, 11]:
            self.jcpds_widget.reflection_table_view.selectRow(ind)

        click_button(self.jcpds_widget.reflections_delete_btn)

        self.assertEqual(len(self.phase_model.phases[5].reflections),
                         num_phase_reflections - 4)
        self.assertEqual(self.jcpds_widget.reflection_table_model.rowCount(),
                         num_table_reflections - 4)

    def test_clear_reflections(self):
        self.assertGreater(self.jcpds_widget.reflection_table_model.rowCount(), 0)
        click_button(self.jcpds_widget.reflections_clear_btn)
        self.assertEqual(len(self.phase_model.phases[5].reflections), 0)
        self.assertEqual(self.jcpds_widget.reflection_table_model.rowCount(), 0)


    @unittest.skip('Does currently not work with pytest running a full suite - needs to be added later again')
    def test_edit_reflection(self):
        col = 0
        row = 1

        previous_d0 = self.phase_model.phases[5].reflections[1].d

        # get x,y position for the cell
        x_pos = self.jcpds_widget.reflection_table_view.columnViewportPosition(col) + 3
        y_pos = self.jcpds_widget.reflection_table_view.rowViewportPosition(row) + 10

        # click then doubleclick  the cell
        self.assertTrue(self.jcpds_widget.reflection_table_view.isVisible())
        viewport = self.jcpds_widget.reflection_table_view.viewport()
        QTest.mouseClick(viewport, QtCore.Qt.LeftButton, pos=QtCore.QPoint(x_pos, y_pos))
        QTest.mouseDClick(viewport, QtCore.Qt.LeftButton, pos=QtCore.QPoint(x_pos, y_pos))

        # type in the new number
        QTest.keyClicks(viewport.focusWidget(), "3")
        QTest.keyPress(viewport.focusWidget(), QtCore.Qt.Key_Enter)
        QtWidgets.QApplication.processEvents()

        self.assertEqual(self.phase_model.phases[5].reflections[1].h, 3)
        print(self.phase_model.phases[5].reflections[1].d)
        self.assertNotEqual(self.phase_model.phases[5].reflections[1].d,
                            previous_d0)

    def test_reload_phase(self):
        num_phase_reflections = len(self.phase_model.phases[5].reflections)
        self.phase_model.delete_reflection(5, 0)
        self.phase_model.delete_reflection(5, 0)
        self.assertEqual(len(self.phase_model.reflections[5]), num_phase_reflections - 2)

        previous_a = self.jcpds_widget.lattice_a_sb.value()
        self.jcpds_widget.lattice_a_sb.setValue(3)

        click_button(self.jcpds_widget.reload_file_btn)

        self.assertEqual(self.jcpds_widget.reflection_table_model.rowCount(), num_phase_reflections)
        self.assertEqual(self.jcpds_widget.lattice_a_sb.value(), previous_a)

    def test_save_as(self):
        filename = os.path.join(jcpds_path, 'dummy.jcpds')
        QtWidgets.QFileDialog.getSaveFileName = MagicMock(return_value=filename)
        click_button(self.jcpds_widget.save_as_btn)
        self.assertEqual(self.jcpds_widget.filename_txt.text(), filename)

    def test_changing_symmetry(self):
        print(self.controller.jcpds_phase.params['symmetry'])
        self.assertTrue(self.jcpds_widget.lattice_a_sb.isEnabled())
        self.assertFalse(self.jcpds_widget.lattice_b_sb.isEnabled())
        self.assertTrue(self.jcpds_widget.lattice_c_sb.isEnabled())

        self.set_symmetry('orthorhombic')
        self.assertEqual(self.controller.jcpds_phase.params['symmetry'], 'ORTHORHOMBIC')
        self.assertTrue(self.jcpds_widget.lattice_a_sb.isEnabled())
        self.assertTrue(self.jcpds_widget.lattice_b_sb.isEnabled())
        self.assertTrue(self.jcpds_widget.lattice_c_sb.isEnabled())

    def test_select_row_in_phase_widget(self):
        self.controller.phase_widget.phase_tw.setRowCount(6)
        self.controller.phase_widget.phase_tw.selectRow(2)
        QtWidgets.QApplication.processEvents()
        self.assertEqual(self.controller.phase_ind, 2)

    def test_editing_the_comments(self):
        enter_value_into_text_field(self.jcpds_widget.comments_txt,
                                    'HAHA this is a phase you will never see in your pattern')
        self.assertEqual(self.controller.jcpds_phase.params['comments'][0],
                         'HAHA this is a phase you will never see in your pattern')

    def test_export_reflection_table(self):
        path = os.path.join(data_path, 'reflection_table.txt')
        self.controller.export_table_data(path)
        with open(path, 'r') as f:
            self.assertEqual(len(f.readlines()), 21)

    def test_copy_complete_reflection_table(self):
        self.controller.reflection_table_key_pressed(QtGui.QKeySequence.SelectAll)
        self.controller.reflection_table_key_pressed(QtGui.QKeySequence.Copy)

        self.assertEqual(QtWidgets.QApplication.clipboard().text().split('\n')[3],
                         '1	0	1	100.00	2.1065	2.1065	8.4396	8.4396	2.9828	2.9828')

        self.jcpds_widget.reflection_table_model.wavelength = None
        self.controller.reflection_table_key_pressed(QtGui.QKeySequence.Copy)
        self.assertEqual(QtWidgets.QApplication.clipboard().text().split('\n')[3],
                         '1	0	1	100.00	2.1065	2.1065')

