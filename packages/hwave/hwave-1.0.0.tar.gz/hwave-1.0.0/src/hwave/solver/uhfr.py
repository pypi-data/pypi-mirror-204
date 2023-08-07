import itertools
import logging
import numpy as np
import itertools
import os
from requests.structures import CaseInsensitiveDict
from .perf import do_profile

logger = logging.getLogger("qlms").getChild("uhfr")

class Interact_UHFr_base():
    def __init__(self, ham_info, Nsize):
        self.Nsize = Nsize
        self.Ham_tmp = np.zeros(tuple([(2 * self.Nsize) for i in range(4)]), dtype=complex)
        self.Ham_trans_tmp = np.zeros(tuple([(2 * self.Nsize) for i in range(2)]), dtype=complex)
        self.param_ham = self._transform_interall(ham_info)
        self._check_range()

    #Change interaction to interall type
    def _transform_interall(self, ham_info):
        return ham_info

    def _calc_hartree(self):
        site = np.zeros(4, dtype=np.int32)
        for site_info, value in self.param_ham.items():
            for i in range(4):
                site[i] = site_info[2 * i] + site_info[2 * i + 1] * self.Nsize
            # Diagonal Fock term
            self.Ham_tmp[site[0]][site[1]][site[2]][site[3]] += value
            self.Ham_tmp[site[2]][site[3]][site[0]][site[1]] += value
            if site[1] == site[2]:
                self.Ham_trans_tmp[site[1]][site[2]] += value
        pass

    def _calc_fock(self):
        site = np.zeros(4,dtype=np.int32)
        for site_info, value in self.param_ham.items():
            for i in range(4):
                site[i] = site_info[2 * i] + site_info[2 * i + 1] * self.Nsize
            # OffDiagonal Fock term
            self.Ham_tmp[site[0]][site[3]][site[2]][site[1]] -= value
            self.Ham_tmp[site[2]][site[1]][site[0]][site[3]] -= value
        pass

    def get_ham(self, type):
        self._calc_hartree()
        if type == "hartreefock":
            self._calc_fock()
        return self.Ham_tmp, self.Ham_trans_tmp

    # check input
    def _check_range(self):
        err = 0
        for site_info, value in self.param_ham.items():
            for i in range(4):
                if not 0 <= site_info[2*i] < self.Nsize:
                    err += 1
                if not 0 <= site_info[2*i+1] < 2:
                    err += 1
        if err > 0:
            logger.error("Range check failed for {}".format(self.__name__))
            exit(1)

    def _check_hermite(self, strict_hermite, tolerance):
        err = 0
        for site_info, value in self.param_ham.items():
            list = tuple([site_info[i] for i in [6,7,4,5,2,3,0,1]])
            vv = self.param_ham.get(list, 0.0).conjugate()
            if not np.isclose(value, vv, atol=tolerance, rtol=0.0):
                logger.info("  index={}, value={}, index={}, value^*={}".format(site_info, value, list, vv))
                err += 1
        if err > 0:
            msg = "Hermite check failed for {}".format(self.__name__)
            if strict_hermite:
                logger.error(msg)
                exit(1)
            else:
                logger.warn(msg)

    def check_hermite(self, strict_hermite=False, tolerance=1.0e-8):
        self._check_hermite(strict_hermite, tolerance)

class CoulombIntra_UHFr(Interact_UHFr_base):
    def __init__(self, ham_info, Nsize):
        self.__name__ = "CoulombIntra"
        super().__init__(ham_info, Nsize)
    def _transform_interall(self, ham_info):
        param_tmp = {}
        for site_info, value in ham_info.items():
            sinfo = tuple([site_info[0], 0, site_info[0], 0, site_info[0], 1, site_info[0], 1])
            param_tmp[sinfo] = value
        return param_tmp

class CoulombInter_UHFr(Interact_UHFr_base):
    def __init__(self, ham_info, Nsize):
        self.__name__ = "CoulombInter"
        super().__init__(ham_info, Nsize)
    def _transform_interall(self, ham_info):
        param_tmp = {}
        for site_info, value in ham_info.items():
            for spin_i, spin_j in itertools.product([0,1], repeat=2):
                sinfo = tuple([site_info[0], spin_i, site_info[0], spin_i, site_info[1], spin_j, site_info[1], spin_j])
                param_tmp[sinfo] = value
        return param_tmp

