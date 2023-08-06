from dataclasses import dataclass
from itertools import product
from typing import Dict, List, Tuple
import numpy as np


@dataclass
class Potential:
    """Objects of this class represent a NEP model in a form suitable for
    inspection and manipulation. Typically a :class:`Potential` object is instantiated
    by calling the :func:`read_potential <calorine.nep.read_potential>` function.

    Attributes
    ----------
    version : int
        NEP version
    types
        chemical species that this model represents
    radial_cutoff : float
        the radial cutoff parameter in Å
    angular_cutoff : float
        the angular cutoff parameter in Å
    max_neighbors_radial : int
        maximum number of neighbors in neighbor list for radial terms
    max_neighbors_angular : int
        maximum number of neighbors in neighbor list for angular terms
    zbl : Tuple[float, float]
        inner and outer cutoff for transition to ZBL potential
    n_basis_radial : int
        number of radial basis functions :math:`n_\\mathrm{basis}^\\mathrm{R}`
    n_basis_angular : int
        number of angular basis functions :math:`n_\\mathrm{basis}^\\mathrm{A}`
    n_max_radial : int
        maximum order of Chebyshev polymonials included in
        radial expansion :math:`n_\\mathrm{max}^\\mathrm{R}`
    n_max_angular : int
        maximum order of Chebyshev polymonials included in
        angular expansion :math:`n_\\mathrm{max}^\\mathrm{A}`
    l_max_3b : int
        maximum expansion order for three-body terms :math:`l_\\mathrm{max}^\\mathrm{3b}`
    l_max_4b : int
        maximum expansion order for four-body terms :math:`l_\\mathrm{max}^\\mathrm{4b}`
    l_max_5b : int
        maximum expansion order for five-body terms :math:`l_\\mathrm{max}^\\mathrm{5b}`
    n_descriptor_radial : int
        dimension of radial part of descriptor
    n_descriptor_angular : int
        dimension of angular part of descriptor
    n_neuron : int
        number of neurons in hidden layer
    n_parameters : int
        total number of parameters including scalers (which are not fit parameters)
    ann_parameters : Dict[Tuple[str, Dict[str, np.darray]]]
        neural network weights
    q_scaler : List[float]
        scaling parameters
    radial_descriptor_weights : Dict[Tuple[str, str], np.ndarray]
        radial descriptor weights by combination of species; the array for each combination
        has dimensions of
        :math:`(n_\\mathrm{max}^\\mathrm{R}+1) \\times (n_\\mathrm{basis}^\\mathrm{R}+1)`
    angular_descriptor_weights : Dict[Tuple[str, str], np.ndarray]
        angular descriptor weights by combination of species; the array for each combination
        has dimensions of
        :math:`(n_\\mathrm{max}^\\mathrm{A}+1) \\times (n_\\mathrm{basis}^\\mathrm{A}+1)`
    """

    version: int
    types: Tuple[str, ...]

    radial_cutoff: float
    angular_cutoff: float

    n_basis_radial: int
    n_basis_angular: int
    n_max_radial: int
    n_max_angular: int
    l_max_3b: int
    l_max_4b: int
    l_max_5b: int
    n_descriptor_radial: int
    n_descriptor_angular: int

    n_neuron: int
    n_parameters: int
    ann_parameters: Dict[str, Dict[str, np.ndarray]]
    q_scaler: List[float]
    radial_descriptor_weights: Dict[Tuple[str, str], np.ndarray]
    angular_descriptor_weights: Dict[Tuple[str, str], np.ndarray]

    zbl: Tuple[float, float] = None
    max_neighbors_radial: int = None
    max_neighbors_angular: int = None

    _special_fields = ['ann_parameters', 'q_scaler',
                       'radial_descriptor_weights', 'angular_descriptor_weights']

    def __str__(self) -> str:
        s = []
        for fld in self.__dataclass_fields__:
            if fld not in self._special_fields:
                s += [f'{fld:22} : {getattr(self, fld)}']
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        s = []
        s += ['<table border="1" class="dataframe"']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Value</th></tr></thead>']
        s += ['<tbody>']
        for fld in self.__dataclass_fields__:
            if fld not in self._special_fields:
                s += [f'<tr><td style="text-align: left;">{fld:22}</td>'
                      f'<td>{getattr(self, fld)}</td><tr>']
        for fld in self._special_fields:
            d = getattr(self, fld)
            if fld.endswith('descriptor_weights'):
                dim = list(d.values())[0].shape
            if fld == 'ann_parameters' and self.version == 4:
                dim = (len(self.types), len(list(d.values())[0]))
            else:
                dim = len(d)
            s += [f'<tr><td style="text-align: left;">Dimension of {fld:22}</td><td>{dim}</td><tr>']
        s += ['</tbody>']
        s += ['</table>']
        return ''.join(s)

    def write(self, filename: str) -> None:
        """Write NEP model to file in `nep.txt` format.
        """
        with open(filename, 'w') as f:
            # header
            version_name = f'nep{self.version}'
            if self.zbl is not None:
                version_name += '_zbl'
            f.write(f'{version_name} {len(self.types)} {" ".join(self.types)}\n')
            if self.zbl is not None:
                f.write(f'zbl {" ".join(map(str, self.zbl))}\n')
            f.write(f'cutoff {self.radial_cutoff} {self.angular_cutoff}')
            if self.max_neighbors_radial is not None and self.max_neighbors_angular is not None:
                f.write(f' {self.max_neighbors_radial} {self.max_neighbors_angular}')
            f.write('\n')
            f.write(f'n_max {self.n_max_radial} {self.n_max_angular}\n')
            f.write(f'basis_size {self.n_basis_radial} {self.n_basis_angular}\n')
            f.write(f'l_max {self.l_max_3b} {self.l_max_4b} {self.l_max_5b}\n')
            f.write(f'ANN {self.n_neuron} 0\n')

            # neural network weights
            keys = self.types if self.version == 4 else ['all_species']
            for s in keys:
                # Order: w0, b0, w1
                # w0 indexed as: n*N_descriptor + nu
                w0 = self.ann_parameters[s]['w0']
                b0 = self.ann_parameters[s]['b0']
                w1 = self.ann_parameters[s]['w1']
                for n in range(self.n_neuron):
                    for nu in range(self.n_descriptor_radial+self.n_descriptor_angular):
                        f.write(f'{w0[n, nu]:15.7e}\n')
                for b in b0[:, 0]:
                    f.write(f'{b:15.7e}\n')
                for v in w1[0, :]:
                    f.write(f'{v:15.7e}\n')
            f.write(f'{self.ann_parameters["b1"]:15.7e}\n')

            # descriptor weights
            mat = []
            for s1 in self.types:
                for s2 in self.types:
                    mat = np.hstack([mat, self.radial_descriptor_weights[(s1, s2)].flatten()])
                    mat = np.hstack([mat, self.angular_descriptor_weights[(s1, s2)].flatten()])
            n_types = len(self.types)
            n = int(len(mat) / (n_types * n_types))
            mat = mat.reshape((n_types * n_types, n)).T
            for v in mat.flatten():
                f.write(f'{v:15.7e}\n')

            # scaler
            for v in self.q_scaler:
                f.write(f'{v:15.7e}\n')


