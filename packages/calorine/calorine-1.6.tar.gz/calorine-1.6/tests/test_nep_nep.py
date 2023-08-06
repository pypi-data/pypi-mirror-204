import pytest
import numpy as np
from ase import Atoms
from ase.io import read
from calorine.nep.nep import get_descriptors, get_dipole, get_latent_space, \
        get_potential_forces_and_virials, _clean_tmp_dir


@pytest.fixture
def PbTe():
    return Atoms('TePb', positions=[(0, 0, 0), (0, 0.0, 1.1)],
                 cell=([100, 0, 0], [0, 100, 0], [0, 0, 100]))


@pytest.fixture
def C():
    return Atoms('C', positions=[(0, 0, 0)])


@pytest.fixture
def CC():
    return Atoms('CC', positions=[(0, 0, 0), (0, 0.0, 1.1)])


@pytest.fixture
def CO():
    return Atoms('CO', positions=[(0, 0, 0), (0, 0.0, 1.1)])


@pytest.fixture
def CON():
    return Atoms('CON', positions=[(0, 0, 0), (0, 0.0, 1.1), (0, 0.0, 2.2)])


def get_expected(path):
    """Load forces or virials from file"""
    return np.loadtxt(path)


def _load_nep_from_file(file: str) -> str:
    """Load a NEP model from file into a stringified version

    Parameters
    ----------
    file
        Path to nep.txt.

    Returns
    -------
    str
        Stringified NEP model.
    """
    with open(file, 'r') as f:
        model = f.read()
    return model


# --- get_descriptors ---
def test_get_descriptors_setup_dummy_NEP2_model(PbTe):
    """Verifies the dummy NEP model is properly formatted."""
    get_descriptors(PbTe, debug=True)
    tmp_dir = './tmp_nepy/'
    PbTe_dummy = _load_nep_from_file(f'{tmp_dir}/nep.txt')
    _clean_tmp_dir(tmp_dir)
    expected_PbTe_dummy = _load_nep_from_file(
        'tests/nep_models/PbTe_NEP2_dummy.txt')
    assert PbTe_dummy == expected_PbTe_dummy


def test_get_descriptors_no_cell(CO):
    """Should get descriptors for atoms without a specified cell, and raise a warning."""
    with pytest.warns(UserWarning) as record:
        descriptors = get_descriptors(CO)
    assert len(record) == 1
    assert record[0].message.args[0] == 'Using default unit cell (cubic with side 100 Å).'
    assert descriptors.shape == (2, 52)


def test_get_descriptors_NEP2_independent_of_species(PbTe, CO):
    """NEP2 should give the same descriptors regardless of atom species."""
    descriptors_PbTe = get_descriptors(PbTe)
    descriptors_CO = get_descriptors(CO)
    assert np.allclose(descriptors_CO, descriptors_PbTe, atol=1e-12, rtol=0)


def test_get_descriptors_NEP2_several_atoms_same_species(CC):
    """NEP2 should get the descritors for a single component system"""
    descriptors_CC = get_descriptors(CC)
    assert descriptors_CC.shape == (2, 52)
    assert descriptors_CC.dtype == np.float64
    assert not np.all(np.isclose(descriptors_CC, 0))


def test_get_descriptors_dummy_NEP2_several_atom_species(C, CO, CON):
    """Verifies the dummy NEP model has the correct number of parameters."""
    # C
    get_descriptors(C, debug=True)
    tmp_dir = './tmp_nepy/'
    C_dummy_parameters = _load_nep_from_file(f'{tmp_dir}/nep.txt').split('\n')[6:]
    _clean_tmp_dir(tmp_dir)
    assert len(C_dummy_parameters) == 1698
    # CO
    get_descriptors(CO, debug=True)
    tmp_dir = './tmp_nepy/'
    CO_dummy_parameters = _load_nep_from_file(f'{tmp_dir}/nep.txt').split('\n')[6:]
    _clean_tmp_dir(tmp_dir)
    assert len(CO_dummy_parameters) == 1773
    # CON
    get_descriptors(CON, debug=True)
    tmp_dir = './tmp_nepy/'
    CON_dummy_parameters = _load_nep_from_file(f'{tmp_dir}/nep.txt').split('\n')[6:]
    _clean_tmp_dir(tmp_dir)
    assert len(CON_dummy_parameters) == 1898


