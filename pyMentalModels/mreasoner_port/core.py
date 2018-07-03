#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
import mreasoner_port.constants as glob_vars
import scipy.stats as stats

# XXX Dont think i will need this
# def reset_system_parameters():
#     """
#     Resets all global parameters to their standard values
#
#     Parameters
#     ----------
#     None
#
#     Returns
#     -------
#     Resets all the global parameters for the mreasoner to their respective default value
#     stochastic = False  4.0 sigma+ 0.0 epsilon+ 0.0 omega+ 1.0
#
#     """
#     glob_vars.stochastic = False
#     glob_vars.poisson_lambda_size_models = 4.0
#     glob_vars.sigma = 0.0
#     glob_vars.epsilon = 0.0
#     glob_vars.omega = 1.0


def stochastic_enabled():
    return glob_vars.stochastic


def generate_size():
    """sample from"""


def build_canonical():
    return stats.rand() < glob_vars.epsilon


def system2_enabled():
    return stats.rand() < glob_vars.sigma


def weaken_conclusions():
    return stats.rand() < glob_vars.omega
