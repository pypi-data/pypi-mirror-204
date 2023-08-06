# Copyright 2023 OctoML, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from tabulate import tabulate
from torch.fx import GraphModule
from torch._dynamo.output_graph import GraphCompileReason
from typing import Dict, Sequence, OrderedDict, Optional, List

from .log_util import LOGFILE
from .pricing import AWS_ON_DEMAND_PER_HOUR


__all__ = ['PerBackendResult', 'Segment', 'TotalPerBackendResult', 'Profile', 'ProfileReport']

# The maximum number of displayed compiled segments in the summary. When this
# threshold is crossed, an abridged summary is displayed.
MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT = 3
# Graph information dir
GRAPH_REPORT_DIR = "/tmp/report"


@dataclass
class PerBackendResult:
    mean_ms: Optional[float]
    num_samples: int
    num_failures: int

    def total_ms(self):
        return self.mean_ms * self.num_samples


_instance_type_to_processor = {
    'r6i': 'Intel Ice Lake CPU',
    'r7g': 'AWS Graviton3 CPU',
    'g4dn': 'Nvidia T4 GPU',
    'g5': 'Nvidia A10g GPU',
}


@dataclass
class BackendDescription:
    instance: str
    processor: str
    software_backend: str

    @staticmethod
    def from_backend_spec(spec_str):
        hardware_platform, software_backend = spec_str.split('/')
        try:
            instance_type, instance_size = hardware_platform.split(".")
            processor = _instance_type_to_processor[instance_type]
        except (KeyError, ValueError):
            processor = "N/A"
        return BackendDescription(hardware_platform, processor, software_backend)


@dataclass
class Segment:
    graph_id: Optional[int]  # None if segment is uncompiled
    results_per_backend: OrderedDict[str, PerBackendResult]

    def add(self, segment: 'Segment'):
        # We only ever aggregate compiled segments when we have
        # more compiled segments than MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT.
        for backend, update in segment.results_per_backend.items():
            total = self.results_per_backend[backend]
            total_samples = total.num_samples + update.num_samples

            if total.mean_ms and update.mean_ms:
                total.mean_ms = (total.total_ms() + update.total_ms()) / total_samples
            elif total.mean_ms is None:
                total.mean_ms = update.mean_ms

            total.num_samples = total_samples
            total.num_failures += update.num_failures

    def total_ms(self):
        # NOTE: this function should only be used for sorting. It aggregates
        # total runtimes across all backends.
        runtimes = [v.total_ms() for v in self.results_per_backend.values() if v.mean_ms]
        return functools.reduce(lambda x, y: x + y, runtimes, 0.0)


@dataclass
class PerBackendError:
    graph_id: int
    error_messages_to_count: Dict[str, int]


@dataclass
class TotalPerBackendResult:
    estimated_total_ms: Optional[float]
    errors: List[PerBackendError]


@dataclass
class GraphResult:
    graph_id: int
    graph_module: GraphModule
    compile_reason: GraphCompileReason