class Hund_UHFr(Interact_UHFr_base):
    def __init__(self, ham_info, Nsize):
        self.__name__ = "Hund"
        super().__init__(ham_info, Nsize)
    def _transform_interall(self, ham_info):
        param_tmp = {}
        for site_info, value in ham_info.items():
            for spin_i in range(2):
                sinfo = tuple([site_info[0], spin_i, site_info[0], spin_i, site_info[1], spin_i, site_info[1], spin_i])
                param_tmp[sinfo] = -value
        return param_tmp

class PairHop_UHFr(Interact_UHFr_base):
    def __init__(self, ham_info, Nsize):
        self.__name__ = "PairHop"
        super().__init__(ham_info, Nsize)
    def _transform_interall(self, ham_info):
        param_tmp = {}
        for site_info, value in ham_info.items():
            sinfo = tuple([site_info[0], 0, site_info[1], 0, site_info[0], 1, site_info[1], 1])
            param_tmp[sinfo] = value
            sinfo = tuple([site_info[1], 1, site_info[0], 1, site_info[1], 0, site_info[0], 0])
            param_tmp[sinfo] = value
        return param_tmp

class Exchange_UHFr(Interact_UHFr_base):
    def __init__(self, ham_info, Nsize):
        self.__name__ = "Exchange"
        super().__init__(ham_info, Nsize)
    def _transform_interall(self, ham_info):
        param_tmp = {}
        for site_info, value in ham_info.items():
            sinfo = tuple([site_info[0], 0, site_info[1], 0, site_info[1], 1, site_info[0], 1])
            param_tmp[sinfo] = value
            sinfo = tuple([site_info[0], 1, site_info[1], 1, site_info[1], 0, site_info[0], 0])
            param_tmp[sinfo] = value
        return param_tmp

class Ising_UHFr(Interact_UHFr_base):
    def __init__(self, ham_info, Nsize):
        self.__name__ = "Ising"
        super().__init__(ham_info, Nsize)
    def _transform_interall(self, ham_info):
        param_tmp = {}
        for site_info, value in ham_info.items():
            for spin_i, spin_j in itertools.product([0,1], repeat=2):
                sinfo = tuple([site_info[0], spin_i, site_info[0], spin_i, site_info[1], spin_j, site_info[1], spin_j])
                param_tmp[sinfo] = value * (1-2*spin_i) * (1-2*spin_j) / 4
        return param_tmp

class PairLift_UHFr(Interact_UHFr_base):
    def __init__(self, ham_info, Nsize):
        self.__name__ = "PairLift"
        super().__init__(ham_info, Nsize)
    def _transform_interall(self, ham_info):
        param_tmp = {}
        for site_info, value in ham_info.items():
            sinfo = tuple([site_info[0], 0, site_info[0], 1, site_info[1], 0, site_info[1], 1])
            param_tmp[sinfo] = value
            sinfo = tuple([site_info[1], 1, site_info[1], 0, site_info[0], 1, site_info[0], 0])
            param_tmp[sinfo] = value
        return param_tmp

class InterAll_UHFr(Interact_UHFr_base):
    def __init__(self, ham_info, Nsize, strict_hermite, tolerance):
        self.__name__ = "InterAll"
        super().__init__(ham_info, Nsize)
        self._check_hermite(strict_hermite, tolerance)
    def _transform_interall(self, ham_info):
        return ham_info

