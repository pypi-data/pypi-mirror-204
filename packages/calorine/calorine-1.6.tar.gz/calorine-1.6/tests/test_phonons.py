import pytest

import numpy as np
from ase.build import bulk
from ase.calculators.emt import EMT
from calorine.calculators import CPUNEP
from calorine.tools import get_force_constants


@pytest.fixture
def material(request):
    if request.param == 'aluminum':
        structure = bulk('Al', a=4.05, crystalstructure='fcc')
        repeat = [2, 2, 2]
        calculator = EMT()
        bandpath = [[(0, 0, 0), (0.5, 0.5, 0), (0.5, 0.5, 0.5), (0.1, 0.2, 0)]]
        expected = \
            ([0.000000, 0.246914, 0.460747, 0.645520],
             [[0, 0, 0],
              [5.28734914e+00, 5.28734914e+00, 7.99139029e+00],
              [3.30089658e+00, 3.30089658e+00, 7.91878187e+00],
              [2.14406375e+00, 2.35341854e+00, 4.19884865e+00]])
    elif request.param == 'lead_telluride':
        structure = bulk('PbTe', a=5.2, crystalstructure='rocksalt')
        repeat = [2, 2, 2]
        calculator = CPUNEP('tests/nep_models/nep3_v3.3.1_PbTe_Fan22.txt')
        bandpath = [[(0, 0, 0), (0.5, 0.5, 0), (0.5, 0.5, 0.5), (0.1, 0.2, 0)]]
        expected = \
            ([0.000000, 0.192308, 0.358851, 0.502761],
             [[-4.01167092e+00, -4.01167092e+00, -4.01167092e+00,
               2.63906328e-04, 2.63906336e-04, 2.63906338e-04],
              [-3.38462560e+00, -2.81849989e+00, -2.81849989e+00,
               -2.23935109e+00, -2.23935109e+00,  1.37130908e+00],
              [-2.07473436e+00, -1.32600081e+00, -1.32600081e+00,
               -1.15659000e+00, -1.15659000e+00,  1.50710525e+00],
              [-3.64935617e+00, -3.56129938e+00, -3.55761822e+00,
               4.87919688e-01, 5.60728777e-01, 1.23896629e+00]])
    return structure, calculator, repeat, bandpath, expected


@pytest.mark.parametrize(
    'material',
    [
        ('aluminum'),
        ('lead_telluride'),
    ],
    indirect=['material']
)
def test_get_force_constants_via_dispersion(material):
    structure, calculator, repeat, bandpath, (qpt_lin, frequencies) = material
    phonon = get_force_constants(structure, calculator, repeat)
    phonon.run_band_structure(bandpath)
    band = phonon.get_band_structure_dict()
    assert np.allclose(band['distances'], qpt_lin, atol=1e-6)
    assert np.allclose(band['frequencies'][0], frequencies, atol=1e-4)
