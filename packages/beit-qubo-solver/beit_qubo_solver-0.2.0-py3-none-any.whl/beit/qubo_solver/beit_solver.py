from itertools import chain
from time import sleep
from typing import Any, Dict, Hashable, List, Optional, Tuple

import dimod
from dimod.exceptions import BinaryQuadraticModelStructureError

from beit.qubo_solver.architecture import make_chimera_architecture
from beit.qubo_solver.qubo_instance import QuboInstance
from beit.qubo_solver.solver_connection import JobStatus, SolverConnection


class BEITSamplerBase(dimod.Sampler):

    _BACKEND: Optional[str] = None

    def __init__(self, solver_connection: SolverConnection):
        self._connection = solver_connection
        super().__init__()

    def _sample_qubo(self, qubo_instance: QuboInstance, **parameters):
        parameters = self.remove_unknown_kwargs(**parameters)
        job = self._connection.create_job(qubo_instance, backend=self._BACKEND, **parameters)
        while job.request_result() == JobStatus.PENDING:
            sleep(0.5)  # Arbitrary number
        assert job.status == JobStatus.DONE  # Otherwise it should've throw earlier.
        assert job.result is not None
        states = [result.state for result in job.result]
        energies = [result.energy for result in job.result]
        return states, energies


class BEITSolver(BEITSamplerBase, dimod.Structured):
    """
    This is an exact solver for QUBO. It works only with
    chimera architecture (max size being (8, 16, 4))
    """

    _TARGET_ARCHITECTURE = make_chimera_architecture()

    _BACKEND = "chimera-solver-bellerophon"

    @property
    def edgelist(self) -> List[Tuple[Hashable, Hashable]]:
        return list(self._TARGET_ARCHITECTURE.edges)

    @property
    def nodelist(self) -> List[Hashable]:
        return list(self._TARGET_ARCHITECTURE.nodes)

    @property
    def parameters(self) -> Dict[str, Any]:
        return {}

    @property
    def properties(self) -> Dict[str, Any]:
        return {}

    def _check_instance_valid(self, qubo_instance: QuboInstance):
        nodes = set(chain.from_iterable(qubo_instance.keys()))
        for node in nodes:
            if not isinstance(node, int):
                raise TypeError("Names of nodes in QUBO instance must be integers")
        wrong_nodes = nodes - set(self.nodelist)
        if wrong_nodes:
            raise BinaryQuadraticModelStructureError(
                f"The following variables are not present in the nodelist: {' '.join(map(str, wrong_nodes))}"
            )
        wrong_edges = {
            edge for edge in qubo_instance.keys()
            if edge not in self._TARGET_ARCHITECTURE.edges and edge[::-1] not in self._TARGET_ARCHITECTURE.edges and edge[0] != edge[1]
        }
        if wrong_edges:
            raise BinaryQuadraticModelStructureError(
                f"The following edges are not present in the edgelist: {' '.join(map(str, wrong_edges))}"
            )

    def sample_qubo(self, qubo_instance: QuboInstance, **parameters):
        self._check_instance_valid(qubo_instance)
        states, energies = self._sample_qubo(qubo_instance, **parameters)
        return dimod.SampleSet.from_samples(states, dimod.Vartype.BINARY, energies)


class BEITUnconstrainedSampler(BEITSamplerBase):

    _BACKEND = "any-sampler-hephaestus"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "timeout": [],
            "sample_count": ["Number of samples returned, returned value can differ from requested."],
        }

    @property
    def properties(self) -> Dict[str, Any]:
        return {
            "max_timeout": 60 * 12,  # 12 minutes
            "max_combined_sample_size": [10 ** 6, "Number of variables times number of samples can not exceed this number."],
            "weights_range": [10 ** 6, "Maximum absolute value for any single weight (biases and couplers)"],
            "max_num_weights": [5000, "Maximum number of weights in a problem (biases and couplers)"],
        }

    def _prepare_mapping(self, qubo_instance) -> Tuple[QuboInstance, List[Hashable]]:
        #  Set is constructed to remove duplicates
        reverse_mapping = list(set(chain.from_iterable(qubo_instance.keys())))
        mapping = {x: i for i, x in enumerate(reverse_mapping)}
        qubo_instance = {(mapping[x], mapping[y]): v for (x, y), v in qubo_instance.items()}
        return qubo_instance, reverse_mapping

    @staticmethod
    def _unmap(solutions: List[Tuple[int, ...]], reverse_mapping: List[Hashable]) -> List[Dict[Hashable, int]]:
        return [
            {reverse_mapping[i]: v for i, v in enumerate(solution)} for solution in solutions
        ]

    def sample_qubo(self, qubo_instance: QuboInstance, sample_count: int = 1, **parameters):
        qubo_instance, reverse_mapping = self._prepare_mapping(qubo_instance)
        states, energies = self._sample_qubo(qubo_instance, sample_count=sample_count, **parameters)
        states = self._unmap(states, reverse_mapping)
        return dimod.SampleSet.from_samples(states, dimod.Vartype.BINARY, energies)