class Term_base:
    def __init__(self, term_info, Nsize, coeff=1.0):
        self.Nsize = Nsize
        self.term_info = term_info
        self.coeff = coeff
        self._check_range()

    def get_data(self):
        data = np.zeros(tuple([(2 * self.Nsize) for i in range(2)]), dtype=complex)
        for site_info, value in self.term_info.items():
            # set value
            site1 = site_info[0] + site_info[1] * self.Nsize
            site2 = site_info[2] + site_info[3] * self.Nsize
            data[site1][site2] += self.coeff * value
        return data

    def _check_range(self):
        err = 0
        for site_info, value in self.term_info.items():
            for i in range(2):
                if not 0 <= site_info[2*i] < self.Nsize:
                    err += 1
                if not 0 <= site_info[2*i+1] < 2:
                    err += 1
        if err > 0:
            logger.error("Range check failed for Transfer")
            exit(1)

    def _check_hermite(self, strict_hermite, tolerance):
        err = 0
        for site_info, value in self.term_info.items():
            list = tuple([site_info[i] for i in [2,3,0,1]])
            vv = self.term_info.get(list, 0.0).conjugate()
            if not np.isclose(value, vv, atol=tolerance, rtol=0.0):
                logger.debug("  index={}, value={}, index={}, value^*={}".format(site_info, value, list, vv))
                err += 1
        if err > 0:
            msg = "Hermite check failed for {}".format(self.__name__)
            if strict_hermite:
                logger.error(msg)
                exit(1)
            else:
                logger.warn(msg)

    def check_hermite(self, strict_hermite=False, tolerance=1.0e-8):
        self._check_hermite(strict_hermite, tolerance)

class Transfer_UHFr(Term_base):
    def __init__(self, term_info, Nsize):
        self.__name__ = "Transfer"
        super().__init__(term_info, Nsize, coeff=-1.0)

class Green_UHFr(Term_base):
    def __init__(self, term_info, Nsize):
        self.__name__ = "Green"
        super().__init__(term_info, Nsize, coeff=1.0)


from .base import solver_base

