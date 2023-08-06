import abc
from copy import deepcopy
import enum
from functools import wraps
import json
from typing import cast, Optional, Tuple

from beit.runfiles import runfiles
from requests.status_codes import codes

from beit.qubo_solver.endpoint import APIEndpoint, APIError
from beit.qubo_solver.qubo_instance import QuboInstance, QuboSolution


DEFAULT_API_PREFIX = "https://qubo-solver.pro.beit.tech/v1"
RUNFILES = runfiles.Create()

def _schema(path_to_schema: str):
    with open(RUNFILES.Rlocation(path_to_schema)) as schema_file:
        return json.load(schema_file)

class JobError(Exception):
    pass


class JobStatus(enum.Enum):
    PENDING = 0
    DONE = 1
    ERROR = 2


class Job(abc.ABC):
    """
    Represents job posted for remote execution.
    """

    @property
    @abc.abstractmethod
    def status(self) -> JobStatus:
        pass

    @property
    @abc.abstractmethod
    def result(self) -> Optional[Tuple[QuboSolution]]:
        pass

    @abc.abstractmethod
    def request_result(self):
        """Tries to retrieve result of the running job"""
        pass


class SolverConnection(abc.ABC):
    """
        Responsible for creating jobs.
    """

    @abc.abstractmethod
    def create_job(self, qubo_instance, **kwargs) -> Job:
        pass


def _remember_failure(method):
    @wraps(method)
    def _inner(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs)
        except Exception:
            self._status = JobStatus.ERROR
            raise
        self._status = result
        return result
    return _inner


class AWSJob(Job):
    """Job running on BEIT Qubo Solver"""

    def __init__(self, job_id: str, customer_key: str, endpoint: APIEndpoint):
        self._job_id = job_id
        self._customer_key = customer_key
        self._status = JobStatus.PENDING
        self._result: Optional[Tuple[QuboSolution]] = None
        self._solution_endpoint = endpoint
    
    @property
    def result(self) -> Optional[Tuple[QuboSolution]]:
        return deepcopy(self._result)

    @property    
    def status(self) -> JobStatus:
        return self._status

    @_remember_failure
    def request_result(self) -> JobStatus:
        """Tries to retrieve result of the running job"""
        if self._status != JobStatus.PENDING:
            return self._status
        body, response = self._solution_endpoint.execute(
            {"job_id": self._job_id},
            headers={"x-api-key": self._customer_key}
        )
        if response.status_code != codes.ok:
            raise JobError(f"Something went wrong, API returned code {response.status_code}" + 
                (f" reason given {body['error']}" if 'error' in body else "")
            )
        if body == {}:
            return JobStatus.PENDING
        self._result = cast(Tuple[QuboSolution], tuple(QuboSolution.from_json(sample) for sample in body['samples']))
        return JobStatus.DONE


class AWSSolverConnection(SolverConnection):

    def __init__(self, customer_key: str, api_prefix: str = DEFAULT_API_PREFIX):
        self._customer_key = customer_key
        self._solve_endpoint = APIEndpoint(
            url=api_prefix + "/solve",
            method="POST",
            request_schema=_schema("qubo_solver/schemas/solve.json"),
            response_schema=_schema("qubo_solver/schemas/solve_response.json"),
        )
        self._solution_endpoint = APIEndpoint(
            url=api_prefix + "/solution",
            method="POST",
            request_schema=_schema("qubo_solver/schemas/result.json"),
            response_schema=_schema("qubo_solver/schemas/result_response.json"),
        )

    @staticmethod
    def _create_request_body(qubo_instance, backend, **kwargs):
        request_body = {
            "instance": [{"edge": list(edge), "weight": weight} for edge, weight in qubo_instance.items()],
            "execution": {"backend": backend},
        }
        if "timeout" in kwargs:
            request_body["execution"]["timeout"] = kwargs["timeout"]
        if "sample_count" in kwargs:
            request_body["distribution"] = {"sample_count": kwargs["sample_count"]}
        return request_body

    def create_job(self, qubo_instance: QuboInstance, backend: str = "chimera-solver-bellerophon", **kwargs) -> AWSJob:
        """Creates a job"""

        body, response = self._solve_endpoint.execute(
            self._create_request_body(qubo_instance, backend=backend, **kwargs),
            headers={"x-api-key": self._customer_key}
        )
        if response.status_code == codes.created:
            return AWSJob(body['task_key'], self._customer_key, self._solution_endpoint)
        raise JobError(
            f"Posting job failed with code {response.status_code}" +
            (f' with message: "{body["error"]}"' if 'error' in body else "")
        )
