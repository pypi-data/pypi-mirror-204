"""Implementation of mcli describe run"""
from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Tuple, TypeVar

from rich.table import Table

from mcli.api.exceptions import cli_error_handler
from mcli.api.model.run import Node, Run
from mcli.cli.m_get.display import (MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, create_vertical_display_table,
                                    format_timestamp)
from mcli.models.run_config import DEFAULT_PRIORITY_NAME, ComputeConfig
from mcli.sdk import get_run
from mcli.utils.utils_logging import FormatString, console, format_string, print_timedelta

logger = logging.getLogger(__name__)

DISPLAY_RUN_STATUSES = ['PENDING', 'RUNNING', 'COMPLETED']


class DisplayRunStatus(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'


class DescribeRunDetailColumns(Enum):
    NAME = 'name'
    RUN_ID = 'run_uid'
    IMAGE = 'image'
    LAST_ATTEMPT_ID = 'last_attempt_id'
    PRIORITY = 'priority'


class DescribeRunLifecycleColumns(Enum):
    STATUS = 'status'
    START_TIME = 'start_time'
    END_TIME = 'end_time'
    DURATION = 'duration'


class DescribeRunOriginalInputColumns(Enum):
    SUBMITTED_CONFIG = 'submitted_config'


RUN_DETAIL_DISPLAY_NAMES = ['Run Name', 'Image', 'Last Attempt ID', 'Priority']

RUN_LIFECYCLE_DISPLAY_NAMES = [
    'Start Time',
    'End Time',
    'Duration',
]
RUN_NODES_DISPLAY_NAMES = ['Node Name']
SUBMITTED_CONFIG = ['Run Config']


@dataclass
class DescribeRunDetailDisplayItem(MCLIDisplayItem):
    """Tuple that extracts detailed run data for display purposes"""
    name: str
    image: str
    last_attempt_id: str
    priority: str

    @classmethod
    def from_run(cls, run: Run) -> DescribeRunDetailDisplayItem:
        priority = run.config.scheduling.get('priority', None) or DEFAULT_PRIORITY_NAME
        if priority and priority.lower() == 'default':
            priority = DEFAULT_PRIORITY_NAME

        extracted: Dict[str, Any] = {
            DescribeRunDetailColumns.NAME.value: run.config.name,
            DescribeRunDetailColumns.IMAGE.value: run.config.image,
            DescribeRunDetailColumns.LAST_ATTEMPT_ID.value: run.last_attempt_id,
            DescribeRunDetailColumns.PRIORITY.value: priority.lower(),
        }

        return DescribeRunDetailDisplayItem(**extracted)


@dataclass
class DescribeRunLifecycleDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for run lifecycle display purposes"""
    status: str
    start_time: str
    end_time: str
    duration: str


@dataclass
class DescribeRunMetadataDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run metadata for display purposes"""

    key: str
    value: str


@dataclass
class MCLIDescribeRunNodeDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for run node display purposes"""
    rank: int
    name: str


# Displays
class MCLIDescribeRunDetailsDisplay(MCLIGetDisplay):
    """ Vertical table view of run details """

    def __init__(self, models: List[Run]):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)

    @property
    def index_label(self) -> str:
        return ""

    def create_custom_table(self, columns: List[str], data: List[Tuple[Any, ...]], names: List[str]) -> Optional[Table]:
        return create_vertical_display_table(data=data, columns=RUN_DETAIL_DISPLAY_NAMES)

    def __iter__(self) -> Generator[DescribeRunDetailDisplayItem, None, None]:
        for model in self.models:
            item = DescribeRunDetailDisplayItem.from_run(model)
            yield item


class MCLIDescribeRunLifecycleDisplay(MCLIGetDisplay):
    """ Horizontal table view of run lifecycle """

    def __init__(self, models: List[Run]):
        self.model = models[0]

    @property
    def custom_column_names(self) -> List[str]:
        return RUN_LIFECYCLE_DISPLAY_NAMES

    def __iter__(self) -> Generator[DescribeRunLifecycleDisplayItem, None, None]:
        for e in DisplayRunStatus:
            item = format_run_status(e.value, self.model)
            yield item

    @property
    def index_label(self) -> str:
        return 'status'


class MCLIDescribeRunMetadataDisplay(MCLIGetDisplay):
    """ Vertical table view of run metadata """

    def __init__(self, metadata: Dict[str, Any]):
        self.columns = sorted(metadata.keys())
        self.metadata = metadata

    @property
    def index_label(self) -> str:
        return "key"

    def __iter__(self) -> Generator[DescribeRunMetadataDisplayItem, None, None]:
        for k in self.columns:
            item = DescribeRunMetadataDisplayItem(key=k, value=self.metadata[k])
            yield item


class MCLIDescribeRunNodeDisplay(MCLIGetDisplay):
    """ Horizontal table view of run node """

    def __init__(self, nodes: List[Node]):
        self.nodes = sorted(nodes, key=lambda x: x.rank)

    @property
    def custom_column_names(self) -> List[str]:
        return RUN_NODES_DISPLAY_NAMES

    def __iter__(self) -> Generator[MCLIDescribeRunNodeDisplayItem, None, None]:
        for n in self.nodes:
            yield MCLIDescribeRunNodeDisplayItem(n.rank, n.name)

    @property
    def index_label(self) -> str:
        return 'rank'


T = TypeVar('T')


def compute_or_deprecated(compute: ComputeConfig, key: str, deprecated: T) -> Optional[T]:
    from_compute = compute.get(key, None)
    if from_compute is not None:
        return from_compute
    return deprecated


@dataclass
class DescribeComputeRequests():
    """Describer for compute requests"""
    cluster: Optional[str] = None
    gpu_type: Optional[str] = None
    gpus: Optional[int] = None
    cpus: Optional[int] = None
    instance: Optional[str] = None
    nodes: Optional[int] = None

    @property
    def display_names(self) -> Dict[str, str]:
        # Return display name mapping for table
        return {
            'cluster': 'Cluster',
            'gpu_type': 'GPU Type',
            'gpus': 'GPUs',
            'cpus': 'CPUs',
            'instance': 'Instance',
            'nodes': 'Nodes',
        }

    @classmethod
    def from_run(cls, run: Run) -> DescribeComputeRequests:
        return DescribeComputeRequests(
            cluster=compute_or_deprecated(run.config.compute, 'cluster', run.config.cluster),
            gpu_type=compute_or_deprecated(run.config.compute, 'gpu_type', run.config.gpu_type),
            gpus=compute_or_deprecated(run.config.compute, 'gpus', run.config.gpu_num),
            cpus=compute_or_deprecated(run.config.compute, 'cpus', run.config.cpus),
            instance=run.config.compute.get('instance', None),
            nodes=run.config.compute.get('nodes', None),
        )

    def to_table(self) -> Table:
        data = {self.display_names.get(k, k.capitalize()): str(v) for k, v in asdict(self).items() if v is not None}
        columns = list(data.keys())
        values = [tuple(data.values())]
        return create_vertical_display_table(data=values, columns=columns)


# Run lifecycle
def format_run_status(status: str, run: Run) -> DescribeRunLifecycleDisplayItem:
    if status == DisplayRunStatus.PENDING.value:
        duration = print_timedelta(run.started_at - run.created_at) if run.started_at and run.created_at else '-'
        return DescribeRunLifecycleDisplayItem(status=status,
                                               start_time=format_timestamp(run.created_at),
                                               end_time=format_timestamp(run.started_at),
                                               duration=duration)
    elif status == DisplayRunStatus.RUNNING.value:
        duration = print_timedelta(run.completed_at - run.started_at) if run.completed_at and run.started_at else '-'
        return DescribeRunLifecycleDisplayItem(status=status,
                                               start_time=format_timestamp(run.started_at),
                                               end_time=format_timestamp(run.completed_at),
                                               duration=duration)
    else:
        return DescribeRunLifecycleDisplayItem(status=status,
                                               start_time='--',
                                               end_time=format_timestamp(run.completed_at),
                                               duration='')


@cli_error_handler("mcli describe run")
def describe_run(run_name: str, output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    """
    Fetches more details of a Run
    """
    del kwargs

    run = get_run(run_name)

    # Run details section
    print(format_string('Run Details', FormatString.BOLD))
    metadata_display = MCLIDescribeRunDetailsDisplay([run])
    metadata_display.print(output)
    print()

    # Compute requests section
    print(format_string('Compute Requests', FormatString.BOLD))
    compute_display = DescribeComputeRequests.from_run(run)
    console.print(compute_display.to_table())
    print()

    # Run lifecycle section
    print(format_string('Run Lifecycle', FormatString.BOLD))
    lifecycle_display = MCLIDescribeRunLifecycleDisplay([run])
    lifecycle_display.print(output)
    print()

    if run.metadata:
        print(format_string('Run Metadata', FormatString.BOLD))
        metadata_display = MCLIDescribeRunMetadataDisplay(run.metadata)
        metadata_display.print(output)
        print()

    if run.nodes:
        print(format_string('Run Nodes', FormatString.BOLD))
        node_display = MCLIDescribeRunNodeDisplay(run.nodes)
        node_display.print(output)
        print()

    # Run original input section
    print(format_string('Submitted YAML', FormatString.BOLD))
    print(run.submitted_config)

    # TODO: cleanup code to print directly to console after parsing
    # wrap command string within a literal `representer` - dump long str as block