class UHFr(solver_base):
    @do_profile
    def __init__(self, param_ham, info_log, info_mode, param_mod=None):
        self.name = "uhfr"
        super().__init__(param_ham, info_log, info_mode, param_mod)
        self.physics = {"Ene": 0, "NCond": 0, "Sz": 0, "Rest": 1.0}

        output_str = "Show input parameters"
        for k, v in self.param_mod.items():
            output_str += "\n  {:<20s}: {}".format(k, v)
        logger.info(output_str)

        if self._check_param_range(self.param_mod, { "Nsite": [1, None]}) != 0:
            logger.error("parameter range check failed.")
            exit(1)

        self.iflag_fock = info_mode.get("flag_fock", True)
        self.ene_cutoff = self.param_mod.get("ene_cutoff", 1e+2)
        self.T = self.param_mod.get("T", 0)

        self.strict_hermite = self.param_mod.get("strict_hermite", False)
        self.hermite_tolerance = self.param_mod.get("hermite_tolerance", 1.0e-8)

        # Make a list for generating Hamiltonian
        self.Nsize = self.param_mod["nsite"]
        if "filling" in self.param_mod:
            round_mode = self.param_mod.get("Ncond_round_mode", "strict")
            self.Ncond = self._round_to_int(self.param_mod["filling"] * 2 * self.Nsize, round_mode)
        else:
            self.Ncond = self.param_mod["Ncond"]
        TwoSz = self.param_mod["2Sz"]
        if TwoSz is None:
            self.green_list = {"sz-free": {"label": [i for i in range(2 * self.Nsize)], "occupied": self.Ncond}}
        else:
            self.green_list = {
                "spin-up": {"label": [i for i in range(self.Nsize)], "value": 0.5, "occupied": int((self.Ncond + TwoSz) / 2)},
                "spin-down": {"label": [i for i in range(self.Nsize, 2 * self.Nsize)], "value": -0.5,
                         "occupied": int((self.Ncond - TwoSz) / 2)}}

    @do_profile
    def solve(self, green_info, path_to_output):
        print_level = self.info_log["print_level"]
        print_step = self.info_log["print_step"]
        print_check = self.info_log.get("print_check", None)
        if print_check is not None:
            fch = open(os.path.join(path_to_output, print_check), "w")
        logger.info("Set Initial Green's functions")
        # Get label for eigenvalues
        label = 0
        for k, v in self.green_list.items():
            self.green_list[k]["eigen_start"] = label
            label += len(self.green_list[k]["label"])
        self.Green = self._initial_G(green_info)

        logger.info("Start UHFr calculations")
        param_mod = self.param_mod

        if print_level > 0:
            logger.info("step, rest, energy, NCond, Sz")
        self._makeham_const()
        self._makeham_mat()
        import time
        for i_step in range(param_mod["IterationMax"]):
            self._makeham()
            self._diag()
            self._green()
            self._calc_energy()
            self._calc_phys()
            if i_step % print_step == 0 and print_level > 0:
                logger.info(
                    "{}, {:.8g}, {:.8g}, {:.4g}, {:.4g} ".format(i_step, self.physics["Rest"], self.physics["Ene"]["Total"],
                                                                 self.physics["NCond"], self.physics["Sz"]))
            if print_check is not None:
                fch.write(
                    "{}, {:.8g}, {:.8g}, {:.4g}, {:.4g}\n".format(i_step,
                                                                 self.physics["Rest"],
                                                                 self.physics["Ene"]["Total"],
                                                                 self.physics["NCond"],
                                                                 self.physics["Sz"]))
            if self.physics["Rest"] < param_mod["eps"]:
                break

        if self.physics["Rest"] < param_mod["eps"]:
            logger.info("UHFr calculation is succeeded: rest={}, eps={}.".format(self.physics["Rest"], param_mod["eps"]))
            logger.info("Total Energy = {}.".format(self.physics["Ene"]["Total"]))
        else:
            logger.warning("UHFr calculation is failed: rest={}, eps={}.".format(self.physics["Rest"], param_mod["eps"]))

        if print_check is not None:
            fch.close()

    @do_profile
    def _initial_G(self, green_info):
        _green_list = self.green_list
        green = np.zeros((2 * self.Nsize, 2 * self.Nsize), dtype=complex)
        if green_info["Initial"] is not None:
            logger.info("Load initial green function")
            g_info = green_info["Initial"]

            for site_info, value in g_info.items():
                # range check
                if not (0 <= site_info[0] < self.Nsize and
                        0 <= site_info[2] < self.Nsize and
                        0 <= site_info[1] < 2 and
                        0 <= site_info[3] < 2):
                    logger.error("range check failed for Initial")
                    exit(1)

                # set value
                site1 = site_info[0] + site_info[1] * self.Nsize
                site2 = site_info[2] + site_info[3] * self.Nsize
                green[site1][site2] = value

            # hermite check
            t = np.conjugate(np.transpose(green))
            if not np.allclose(t, green):
                logger.error("hermite check failed for Initial")
                exit(1)
        else:
            logger.info("Initialize green function by random numbers")
            np.random.seed(self.param_mod["RndSeed"])
            rand = np.random.rand(2 * self.Nsize * 2 * self.Nsize).reshape(2 * self.Nsize, 2 * self.Nsize)
            for k, info in _green_list.items():
                v = info["label"]
                for site1, site2 in itertools.product(v, v):
                    green[site1][site2] = 0.01 * (rand[site1][site2] - 0.5)
        return green

    @do_profile
    def _makeham_const(self):
        self.Ham_trans = np.zeros((2 * self.Nsize, 2 * self.Nsize), dtype=complex)
        # Transfer integrals
        trans = Transfer_UHFr(self.param_ham["Transfer"], self.Nsize)
        trans.check_hermite(self.strict_hermite, self.hermite_tolerance)
        self.Ham_trans = trans.get_data()

    @do_profile
    def _makeham(self):
        import time
        self.Ham = np.zeros((2 * self.Nsize, 2 * self.Nsize), dtype=complex)
        self.Ham = self.Ham_trans.copy()
        green_local = self.Green.reshape((2 * self.Nsize) ** 2)
        ham_dot_green = np.dot(self.Ham_local, green_local)
        self.Ham += ham_dot_green.reshape((2 * self.Nsize), (2 * self.Nsize))

    @do_profile
    def _makeham_mat(self):
        # TODO Add Hund, Exchange, Ising, PairHop, and PairLift
        self.Ham_local = np.zeros(tuple([(2 * self.Nsize) for i in range(4)]), dtype=complex)
        if self.iflag_fock is True:
            type = "hartreefock"
        else:
            type = "hartree"

        for key in ["CoulombIntra", "CoulombInter", "Hund", "Exchange", "Ising", "PairHop", "PairLift", "InterAll"]:
            if self.param_ham[key] is not None:
                param_ham = self.param_ham[key]
                if key == "CoulombIntra":
                    ham_uhfr = CoulombIntra_UHFr(param_ham, self.Nsize)
                elif key == "CoulombInter":
                    ham_uhfr = CoulombInter_UHFr(param_ham, self.Nsize)
                elif key == "Hund":
                    ham_uhfr = Hund_UHFr(param_ham, self.Nsize)
                elif key == "Exchange":
                    ham_uhfr = Exchange_UHFr(param_ham, self.Nsize)
                elif key == "Ising":
                    ham_uhfr = Ising_UHFr(param_ham, self.Nsize)
                elif key == "PairHop":
                    ham_uhfr = PairHop_UHFr(param_ham, self.Nsize)
                elif key == "PairLift":
                    ham_uhfr = PairLift_UHFr(param_ham, self.Nsize)
                elif key == "InterAll":
                    ham_uhfr = InterAll_UHFr(param_ham, self.Nsize,
                                           self.strict_hermite, self.hermite_tolerance)
                else:
                    logger.warning("key {} is wrong!".format(key))
                    exit(1)

                Ham_local_tmp, Ham_trans_tmp = ham_uhfr.get_ham(type=type)
                self.Ham_local += Ham_local_tmp
                self.Ham_trans += Ham_trans_tmp

        self.Ham_local = self.Ham_local.reshape((2 * self.Nsize) ** 2, (2 * self.Nsize) ** 2)

    @do_profile
    def _diag(self):
        _green_list = self.green_list
        for k, block_g_info in _green_list.items():
            g_label = block_g_info["label"]
            block_size = len(g_label)
            mat = np.zeros((block_size, block_size), dtype=complex)
            for site1, org_site1 in enumerate(g_label):
                for site2, org_site2 in enumerate(g_label):
                    mat[site1][site2] = self.Ham[org_site1][org_site2]
            # w: The eigenvalues in ascending order, each repeated according to its multiplicity.
            # v: The column v[:, i] is the normalized eigenvector corresponding to the eigenvalue w[i].
            # Will return a matrix object if a is a matrix object.
            w, v = np.linalg.eigh(mat)
            self.green_list[k]["eigenvalue"] = w
            self.green_list[k]["eigenvector"] = v

    @do_profile
    def _fermi(self, mu, eigenvalue):
        fermi = np.zeros(eigenvalue.shape)
        for idx, value in enumerate(eigenvalue):
            if (value - mu) / self.T > self.ene_cutoff:
                fermi[idx] = 0
            else:
                fermi[idx] = 1.0 / (np.exp((value - mu) / self.T) + 1.0)
        return fermi

    @do_profile
    def _green(self):
        _green_list = self.green_list
        # R_SLT = U^{*} in _green
        # L_SLT = U^T in _green
        R_SLT = np.zeros((2 * self.Nsize, 2 * self.Nsize), dtype=complex)
        L_SLT = np.zeros((2 * self.Nsize, 2 * self.Nsize), dtype=complex)
        # Copy Green_old
        self.Green_old = self.Green.copy()
        if self.T == 0:
            for k, block_g_info in _green_list.items():
                g_label = block_g_info["label"]
                # occupied: return the occupied number
                occupied_number = block_g_info["occupied"]
                eigenvec = self.green_list[k]["eigenvector"]
                eigen_start = self.green_list[k]["eigen_start"]
                for eigen_i in range(occupied_number):
                    evec_i = eigenvec[:, eigen_i]
                    for idx, org_site in enumerate(g_label):
                        R_SLT[org_site][eigen_start + eigen_i] = np.conjugate(evec_i[idx])
                        L_SLT[eigen_start + eigen_i][org_site] = evec_i[idx]
            RMat = np.dot(R_SLT, L_SLT)
            self.Green = RMat.copy()
        else: # for finite temperatures
            from scipy import optimize

            def _calc_delta_n(mu):
                n_eigen = np.einsum("ij, ij -> j", np.conjugate(eigenvec), eigenvec).real
                fermi = self._fermi(mu, eigenvalue)
                return np.dot(n_eigen, fermi)-occupied_number

            self.Green = np.zeros((2 * self.Nsize, 2 * self.Nsize), dtype=complex)
            for k, block_g_info in _green_list.items():
                g_label = block_g_info["label"]
                eigenvalue = self.green_list[k]["eigenvalue"]
                eigenvec = self.green_list[k]["eigenvector"]
                occupied_number = block_g_info["occupied"]

                #determine mu
                is_converged = False

                if (_calc_delta_n(eigenvalue[0]) * _calc_delta_n(eigenvalue[-1])) < 0.0:
                    mu, r = optimize.bisect(_calc_delta_n, eigenvalue[0], eigenvalue[-1], full_output=True, disp=False)
                    is_converged = r.converged
                if not is_converged:
                    mu, r = optimize.newton(_calc_delta_n, eigenvalue[0], full_output=True)
                    is_converged = r.converged
                if not is_converged:
                    logger.error("find mu: not converged. abort")
                    exit(1)

                self.green_list[k]["mu"] = mu
                fermi = self._fermi(mu, eigenvalue)
                tmp_green = np.einsum("ij, j, kj -> ik", np.conjugate(eigenvec), fermi, eigenvec)
                for idx1, org_site1 in enumerate(g_label):
                    for idx2, org_site2 in enumerate(g_label):
                        self.Green[org_site1][org_site2] += tmp_green[idx1][idx2]

    @do_profile
    def _calc_energy(self):
        _green_list = self.green_list
        Ene = {}
        Ene["band"] = 0
        if self.T == 0:
            for k, block_g_info in _green_list.items():
                eigenvalue = self.green_list[k]["eigenvalue"]
                occupied_number = block_g_info["occupied"]
                Ene["band"] += np.sum(eigenvalue[:occupied_number])
        else:

            for k, block_g_info in _green_list.items():
                eigenvalue = self.green_list[k]["eigenvalue"]
                eigenvec = self.green_list[k]["eigenvector"]
                mu = self.green_list[k]["mu"]
                fermi = self._fermi(mu, eigenvalue)

                ln_Ene = np.zeros(eigenvalue.shape)
                for idx, value in enumerate(eigenvalue):
                    if -(value - mu) / self.T < self.ene_cutoff:
                        ln_Ene[idx] = np.log1p(np.exp(-(value - mu) / self.T))
                    else:
                        ln_Ene[idx] = -(value - mu) / self.T
                tmp_n = np.einsum("ij, j, ij -> i", np.conjugate(eigenvec), fermi, eigenvec)
                Ene["band"] += mu*np.sum(tmp_n) - self.T * np.sum(ln_Ene)

        Ene["InterAll"] = 0
        green_local = self.Green.reshape((2 * self.Nsize) ** 2)
        Ene["InterAll"] -= np.dot(green_local.T, np.dot(self.Ham_local, green_local))/2.0

        ene = 0
        for value in Ene.values():
            ene += value
        Ene["Total"] = ene
        self.physics["Ene"] = Ene
        logger.debug(Ene)

    @do_profile
    def _calc_phys(self):
        n = 0
        for site in range(2 * self.Nsize):
            n += self.Green[site][site]
        self.physics["NCond"] = n.real

        sz = 0
        for site in range(self.Nsize):
            sz += self.Green[site][site]
            sz -= self.Green[site + self.Nsize][site + self.Nsize]
        self.physics["Sz"] = (0.5 * sz).real

        rest = 0.0
        mix = self.param_mod["mix"]
        for site1, site2 in itertools.product(range(2 * self.Nsize), range(2 * self.Nsize)):
            rest += abs(self.Green[site1][site2] - self.Green_old[site1][site2])**2
            self.Green[site1][site2] = self.Green_old[site1][site2] * (1.0 - mix) + mix * self.Green[site1][site2]
        self.physics["Rest"] = np.sqrt(rest) / (2.0 * self.Nsize * self.Nsize)
        self.Green[np.where(abs(self.Green) < self.threshold)] = 0

    @do_profile
    def get_results(self):
        return (self.physics, self.Green)

    @do_profile
    def save_results(self, info_outputfile, green_info):
        path_to_output = info_outputfile["path_to_output"]

        if "energy" in info_outputfile.keys():
            output_str  = "Energy_total = {}\n".format(self.physics["Ene"]["Total"].real)
            output_str += "Energy_band = {}\n".format(self.physics["Ene"]["band"].real)
            output_str += "Energy_interall = {}\n".format(self.physics["Ene"]["InterAll"].real)
            output_str += "NCond = {}\n".format(self.physics["NCond"])
            output_str += "Sz = {}\n".format(self.physics["Sz"])
            with open(os.path.join(path_to_output, info_outputfile["energy"]), "w") as fw:
                fw.write(output_str)

        if "eigen" in info_outputfile.keys():
            for key, _green_list in self.green_list.items():
                eigenvalue = _green_list["eigenvalue"]
                eigenvector = _green_list["eigenvector"]
                np.savez(os.path.join(path_to_output, key+"_"+info_outputfile["eigen"]), eigenvalue = eigenvalue, eigenvector=eigenvector)

        if "green" in info_outputfile.keys():
            if "OneBodyG" in green_info and green_info["OneBodyG"] is not None:
                _green_info = green_info["OneBodyG"]
                _green_info = np.array(_green_info, dtype=np.int32)
                output_str = ""
                for info in _green_info:
                    nsite1 = info[0] + self.Nsize*info[1]
                    nsite2 = info[2] + self.Nsize*info[3]
                    output_str += "{} {} {} {} {} {}\n".format(info[0], info[1], info[2], info[3], self.Green[nsite1][nsite2].real, self.Green[nsite1][nsite2].imag)
                with open(os.path.join(path_to_output, info_outputfile["green"]), "w") as fw:
                    fw.write(output_str)
            else:
                logger.error("OneBodyG is required to output green function.")
                    
        if "initial" in info_outputfile.keys():
            output_str = "===============================\n"
            green_nonzero = self.Green[np.where(abs(self.Green)>0)]
            ncisajs = len(green_nonzero)
            output_str += "NCisAjs {}\n".format(ncisajs)
            output_str += "===============================\n"
            output_str += "===============================\n"
            output_str += "===============================\n"
            for nsite1, nsite2 in itertools.product(range(2 * self.Nsize), range(2 * self.Nsize)):
                if abs(self.Green[nsite1][nsite2])>0:
                    output_str += "{} {} {} {} {} {}\n".format(nsite1%self.Nsize, nsite1//self.Nsize, nsite2%self.Nsize, nsite2//self.Nsize,
                                                               self.Green[nsite1][nsite2].real, self.Green[nsite1][nsite2].imag)
            with open(os.path.join(path_to_output, info_outputfile["initial"]), "w") as fw:
                fw.write(output_str)

        if "fij" in info_outputfile.keys():
            Ns = self.Nsize
            Ne = self.Ncond

            if self.param_mod["2Sz"] is None:
                if Ne % 2 == 1:
                    logger.warning("FATAL: Ne={}. Ne should be even for calculating fij".format(Ne))
                else:
                    logger.info("Calculations of fij for free-Sz")

                    key = "sz-free"
                    ev = self.green_list[key]["eigenvector"]

                    output_str = ""
                    for i, j in itertools.product(range(Ns), range(Ns)):
                        fij = 0.0
                        for n in range(Ne//2):
                            fij += ev[i][n*2] * ev[j][n*2+1] - ev[i][n*2+1] * ev[j][n*2]
                        output_str += " {:3} {:3}  {:.12f} {:.12f}\n".format(
                            i, j, np.real(fij), np.imag(fij))

                    with open(os.path.join(path_to_output, key+"_"+info_outputfile["fij"]), "w") as fw:
                        fw.write(output_str)
            else:
                TwoSz = self.param_mod["2Sz"]
                if TwoSz % 2 == 1:
                    logger.warning("FATAL: 2Sz={}. 2Sz should be even for calculating fij".format(TwoSz))
                elif TwoSz == 0:
                    logger.info("Calculations of fij for Sz=0")

                    ev_up = self.green_list["spin-up"]["eigenvector"]
                    ev_dn = self.green_list["spin-down"]["eigenvector"]

                    output_str = ""
                    for i, j in itertools.product(range(Ns), range(Ns)):
                        fij = 0.0
                        for n in range(Ne//2):
                            fij += ev_up[i][n] * ev_dn[j][n]
                        output_str += " {:3} {:3} {:.12f} {:.12f}\n".format(
                            i, j, np.real(fij), np.imag(fij))

                    with open(os.path.join(path_to_output, "Sz0_"+info_outputfile["fij"]), "w") as fw:
                        fw.write(output_str)
                else:
                    logger.warning("NOT IMPLEMENTED: Sz even and Sz != 0: this case will be implemented in near future")

    @do_profile
    def get_Ham(self):
        return self.Ham
