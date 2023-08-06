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
from vibrav.base import resource
from vibrav.numerical.boltzmann import boltz_dist
import numpy as np
import pandas as pd
import pytest

temp = 298

part_params = [([2.26248634, 2.26235374, 2.16852056], np.array([65.2308, 65.2461, 76.550]), 3),
               ([3.70139779, 3.70065934, 3.23641988], np.array([65.2308, 65.2461, 76.550]), 50),
               ([1.72983183, 1.72977792, 1.69101661], np.array([65.2308, 65.2461, 76.550]), 2)]

df = pd.read_csv(resource('boltz-dist-full-test.csv.xz'), compression='xz', index_col=False)
boltz_params = [(df.groupby('states').get_group(3), np.array([65.2308, 65.2461, 76.550]), 3),
                (df.groupby('states').get_group(50), np.array([65.2308, 65.2461, 76.550]), 50),
                (df.groupby('states').get_group(2), np.array([65.2308, 65.2461, 76.550]), 2)]

@pytest.mark.parametrize("expected, freq, states", part_params)
def test_partition(expected, freq, states):
    boltz = boltz_dist(energies=freq, temp=temp, states=states)
    assert np.allclose(expected, boltz['partition'].values)

@pytest.mark.parametrize("expected, freq, states", boltz_params)
def test_boltzmann(expected, freq, states):
    test = expected.T.iloc[range(len(freq))]
    boltz = boltz_dist(energies=freq, temp=temp, states=states)
    assert np.allclose(test.values, boltz[range(states)].values)