def test_get_descriptors_NEP2_dummy(PbTe):
    """Case: No NEP model supplied; using dummy NEP2 model.
       Compares results to output from `nep_cpu`
    """
    descriptors_PbTe = get_descriptors(PbTe)
    expected_PbTe = np.loadtxt(
        'tests/example_output/PbTe_NEP2_dummy_PbTe_2atom_descriptor.out')
    assert np.allclose(descriptors_PbTe, expected_PbTe, atol=1e-12, rtol=0)


def test_get_descriptors_NEP3(PbTe):
    """Case: NEP3 model supplied. Compares results to output from `nep_cpu`"""
    nep3 = 'tests/nep_models/nep3_v3.3.1_PbTe_Fan22.txt'
    descriptors_PbTe = get_descriptors(PbTe, potential_filename=nep3)
    expected_PbTe = np.loadtxt(
        'tests/example_output/nep3_v3.3.1_PbTe_Fan22_PbTe_2atom_descriptor.out')
    assert np.allclose(descriptors_PbTe, expected_PbTe, atol=1e-12, rtol=0)


def test_get_descriptors_debug(PbTe):
    """Check that the generated files are accessible in the debug directory"""
    get_descriptors(PbTe, debug=True)
    tmp_dir = './tmp_nepy/'
    PbTe_dummy = _load_nep_from_file(f'{tmp_dir}/nep.txt')
    _clean_tmp_dir(tmp_dir)
    assert 'nep 2 Te Pb' in PbTe_dummy


def test_get_descriptors_debug_directory_exists(PbTe):
    """Should fail if debug directory already exists from an earlier calculation"""
    get_descriptors(PbTe, debug=True)
    tmp_dir = './tmp_nepy/'
    with pytest.raises(FileExistsError)as e:
        get_descriptors(PbTe, debug=True)
    assert 'Please delete or move the conflicting directory' in str(e)
    _clean_tmp_dir(tmp_dir)


# --- get_potential_forces_and_virials ---
def test_get_potential_forces_and_virials_NEP3(PbTe):
    """Case: NEP3 model supplied. Compares results to output from `nep_cpu`"""
    nep3 = 'tests/nep_models/nep3_v3.3.1_PbTe_Fan22.txt'
    energies, forces, virials = get_potential_forces_and_virials(
        PbTe, potential_filename=nep3)

    expected_forces = get_expected(
        'tests/example_output/nep3_v3.3.1_PbTe_Fan22_PbTe_2atom_force.out')
    expected_virials = get_expected(
        'tests/example_output/nep3_v3.3.1_PbTe_Fan22_PbTe_2atom_virial.out')

    assert energies.shape == (2,)
    assert forces.shape == (2, 3)
    assert virials.shape == (2, 9)
    assert np.allclose(forces, expected_forces, atol=1e-12, rtol=0)
    assert np.allclose(virials, expected_virials, atol=1e-12, rtol=0)


def test_get_potential_forces_and_virials_NEP3_debug(PbTe):
    """Compares result with debug flag enabled."""
    nep3 = 'tests/nep_models/nep3_v3.3.1_PbTe_Fan22.txt'
    energies, forces, virials = get_potential_forces_and_virials(
        PbTe, potential_filename=nep3, debug=True)

    expected_forces = get_expected(
        'tests/example_output/nep3_v3.3.1_PbTe_Fan22_PbTe_2atom_force.out')
    expected_virials = get_expected(
        'tests/example_output/nep3_v3.3.1_PbTe_Fan22_PbTe_2atom_virial.out')

    assert energies.shape == (2,)
    assert forces.shape == (2, 3)
    assert virials.shape == (2, 9)
    assert np.allclose(forces, expected_forces, atol=1e-12, rtol=0)
    assert np.allclose(virials, expected_virials, atol=1e-12, rtol=0)


def test_get_potential_forces_and_virials_dummy_NEP2(CO):
    """Dummy NEP2 model supplied. Compares results to output from `nep_cpu` for another system"""
    nep2_dummy = 'tests/nep_models/CO_NEP2_dummy.txt'
    energies, forces, virials = get_potential_forces_and_virials(
        CO, potential_filename=nep2_dummy)

    expected_forces = get_expected('tests/example_output/CO_NEP2_dummy_CO_2atom_force.out')
    expected_virials = get_expected('tests/example_output/CO_NEP2_dummy_CO_2atom_virial.out')

    assert energies.shape == (2,)
    assert forces.shape == (2, 3)
    assert virials.shape == (2, 9)
    assert np.allclose(forces, expected_forces, atol=1e-12, rtol=0)
    assert np.allclose(virials, expected_virials, atol=1e-12, rtol=0)