@dataclass
class Profile:
    func_name: str
    segments: Sequence[Segment]
    total_uncompiled_ms: float
    total_per_backend: OrderedDict[str, TotalPerBackendResult]
    compilation_occurred: bool
    compilation_errors: Sequence[str]
    num_runs: int
    num_repeats: int
    graph_results: Sequence[GraphResult]
    num_discarded_runs: int

    def _should_abridge(self, verbose):
        return not verbose and \
               len(self._compiled_segments()) > MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT

    def _compiled_segments(self):
        return [s for s in self.segments if s.graph_id is not None]

    def print(self, report_path_prefix, *, file=sys.stdout, verbose=False):
        if len(self.total_per_backend) > 0:
            self._print_totals(file)
            self._print_warnings(file)
            self._print_details(report_path_prefix, file, verbose)
        else:
            print(f'This profile contains only local python code.')

    def _print_details(self, report_path_prefix, file, verbose):
        print(f'Graph level profile is located at {report_path_prefix}*',
              file=file)
        with open(f'{report_path_prefix}.profile.txt', 'w') as profile_file:
            self._print_segments(profile_file, verbose)
            self._print_totals(profile_file)
            self._print_segment_errors(profile_file)
        with open(f'{report_path_prefix}.graph_dump.txt', 'w') as graph_dump_file:
            self._print_graph_dump(graph_dump_file)

    def _print_segments(self, file, verbose):
        abridge = self._should_abridge(verbose)
        if abridge:
            self._print_abridged_segments(file)
        else:
            self._print_full_segments(file)
        if abridge:
            print(file=file)
            print(f"More than {MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT} compiled segments "
                  "were run, so only graphs with the highest aggregate runtimes are shown. "
                  "To display a verbose profile see "
                  "https://github.com/octoml/octoml-profile#the-profile-report", file=file)
            print(file=file)

    def _add_compiled_abridged_row(self, table, subgraph, num_subgraphs_aggregated=0):
        # Take the first backend's number of samples as the number of
        # samples for the whole graph. Assumes each backend has the same
        # number of samples.
        result = list(subgraph.results_per_backend.values())[0]
        num_samples = result.num_samples + result.num_failures
        if num_subgraphs_aggregated:
            table.append((f"{num_subgraphs_aggregated} other subgraphs",))
        else:
            num_calls = num_samples // self.num_repeats // self.num_runs
            table.append((f"Graph #{subgraph.graph_id} ({num_calls} calls)",))
        num_repeats = self.num_repeats
        num_runs = self.num_runs

        for backend, result in subgraph.results_per_backend.items():
            total = self.total_per_backend[backend].estimated_total_ms
            if self.compilation_occurred:
                if result.mean_ms is None:
                    mean_ms = "N/A"
                    per_run_mean_ms = "N/A"
                else:
                    mean_ms = f"{result.mean_ms:.3f}"
                    per_run_mean_ms = result.mean_ms * (num_samples / num_repeats)
                    per_run_mean_ms = f"{per_run_mean_ms:.3f}"
                table.append(("  " + backend, mean_ms, per_run_mean_ms, result.num_failures))
            else:
                if result.mean_ms is None:
                    mean_ms, per_run_mean_ms, percent_of_run = ("N/A", "N/A", "N/A")
                elif total is None:
                    mean_ms = f"{result.mean_ms:.3f}"
                    per_run_mean_ms, percent_of_run = ("N/A", "N/A")
                else:
                    mean_ms = result.mean_ms
                    per_run_mean_ms = mean_ms * (num_samples / num_runs / num_repeats)
                    percent_of_run = 100 * per_run_mean_ms / total
                    mean_ms = f"{mean_ms:.3f}"
                    per_run_mean_ms = f"{per_run_mean_ms:.3f}"
                    percent_of_run = f"{percent_of_run:.1f}"
                if num_subgraphs_aggregated:
                    mean_ms = ""
                table.append(("  " + backend,
                              mean_ms, per_run_mean_ms, percent_of_run, result.num_failures))

    def _print_abridged_segments(self, file):
        if self.compilation_occurred:
            table = [
                ("Top subgraph", "Avg ms/call", "Avg ms/run", "Failures"),
                "="
            ]
        else:
            table = [
                ("Top subgraph", "Avg ms/call", "Avg ms/run", "Runtime % of e2e", "Failures"),
                "="
            ]
        graphs = {}
        for segment in self._compiled_segments():
            gid = segment.graph_id
            if gid not in graphs:
                graphs[gid] = segment
            else:
                graphs[gid].add(segment)

        graphs = sorted(graphs.values(), key=lambda x: x.total_ms(), reverse=True)

        # Add top n subgraphs rows
        n = MAX_COMPILED_SEGMENTS_DISPLAYED_DEFAULT
        top_graphs = graphs[:n]
        for subgraph in top_graphs:
            self._add_compiled_abridged_row(table, subgraph)
            table.append('')

        # Add 'other subgraphs' row
        if len(graphs) > len(top_graphs):
            other_graphs_sum = graphs[n]
            for graph in graphs[n + 1:]:
                other_graphs_sum.add(graph)
            self._add_compiled_abridged_row(table, other_graphs_sum,
                                            num_subgraphs_aggregated=len(graphs) - len(top_graphs))
            table.append('')

        # Add 'local python segments total' row
        if not self.compilation_occurred:
            num_uncompiled = len([s for s in self.segments if s.graph_id is None])
            num_segments = f'{num_uncompiled} local python segments'
            sum_mean_ms = f'{self.total_uncompiled_ms:.3f}'
            table.append((num_segments, "", sum_mean_ms))
        table.append('-')

        if self.compilation_occurred:
            _print_table(table, "<>>>", file)
        else:
            _print_table(table, "<>>>>", file)

    def _print_full_segments(self, file):
        table = [
            ("", "Segment", "Samples", "Avg ms", "Failures"),
            "="
        ]
        for segment_idx, segment in enumerate(self.segments):
            if segment.graph_id is None:
                r = segment.results_per_backend["Uncompiled"]
                table.append((segment_idx, "Local python", r.num_samples, f"{r.mean_ms:.3f}"))
            else:
                table.append('')
                table.append((segment_idx, f"Graph #{segment.graph_id}",))
                for backend, result in segment.results_per_backend.items():
                    mean_ms = "N/A" if result.mean_ms is None else f"{result.mean_ms:.3f}"
                    table.append(("", "  " + backend,
                                  result.num_samples, mean_ms, result.num_failures))
                table.append('')
        table.append('-')
        _print_table(table, "><>>>", file)

    def _print_totals(self, file):
        table = [
            ("Instance", "Processor", "Backend",
             "Backend Time (ms)", "Total Time (ms)", "Cost ($/MReq)"),
            "="
        ]
        backend_hide_total_time = []
        for backend, total_res in self.total_per_backend.items():
            backend_ms, total_ms, cost = "N/A", "N/A", "N/A"
            if total_res.estimated_total_ms is not None:
                total_ms = f"{total_res.estimated_total_ms:.3f}"
                backend_ms = f"{(total_res.estimated_total_ms - self.total_uncompiled_ms):.3f}"
                per_hr = AWS_ON_DEMAND_PER_HOUR.get(backend.split('/')[0])
                if per_hr is None:
                    cost = "N/A"
                else:
                    cost_per_req = per_hr * total_res.estimated_total_ms / (3600 * 1000)
                    cost_per_mreq = 1e6 * cost_per_req
                    cost = f"${cost_per_mreq:.2f}"

            info = BackendDescription.from_backend_spec(backend)
            hide_total_time = (self.compilation_occurred
                               or len(total_res.errors) > 0
                               or len(self.compilation_errors) > 0)
            if hide_total_time:
                total_ms = "N/A"
                cost = "N/A"
            backend_hide_total_time.append(hide_total_time)
            table.append((info.instance, info.processor, info.software_backend,
                          backend_ms, total_ms, cost))
        table.append('-')
        _print_table(table, "<<<>>>", file)
        if not all(backend_hide_total_time):
            uncompiled_time = f'{self.total_uncompiled_ms:.3f} ms'
            print(f'Total time above is `remote backend time + local python code time`,\n',
                  f'in which local python code run time is {uncompiled_time}.', file=file)

    def _print_warnings(self, file):
        if len(self.compilation_errors) > 0:
            print(f'WARNING: Total time and cost is not shown because some graphs fail to '
                  f'compile and falls back to running locally.', file=file)
        elif any([total.errors for total in self.total_per_backend.values()]):
            print('WARNING: Total time and cost is not shown for some backends because\n'
                  'some graphs fail to execute remotely and falls back to running locally.',
                  file=file)
        elif self.compilation_occurred:
            print(f'NOTE: Total time and cost is not shown because compilation has happened\n'
                  f'during this run. This can happen if `accelerate(dynamic=True)` is used\n'
                  f'and TorchDynamo compiles a different trace for the first run. In this case\n'
                  f'you can ignore this profile and find more profiles without compilation.\n'
                  f'Or you may need to run the decorated function multiple times\n'
                  f'in the `remote_profile` context to get the total time and cost.',
                  file=file)
            print(f'''For example:

    with remote_profile():
        # Compilation can depend on shape and dtype of the input.
        # Make sure each input gets invoked at least twice
        for _ in range(3):
            for input in dataset:
                {self.func_name}(input)''', file=file)

    def _print_segment_errors(self, file):
        for backend, total_res in self.total_per_backend.items():
            if not total_res.errors:
                continue
            print(f'    {backend}', file=file)
            for error in total_res.errors:
                graph_str = f'       Graph #{error.graph_id} - '
                print(graph_str, end='', file=file)
                for i, (error, count) in enumerate(error.error_messages_to_count.items()):
                    if i > 0:
                        print('\n', ' ' * (len(graph_str) - 1), end='', file=file)
                    print(f'{count} errors: {error}', end='', file=file)
                print(file=file)

    def _print_graph_dump(self, file):
        visited = set()
        for graph in self.graph_results:
            id = graph.graph_id
            if id in visited:
                continue
            visited.add(id)
            start = list(graph.graph_module.graph.nodes)[0].stack_trace
            reason = graph.compile_reason.reason

            print(f"Graph #{id} ends due to \"{reason}\"", file=file)
            for frame in graph.compile_reason.user_stack:
                start = start.strip().replace("File", "file")
                print(f"  From {start}", file=file)
                print(f"  To file \"{frame.filename}\", line {frame.lineno}", file=file)
                print(f"    {frame.line}", file=file)

            # print_tabular code below is taken from
            # https://github.com/pytorch/pytorch/blob/5bcbb9bca714ebf105c407390d5fe293876d8634/torch/fx/graph.py#L1283-L1298
            node_specs = [[n.op, n.name, n.target, n.args, n.kwargs]
                          for n in graph.graph_module.graph.nodes]
            print(tabulate(node_specs,
                           headers=['opcode', 'name', 'target', 'args', 'kwargs']), file=file)