def read_potential(filename: str) -> Potential:
    """Parses a file in ``nep.txt`` format from GPUMD and returns the
    content in the form of a :class:`Potential <calorine.nep.potential.Potential>`
    object.

    Parameters
    ----------
    filename
        input file name
    """

    # parse file and split header and parameters
    header = []
    parameters = []
    nheader = 6
    with open(filename) as f:
        for k, line in enumerate(f.readlines()):
            flds = line.split()
            assert len(flds) != 0, f'Empty line number {k}'
            if k == 0 and 'zbl' in flds[0]:
                nheader += 1
            if k < nheader:
                header.append(tuple(flds))
            elif len(flds) == 1:
                parameters.append(float(flds[0]))
            else:
                raise IOError(f'Failed to parse line {k} from {filename}')

    # compile data from the header into a dict
    data = {}
    for flds in header:
        if flds[0] in ['cutoff']:
            data[flds[0]] = tuple(map(float, flds[1:]))
        elif flds[0] in ['zbl', 'n_max', 'l_max', 'ANN', 'basis_size']:
            data[flds[0]] = tuple(map(int, flds[1:]))
        elif flds[0].startswith('nep'):
            data['version'] = int(flds[0].replace('nep', '').split('_')[0])
            data['types'] = flds[2:]
        else:
            raise ValueError(f'Unknown field: {flds[0]}')

    # sanity checks
    for fld in ['cutoff', 'basis_size', 'n_max', 'l_max', 'ANN']:
        assert fld in data, f'Invalid potential file; {fld} line is missing'
    assert data['version'] in [3, 4], \
        'Invalid potential files; only NEP versions 3 and 4 are currently supported'

    # split up cutoff tuple
    assert len(data['cutoff']) in [2, 4]
    data['radial_cutoff'] = data['cutoff'][0]
    data['angular_cutoff'] = data['cutoff'][1]
    if len(data['cutoff']) == 4:
        data['max_neighbors_radial'] = int(data['cutoff'][2])
        data['max_neighbors_angular'] = int(data['cutoff'][3])
    del data['cutoff']

    # split up basis_size tuple
    assert len(data['basis_size']) == 2
    data['n_basis_radial'] = data['basis_size'][0]
    data['n_basis_angular'] = data['basis_size'][1]
    del data['basis_size']

    # split up n_max tuple
    assert len(data['n_max']) == 2
    data['n_max_radial'] = data['n_max'][0]
    data['n_max_angular'] = data['n_max'][1]
    del data['n_max']

    # split up nl_max tuple
    len_l = len(data['l_max'])
    assert len_l in [1, 2, 3]
    data['l_max_3b'] = data['l_max'][0]
    data['l_max_4b'] = data['l_max'][1] if len_l > 1 else 0
    data['l_max_5b'] = data['l_max'][2] if len_l > 2 else 0
    del data['l_max']

    # compute dimensions of descriptor components
    data['n_descriptor_radial'] = data['n_max_radial'] + 1
    l_max_enh = data['l_max_3b'] + (data['l_max_4b'] > 0) + (data['l_max_5b'] > 0)
    data['n_descriptor_angular'] = (data['n_max_angular'] + 1) * l_max_enh
    n_descriptor = data['n_descriptor_radial'] + data['n_descriptor_angular']

    # compute number of parameters
    data['n_neuron'] = data['ANN'][0]
    del data['ANN']
    n_types = len(data['types'])
    if data['version'] == 3:
        n = 1
    else:  # version 4
        # one hidden layer per atomic species
        n = n_types
    n_ann_input_weights = (n_descriptor + 1) * data['n_neuron']  # weights + bias
    n_ann_output_weights = data['n_neuron']  # only weights
    n_ann_parameters = (n_ann_input_weights + n_ann_output_weights) * n + 1  # + single output bias

    n_descriptor_weights = n_types ** 2 * (
        (data['n_max_radial'] + 1) * (data['n_basis_radial'] + 1) +
        (data['n_max_angular'] + 1) * (data['n_basis_angular'] + 1)
    )
    data['n_parameters'] = n_ann_parameters + n_descriptor_weights + n_descriptor
    assert data['n_parameters'] == len(parameters), \
        'Parsing of parameters inconsistent; please submit a bug report'

    # split up parameters into the ANN weights, descriptor weights, and scaling parameters
    n1 = n_ann_parameters
    n2 = n1 + n_descriptor_weights
    data['ann_parameters'] = parameters[:n1]
    descriptor_weights = np.array(parameters[n1:n2])
    data['q_scaler'] = parameters[n2:]

    # Group ANN parameters into
    pars = {}
    n1 = 0
    n_network_params = n_ann_input_weights + n_ann_output_weights  # except last bias
    n_neuron = data['n_neuron']
    keys = data['types'] if data['version'] == 4 else ['all_species']

    for s in keys:
        # Get the parameters for the ANN; in the case of NEP4, there is effectively
        # one network per atomic species.
        ann_parameters = data['ann_parameters'][n1:n1+n_network_params]

        ann_input_weights = ann_parameters[:n_ann_input_weights]
        w0 = np.zeros((n_neuron, n_descriptor))
        b0 = np.zeros((n_neuron, 1))
        for n in range(n_neuron):
            for nu in range(n_descriptor):
                w0[n, nu] = ann_input_weights[n*n_descriptor+nu]
        b0[:, 0] = ann_input_weights[n_neuron*n_descriptor:]

        assert np.all(w0.shape == (n_neuron, n_descriptor)), \
            f'w0 has invalid shape for key {s}; please submit a bug report'
        assert np.all(b0.shape == (n_neuron, 1)), \
            f'b0 has invalid shape for key {s}; please submit a bug report'
        assert np.all(w0), \
            f'some weights in w0 are zero for key {s}; please submit a bug report'
        assert np.all(b0), \
            f'some weights in b0 are zero for key {s}; please submit a bug report'

        ann_output_weights = ann_parameters[n_ann_input_weights:
                                            n_ann_input_weights+n_ann_output_weights]

        w1 = np.zeros((1, n_neuron))
        w1[0, :] = ann_output_weights[:]
        assert np.all(w1.shape == (1, n_neuron)), \
            f'w1 has invalid shape for key {s}; please submit a bug report'
        assert np.all(w1), \
            f'some weights in w1 are zero for key {s}; please submit a bug report'

        pars[s] = {
            'w0': w0,
            'b0': b0,
            'w1': w1,
        }
        n1 += n_network_params
    pars['b1'] = data['ann_parameters'][n1]

    sum = 0
    for s in pars.keys():
        if s == 'b1':
            sum += 1
        else:
            sum += np.sum([np.count_nonzero(p) for p in pars[s].values()])
    assert sum == n_ann_parameters, \
        'Inconsistent number of parameters accounted for; please submit a bug report'
    data['ann_parameters'] = pars

    # split up descriptor by chemical species and radial/angular
    n = int(len(descriptor_weights) / (n_types * n_types))
    n_max_radial = data['n_max_radial']
    n_max_angular = data['n_max_angular']
    n_basis_radial = data['n_basis_radial']
    n_basis_angular = data['n_basis_angular']
    m = (n_max_radial + 1) * (n_basis_radial + 1)
    descriptor_weights = descriptor_weights.reshape((n, n_types * n_types)).T
    descriptor_weights_radial = descriptor_weights[:, :m]
    descriptor_weights_angular = descriptor_weights[:, m:]

    # add descriptors to data dict
    data['radial_descriptor_weights'] = {}
    data['angular_descriptor_weights'] = {}
    m = -1
    for i, j in product(range(n_types), repeat=2):
        m += 1
        s1, s2 = data['types'][i], data['types'][j]
        subdata = descriptor_weights_radial[m, :].reshape(
            (n_max_radial + 1, n_basis_radial + 1))
        data['radial_descriptor_weights'][(s1, s2)] = subdata
        subdata = descriptor_weights_angular[m, :].reshape(
            (n_max_angular + 1, n_basis_angular + 1))
        data['angular_descriptor_weights'][(s1, s2)] = subdata

    return Potential(**data)