def test_get_potential_forces_and_virials_no_cell(CO):
    """Should work with default cell if no cell is supplied"""
    nep2_dummy = 'tests/nep_models/CO_NEP2_dummy.txt'
    with pytest.warns(UserWarning) as record:
        energies, forces, virials = get_potential_forces_and_virials(
            CO, potential_filename=nep2_dummy)

    expected_forces = get_expected('tests/example_output/CO_NEP2_dummy_CO_2atom_force.out')
    expected_virials = get_expected('tests/example_output/CO_NEP2_dummy_CO_2atom_virial.out')

    assert len(record) == 1
    assert record[0].message.args[0] == 'Using default unit cell (cubic with side 100 Å).'
    assert energies.shape == (2,)
    assert forces.shape == (2, 3)
    assert virials.shape == (2, 9)
    assert np.allclose(forces, expected_forces, atol=1e-12, rtol=0)
    assert np.allclose(virials, expected_virials, atol=1e-12, rtol=0)


def test_get_potential_forces_and_virials_several_of_same_species(CC):
    """Check that forces are correct for a CC system"""
    nep = 'tests/nep_models/C_NEP2_dummy.txt'
    energies, forces, virials = get_potential_forces_and_virials(
        CC, potential_filename=nep)

    expected_forces = get_expected('tests/example_output/C_NEP2_dummy_C_2atom_force.out')
    expected_virials = get_expected('tests/example_output/C_NEP2_dummy_C_2atom_virial.out')

    assert energies.shape == (2,)
    assert forces.shape == (2, 3)
    assert virials.shape == (2, 9)
    assert np.allclose(forces, expected_forces, atol=1e-12, rtol=0)
    assert np.allclose(virials, expected_virials, atol=1e-12, rtol=0)


def test_get_potential_forces_and_virials_several_different_species(CON):
    """Check that forces are correct for a CON system.
    Note that these forces should be exactly zero for this system
    since the NEP2 dummy potential treats all atom species as identical atm.
    """
    nep = 'tests/nep_models/CON_NEP2_dummy.txt'
    energies, forces, virials = get_potential_forces_and_virials(
        CON, potential_filename=nep)

    expected_forces = get_expected('tests/example_output/CON_NEP2_dummy_CON_3atom_force.out')
    expected_virials = get_expected('tests/example_output/CON_NEP2_dummy_CON_3atom_virial.out')

    assert energies.shape == (3,)
    assert forces.shape == (3, 3)
    assert virials.shape == (3, 9)

    assert np.allclose(forces, expected_forces, atol=1e-12, rtol=0)
    assert np.allclose(forces, np.zeros((3, 3)), atol=1e-12, rtol=0)
    assert np.allclose(virials, expected_virials, atol=1e-12, rtol=0)
    assert np.allclose(virials, np.zeros((3, 9)), atol=1e-12, rtol=0)


def test_get_potential_forces_and_virials_no_potential(PbTe):
    """Tries to get potentials, forces and virials without specifying potential"""
    with pytest.raises(ValueError)as e:
        get_potential_forces_and_virials(PbTe)
    assert 'Potential must be defined!' in str(e)


# --- get_dipole ---
def test_get_dipole_NEP3():
    """Case: NEP3 model supplied. Compares results to output from DFT."""
    nep3 = 'tests/nep_models/nep4_dipole_Christian.txt'
    structure = read('tests/example_files/dipole/test.xyz')

    dipole = get_dipole(structure, potential_filename=nep3)
    dft_dipole = structure.info['dipole']
    delta = dipole - dft_dipole
    assert dipole.shape == (3,)
    assert np.allclose([-0.07468218, -0.03891397, -0.11160894], delta, atol=1e-12, rtol=1e-5)


def test_get_dipole_no_potential(PbTe):
    """Tries to get dipole without specifying potential"""
    with pytest.raises(ValueError)as e:
        get_dipole(PbTe)
    assert 'Potential must be defined!' in str(e)


# --- get_latent_space ---
def test_get_latent_space_NEP3(PbTe):
    """Case: NEP3 model supplied. Returns a latent space with expected shape."""
    nep3 = 'tests/nep_models/nep3_v3.3.1_PbTe_Fan22.txt'
    latent = get_latent_space(PbTe, potential_filename=nep3)
    assert latent.shape == (2, 30)


def test_get_latent_space_no_potential(PbTe):
    """Tries to get latent space without specifying potential"""
    with pytest.raises(ValueError)as e:
        get_latent_space(PbTe)
    assert 'Potential must be defined!' in str(e)
