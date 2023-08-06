# -*- coding: utf-8 -*-

"""CPU strain energy evaluator implementation.

"""

from json import loads
from logging import getLogger
from multiprocessing import Pool, RawArray
from os import cpu_count
from time import time

import matplotlib.pyplot as plt
import numpy as np

from numlpa import config
from . import energy


logger = getLogger(__package__)

shared = {}


def evaluate(sample, **kwargs):
    """Return the strain energy evaluation.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.

    Keyword Arguments
    -----------------
    type : str
        Dislocation type ('screw' or 'edge').
    b_uvw : tuple of int
        Direction of the Burgers vector (uvw).
    cell : float
        Lattice constant (m).
    poisson : float
        Poisson number.
    shear : float
        Shear modulus (Pa).
    core : float
        Absolute or relative value of the core radius (1|m).
    absolute : bool
        If true, the core parameter becomes an absolute value.
    replicate : int
        Number of replications of the region of interest.
    points : int
        Number of random points.
    processes : int
        Number of parallel processes.
    check : bool
        Display random points and replicated dislocations.

    Returns
    -------
    dict
        Energy evaluation data.

    """
    settings = {}
    share = {}
    times = {}
    result = {}

    check_parameters(kwargs)
    prepare_settings(sample, kwargs, settings)
    prepare_shared_data(sample, settings, share)
    user_check(settings, share, kwargs)
    run_monte_carlo(settings, share, result, times)
    return assemble_data(sample, settings, kwargs, result, times)


