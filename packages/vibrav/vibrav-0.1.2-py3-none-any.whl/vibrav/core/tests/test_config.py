# This file is part of vibrav.
#
# vibrav is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# vibrav is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vibrav.  If not, see <https://www.gnu.org/licenses/>.
from vibrav.core.config import Config, MissingRequiredInput
from vibrav.base import resource
import pandas as np
import pytest
import os

def test_config():
    required = {'number_of_multiplicity': int, 'spin_multiplicity': (tuple, int),
                 'number_of_states': (tuple, int), 'number_of_nuclei': int,
                 'number_of_modes': int, 'zero_order_file': str,
                 'oscillator_spin_states': int}
    default= {'sf_energies_file': ('', str), 'so_energies_file': ('', str),
              'angmom_file': ('angmom', str), 'dipole_file': ('dipole', str),
              'spin_file': ('spin', str), 'quadrupole_file': ('quadrupole', str),
              'degen_delta': (1e-5, float)}
    config = Config.open_config(resource('molcas-ucl6-2minus-vibronic-config'), required=required,
                                defaults=default)
    base = {'number_of_multiplicity': 2, 'spin_multiplicity': (3, 1), 'number_of_states': (42, 49),
            'number_of_nuclei': 7, 'number_of_modes': 15, 
            'oscillator_spin_states': 91, 'delta_file': 'delta.dat',
            'reduced_mass_file': 'redmass.dat', 'frequency_file': 'freq.dat',
            'sf_energies_file': 'energies-SF.txt', 'so_energies_file': 'energies.txt',
            'zero_order_file': 'ucl-rassi.out', 'degen_delta': 1e-5,
            'eqcoord_file': 'eqcoord.dat', 'smatrix_file': 'smatrix.dat',
            'atom_order_file': 'atom_order.dat'}
    for key, val in base.items():
        assert val == config[key]
    with pytest.raises(MissingRequiredInput):
        config = Config.open_config(resource('molcas-ucl6-2minus-vibronic-config'),
                                    required={'to_fail': str})

def test_config_resource():
    required = {'number_of_modes': int, 'number_of_nuclei': int, 'property_file': str,
                'gradient_file': str, 'property_atoms': (list, int),
                'property_column': str}
    default = {'smatrix_file': ('smatrix.dat', str), 'eqcoord_file': ('eqcoord.dat', str),
               'atom_order_file': ('atom_order.dat', str)}
    config = Config.open_config(resource('nitromal-zpvc-va.conf'), required=required,
                                defaults=default)
    for key, val in config.items():
        if key.endswith('_file'):
            assert os.path.join('static', 'misc', 'zpvc-test') in val