@dataclass
class ProfileReport:
    profiles: List[Profile]
    compilation_errors: List[str]
    report_dir: str

    def print(self, *, file=sys.stdout, verbose=False):
        os.makedirs(self.report_dir, exist_ok=True)
        if len(self.profiles) == 0:
            print('Profiling was enabled but no results were recorded', file=file)

        profiles_by_func = defaultdict(list)
        for p in self.profiles:
            profiles_by_func[p.func_name].append(p)

        for func in profiles_by_func.keys():
            profiles = profiles_by_func[func]

            num_profiles = "1 profile" if len(profiles) == 1 else f"{len(profiles)} profiles"
            print(file=file)
            print(f'Function `{func}` has {num_profiles}:', file=file)
            for i, p in enumerate(profiles):
                profile_id = f'{func}[{i+1}/{len(profiles)}]'
                total_runs = p.num_runs + p.num_discarded_runs
                runs = "1 time" if total_runs == 1 else f'{total_runs} times'
                header = f'- Profile `{profile_id}` ran {runs}.'
                if p.num_discarded_runs > 0:
                    header += f' ({p.num_discarded_runs} discarded because compilation happened)'
                elif p.compilation_occurred:
                    header += f' (compilation occurred)'
                print(header + "\n", file=file)
                path_prefix = f'{self.report_dir}/{func}_{i+1}'
                p.print(file=file, report_path_prefix=path_prefix, verbose=verbose)
                print(file=file)

        if len(self.compilation_errors):
            print(f"WARNING: {len(self.compilation_errors)} graphs fail to compile+load "
                  f"on the remote machine and fall back running locally.", file=file)
        for e in self.compilation_errors:
            print("  " + e, file=file)
        has_runtime_error = any(
            [total.errors for total in p.total_per_backend.values() for p in self.profiles]
        )
        if has_runtime_error or len(self.compilation_errors) > 0:
            print(f"Please file report to https://github.com/octoml/octoml-profile/issues "
                  f"with full client-side trace at {LOGFILE}")

    @property
    def runtime_errors(self) -> Dict[str, List[str]]:
        runtime_errors = defaultdict(list)
        for profile in self.profiles:
            for k, total in profile.total_per_backend.items():
                if not total.errors:
                    continue
                for error in total.errors:
                    for error_msg in error.error_messages_to_count.keys():
                        runtime_errors[k].append(error_msg)
        return runtime_errors


def _string_width(s):
    # FIXME: use wcwidth if we need to display non-latin characters
    return len(str(s))


_align = {
    '<': lambda s, width: s + ' ' * max(0, width - _string_width(s)),
    '>': lambda s, width: ' ' * max(0, width - _string_width(s)) + s
}


def _print_table(rows, column_alignment: str, file):
    col_spacing = 2
    col_spacing_str = ' ' * col_spacing
    num_cols = len(column_alignment)
    column_alignment = tuple(_align[a] for a in column_alignment)

    col_width = [0] * num_cols
    for row in rows:
        if not isinstance(row, str):
            for i, cell in enumerate(row):
                col_width[i] = max(col_width[i], _string_width(cell))

    total_width = sum(col_width) + col_spacing * (num_cols - 1)
    for row in rows:
        if isinstance(row, str):
            num_reps = 1 if _string_width(row) == 0 else total_width // _string_width(row)
            print(row * num_reps, file=file)
        else:
            print(*(align(str(cell), width)
                    for cell, width, align in zip(row, col_width, column_alignment)),
                  file=file,
                  sep=col_spacing_str)