def check_parameters(kwargs):
    """Set the default configuration value to missing parameters.

    Parameters
    ----------
    kwargs : dict
        Keyword arguments passed to the main function.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('type', config.get(__package__, 'type'))
    kwargs.setdefault('b_uvw', loads(config.get(__package__, 'b_uvw')))
    kwargs.setdefault('cell', config.getfloat(__package__, 'cell'))
    kwargs.setdefault('poisson', config.getfloat(__package__, 'poisson'))
    kwargs.setdefault('shear', config.getfloat(__package__, 'shear'))
    kwargs.setdefault('core', config.getfloat(__package__, 'core'))
    kwargs.setdefault('absolute', config.getboolean(__package__, 'absolute'))
    kwargs.setdefault('replicate', config.getint(__package__, 'replicate'))
    kwargs.setdefault('points', config.getint(__package__, 'points'))
    kwargs.setdefault('processes', config.getint(__package__, 'processes'))
    kwargs.setdefault('check', config.getboolean(__package__, 'check'))
    if kwargs['processes'] < 1:
        kwargs['processes'] = cpu_count()


def prepare_settings(sample, kwargs, settings):
    """Prepare the evaluation variables.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.
    kwargs : dict
        Keyword arguments passed to the main function.
    settings : dict
        Evaluation variables.

    """
    logger.debug("defining the number of dislocations")
    settings['n_roi'] = len(sample['dislocations']['senses'])
    settings['n_all'] = settings['n_roi'] * (2*kwargs['replicate'] + 1)**2

    logger.debug("drawing random points")
    settings['points'] = random_points(sample, kwargs['points'])

    logger.debug("adding some parameters")
    settings['replicate'] = kwargs['replicate']
    settings['b_len'] = np.linalg.norm(kwargs['b_uvw']) * kwargs['cell']/2
    settings['poisson'] = kwargs['poisson']
    settings['shear'] = kwargs['shear']
    settings['processes'] = kwargs['processes']
    settings['density'] = sample['distribution']['density']
    settings['core'] = kwargs['core']
    if not kwargs['absolute']:
        settings['core'] *= settings['b_len']

    logger.debug("identifying dislocation type")
    settings['constant'] = (
        settings['shear'] *
        settings['b_len']**2 /
        16 /
        np.pi**2
    )
    settings['factor'] = (
        4 * np.pi /
        settings['shear'] /
        settings['b_len']**2 /
        settings['density']
    )
    if kwargs['type'] == 'edge':
        settings['type'] = 'edge'
        settings['constant'] /= (1 - settings['poisson'])**2
        settings['factor'] *= (1 - settings['poisson'])
        settings['function'] = energy_edge
    elif kwargs['type'] == 'screw':
        settings['type'] = 'screw'
        settings['function'] = energy_screw
    else:
        raise NotImplementedError("mixed dislocations")


def prepare_shared_data(sample, settings, share):
    """Initialize and fill the shared containers.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.
    settings : dict
        Evaluation variables.
    share : dict
        Shared data.

    """
    wrap = {}

    logger.debug("declaring shared data")
    share['x'] = RawArray('d', settings['n_all'])
    share['y'] = RawArray('d', settings['n_all'])
    share['s'] = RawArray('b', settings['n_all'])
    share['poisson'] = settings['poisson']
    share['constant'] = settings['constant']
    share['core'] = settings['core']

    logger.debug("wrapping shared data")
    wrap['x'] = np.frombuffer(share['x'], dtype=np.float64)
    wrap['y'] = np.frombuffer(share['y'], dtype=np.float64)
    wrap['s'] = np.frombuffer(share['s'], dtype=np.int8)

    logger.debug("defining shared data")
    wrap['x'][0:settings['n_roi']] = sample['dislocations']['positions'][0]
    wrap['y'][0:settings['n_roi']] = sample['dislocations']['positions'][1]
    wrap['s'][0:settings['n_roi']] = sample['dislocations']['senses']
    if settings['replicate'] > 0:
        if sample['region']['type'] != 'square':
            raise TypeError("can only apply replication on a square region")
        for i, (k_x, k_y) in enumerate(shift_indexes(settings['replicate'])):
            j = (i+1) * settings['n_roi']
            k = (i+2) * settings['n_roi']
            wrap['x'][j:k] = k_x * sample['region']['side']
            wrap['y'][j:k] = k_y * sample['region']['side']
            wrap['x'][j:k] += wrap['x'][0:settings['n_roi']]
            wrap['y'][j:k] += wrap['y'][0:settings['n_roi']]
            wrap['s'][j:k] = wrap['s'][0:settings['n_roi']]


def user_check(settings, share, kwargs):
    """Display random points and replications if requested by the user.

    Parameters
    ----------
    settings : dict
        Evaluation variables.
    share : dict
        Shared data.
    kwargs : dict
        Keyword arguments passed to the main function.

    """
    logger.debug("checking random points and replicated dislocations")
    if kwargs['check']:
        fig, axes = plt.subplots()
        axes.scatter(share['x'], share['y'], label='dislocations')
        axes.scatter(*settings['points'].T, label='random points')
        axes.set_aspect(1)
        axes.set_xlabel("$x$ (m)")
        axes.set_ylabel("$y$ (m)")
        axes.legend()
        plt.show()
        plt.close(fig)


def assemble_data(sample, settings, kwargs, result, times):
    """Return the energy evaluation data.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.
    settings : dict
        Evaluation variables.
    kwargs : dict
        Keyword arguments passed to the main function.
    results : dict
        Energy evaluation results.
    times : dict
        Time measurements.

    Returns
    -------
    dict
        Energy evaluation data.

    """
    logger.debug("assembling data")
    data = {
        'distribution': sample['distribution'],
        'region': sample['region'],
        'evaluation': {
            'module': __package__,
            'type': settings['type'],
            'b_uvw': kwargs['b_uvw'],
            'cell': kwargs['cell'],
            'b_len': settings['b_len'],
            'poisson': kwargs['poisson'],
            'shear': kwargs['shear'],
            'core': settings['core'],
            'energy_mean': result['energy_mean'],
            'energy_deviation': result['energy_deviation'],
            'factor': settings['factor'],
            'cutoff': result['cutoff'],
            'samples': 1,
            'replicate': kwargs['replicate'],
            'duration': times['1'] - times['0'],
            'points': kwargs['points'],
            'processes': kwargs['processes'],
            'hidden': kwargs['points'] - int(result['mask']),
        },
    }
    return data


def run_monte_carlo(settings, share, result, times):
    """Run the Monte Carlo method.

    Parameters
    ----------
    settings : dict
        Evaluation variables.
    share : dict
        Shared data.
    results : dict
        Evaluation results.
    times : dict
        Time measurements.

    """
    logger.debug("computing strain energy")
    times['0'] = time()
    with Pool(
        settings['processes'],
        initializer=initializer,
        initargs=(share,),
    ) as pool:
        result['output'] = pool.map(settings['function'], settings['points'])
    times['1'] = time()

    logger.debug("processing output")
    result['energy'], result['mask'] = np.array(result['output']).T
    result['energy'] = result['energy'][result['mask'].astype(bool)]
    result['mask'] = sum(result['mask'])
    result['energy_mean'] = np.mean(result['energy'])
    result['energy_deviation'] = np.std(result['energy'])
    result['cutoff'] = settings['core'] * np.exp(
        settings['factor'] * result['energy_mean']
    )


def initializer(share):
    """Initialize a worker.

    Parameters
    ----------
    share : dict
        Shared data to be passed to the worker.

    """
    shared.update(share)


def shift_indexes(replications):
    """Return the indexes for the replications of the roi.

    Parameters
    ----------
    replications : int
        Number of replications around the region of interest.

    Returns
    -------
    list of tuple
        Replications indexes.

    """
    indexes = []
    for i in range(1, replications+1):
        for j in range(2*i):
            for k in (1, -1):
                indexes.append((-i*k, (i-j)*k))
                indexes.append(((i-j)*k,  i*k))
    return indexes


def random_points(sample, number):
    """Return the position of the random points.

    Parameters
    ----------
    sample : dict
        Dislocation sample data.
    number : int
        Number of random points in the region of interest.

    Returns
    -------
    np.array
        Position of the random points.

    """
    rng = np.random.default_rng(sample['distribution']['seed'])
    if sample['region']['type'] == 'square':
        side = sample['region']['side']
        positions = rng.random((number, 2), np.float64) * side
    elif sample['region']['type'] == 'disk':
        phi = 2 * np.pi * rng.random(number)
        rad = sample['region']['radius'] * np.sqrt(rng.random(number))
        return np.stack((rad*np.cos(phi), rad*np.sin(phi)), axis=1)
    else:
        raise NotImplementedError("unknown region type")
    return positions


def energy_screw(position):
    """Return the strain energy density at the position.

    Parameters
    ----------
    position : np.array
        Position of the random point.

    Returns
    -------
    np.array
        Strain energy density.

    """
    density, keep = energy.screw(
        position[0],
        position[1],
        shared['x'],
        shared['y'],
        shared['s'],
        shared['core'],
    )
    density = shared['constant'] * density
    return (density, keep)


def energy_edge(position):
    """Return the strain energy density at the position.

    Parameters
    ----------
    position : np.array
        Position of the random point.

    Returns
    -------
    np.array
        Strain energy density.

    """
    density, keep = energy.edge(
        position[0],
        position[1],
        shared['x'],
        shared['y'],
        shared['s'],
        shared['core'],
        shared['poisson'],
    )
    density = shared['constant'] * density
    return (density, keep)
