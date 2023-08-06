from qsolve.core import qsolve_core_gpe_3d as qsolve_core


def compute_E_interaction(self, identifier, kwargs):

    if "units" in kwargs:

        units = kwargs["units"]

    else:

        units = "si_units"

    if identifier == "psi":

        E_interaction = qsolve_core.compute_interaction_energy_gpe_3d(
            self.psi,
            self.dx,
            self.dy,
            self.dz,
            self.g)

    elif identifier == "psi_0":

        E_interaction = qsolve_core.compute_interaction_energy_gpe_3d(
            self.psi_0,
            self.dx,
            self.dy,
            self.dz,
            self.g)

    elif identifier == "psi_tof_free_gpe":

        E_interaction = qsolve_core.compute_interaction_energy_gpe_3d(
            self.psi_tof_free_gpe,
            self.dx_tof_free_gpe,
            self.dy_tof_free_gpe,
            self.dz_tof_free_gpe,
            self.g)

    else:

        message = 'compute_E_interaction(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    if units == "si_units":

        return self.units.unit_energy * E_interaction

    else:

        return E_interaction


def compute_E_kinetic(self, identifier, kwargs):

    if "units" in kwargs:

        units = kwargs["units"]

    else:

        units = "si_units"

    if identifier == "psi":

        E_kinetic = qsolve_core.compute_kinetic_energy_gpe_3d(
            self.psi,
            self.dx,
            self.dy,
            self.dz,
            self.hbar,
            self.m_atom)

    elif identifier == "psi_0":

        E_kinetic = qsolve_core.compute_kinetic_energy_gpe_3d(
            self.psi_0,
            self.dx,
            self.dy,
            self.dz,
            self.hbar,
            self.m_atom)

    elif identifier == "psi_tof_free_gpe":

        E_kinetic = qsolve_core.compute_kinetic_energy_gpe_3d(
            self.psi_tof_free_gpe,
            self.dx_tof_free_gpe,
            self.dy_tof_free_gpe,
            self.dz_tof_free_gpe,
            self.hbar,
            self.m_atom)

    else:

        message = 'compute_E_kinetic(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    if units == "si_units":

        return self.units.unit_energy * E_kinetic

    else:

        return E_kinetic


def compute_E_potential(self, identifier, kwargs):

    if "units" in kwargs:

        units = kwargs["units"]

    else:

        units = "si_units"

    if identifier == "psi":

        E_potential = qsolve_core.compute_potential_energy_gpe_3d(self.psi, self.V, self.dx, self.dy, self.dz)

    elif identifier == "psi_0":

        E_potential = qsolve_core.compute_potential_energy_gpe_3d(self.psi_0, self.V, self.dx, self.dy, self.dz)

    else:

        message = 'compute_E_potential(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    if units == "si_units":

        return self.units.unit_energy * E_potential

    else:

        return E_potential


def compute_E_total(self, identifier, kwargs):

    if "units" in kwargs:

        units = kwargs["units"]

    else:

        units = "si_units"

    if identifier == "psi":

        E = qsolve_core.compute_total_energy_gpe_3d(self.psi, self.V, self.dx, self.dy, self.dz, self.hbar, self.m_atom, self.g)

    elif identifier == "psi_0":

        E = qsolve_core.compute_total_energy_gpe_3d(self.psi_0, self.V, self.dx, self.dy, self.dz, self.hbar, self.m_atom, self.g)

    else:

        message = 'compute_E_total(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    if units == "si_units":

        return self.units.unit_energy * E

    else:

        return E
