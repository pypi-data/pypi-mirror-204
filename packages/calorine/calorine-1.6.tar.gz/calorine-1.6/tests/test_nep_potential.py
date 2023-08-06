import pytest
import numpy as np
import tempfile
from ase.build import bulk
from calorine.calculators import CPUNEP
from calorine.nep import read_potential


def test_read_potential_case1():
    """Reads a NEP3 nep.txt file"""
    potential = read_potential('tests/example_files/nep.txt')
    assert potential.zbl == (1, 2)
    assert potential.radial_cutoff == 8
    assert potential.angular_cutoff == 4
    assert potential.n_max_radial == 4
    assert potential.n_max_angular == 4
    assert potential.l_max_3b == 4
    assert potential.l_max_4b == 2
    assert potential.l_max_5b == 0
    assert potential.n_basis_radial == 8
    assert potential.n_basis_angular == 8
    assert potential.n_neuron == 30


def test_read_potential_case2():
    """Reads a NEP3 nep.txt file"""
    potential = read_potential('tests/nep_models/CsPbI3-SCAN.txt')
    assert potential.radial_cutoff == 8
    assert potential.angular_cutoff == 4
    assert potential.max_neighbors_radial == 74
    assert potential.max_neighbors_angular == 14
    assert potential.n_max_radial == 8
    assert potential.n_max_angular == 6
    assert potential.l_max_3b == 4
    assert potential.l_max_4b == 0
    assert potential.l_max_5b == 0
    assert potential.n_basis_radial == 8
    assert potential.n_basis_angular == 8
    assert potential.n_neuron == 50


def test_read_potential_case3():
    """Reads a NEP4 nep.txt file"""
    potential = read_potential('tests/nep_models/nep4_PbTe.txt')
    assert potential.radial_cutoff == 8
    assert potential.angular_cutoff == 4
    assert potential.max_neighbors_radial == 74
    assert potential.max_neighbors_angular == 10
    assert potential.n_max_radial == 4
    assert potential.n_max_angular == 4
    assert potential.l_max_3b == 4
    assert potential.l_max_4b == 2
    assert potential.l_max_5b == 0
    assert potential.n_basis_radial == 8
    assert potential.n_basis_angular == 8
    assert potential.n_neuron == 30


@pytest.mark.parametrize('nep_file',
                         ['tests/example_files/nep.txt',
                          'tests/nep_models/nep4_PbTe.txt'
                          ])
def test_potential_read_and_write_case1(nep_file):
    """
    Reads and rewrites a NEP nep.txt file, and verifies that
    the energies are consistent.

    Test is performed both with a NEP3 and a NEP4 potential.
    """
    def get_energies(confs, fname):
        energies = []
        for conf in confs:
            conf.calc = CPUNEP(fname)
            energies.append(conf.get_potential_energy())
        return np.array(energies)

    confs = []
    confs.append(bulk('Pb', crystalstructure='fcc', a=4))
    confs.append(bulk('Te', crystalstructure='fcc', a=4))

    fname = nep_file
    ref_data = get_energies(confs, fname)

    potential = read_potential(fname)
    with tempfile.NamedTemporaryFile() as tmp:
        potential.write(tmp.name)
        new_data = get_energies(confs, tmp.name)
    assert np.allclose(new_data, ref_data)

    potential = read_potential(fname)
    potential.types = ['Te', 'Pb']
    with tempfile.NamedTemporaryFile() as tmp:
        potential.write(tmp.name)
        new_data = get_energies(confs, tmp.name)
    assert np.allclose(new_data, ref_data)


def test_potential_read_and_write_case2():
    """Reads a NEP3 nep.txt file"""
    def get_energies(confs, fname):
        energies = []
        for conf in confs:
            conf.calc = CPUNEP(fname)
            energies.append(conf.get_potential_energy())
        return np.array(energies)

    confs = []
    confs.append(bulk('Cs', crystalstructure='fcc', a=4))
    confs.append(bulk('Pb', crystalstructure='fcc', a=4))
    confs.append(bulk('I', crystalstructure='fcc', a=4))

    fname = 'tests/nep_models/CsPbI3-SCAN.txt'
    ref_data = get_energies(confs, fname)

    potential = read_potential(fname)
    with tempfile.NamedTemporaryFile() as tmp:
        potential.write(tmp.name)
        new_data = get_energies(confs, tmp.name)
    assert np.allclose(new_data, ref_data)

    potential = read_potential(fname)
    potential.types = ['I', 'Cs', 'Pb']
    with tempfile.NamedTemporaryFile() as tmp:
        potential.write(tmp.name)
        new_data = get_energies(confs, tmp.name)
    assert np.allclose(new_data, ref_data)


def test_potential_str():
    fname = 'tests/nep_models/CsPbI3-SCAN.txt'
    potential = read_potential(fname)
    s = str(potential)
    for fld in ['radial_cutoff', 'angular_cutoff', 'max_neighbors_radial',
                'max_neighbors_angular', 'n_max_radial', 'l_max', 'n_neuron']:
        assert fld in s


@pytest.mark.parametrize('nep_file',
                         ['tests/nep_models/CsPbI3-SCAN.txt',
                          'tests/nep_models/nep4_PbTe.txt'
                          ])
def test_potential_repr_html_(nep_file):
    fname = nep_file
    potential = read_potential(fname)
    s = potential._repr_html_()
    for fld in ['radial_cutoff', 'angular_cutoff', 'max_neighbors_radial',
                'max_neighbors_angular', 'n_max_radial', 'l_max', 'n_neuron']:
        assert fld in s


def test_read_malformed_potential(tmp_path):
    """Should fail, raising an IOError."""
    p = tmp_path / "nep.txt"
    rows = [str(i) for i in range(7)]
    rows.append('invalid parameter')
    text = '\n'.join(rows)
    p.write_text(text)
    with pytest.raises(IOError) as e:
        read_potential(p)
    assert 'Failed to parse line 7 from' in str(e)


def test_read_invalid_keyword(tmp_path):
    """Should fail, raising a ValueError."""
    p = tmp_path / "nep.txt"
    p.write_text('unknown\n')
    with pytest.raises(ValueError) as e:
        read_potential(p)
    assert 'Unknown field: unknown' in str(e)
