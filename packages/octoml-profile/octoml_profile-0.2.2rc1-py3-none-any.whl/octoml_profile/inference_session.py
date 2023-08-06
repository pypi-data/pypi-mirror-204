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
import hashlib
import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Sequence, Mapping, Tuple, Callable, Iterator, Optional, Union
from collections import OrderedDict

import numpy as np

from .conversion_util import proto_to_numpy
from .protos import remote_inference_pb2 as pb


class BackendOptions(OrderedDict):

    @staticmethod
    def parse(spec: str) -> 'BackendOptions':
        """
        Args:
            spec: option string "k1,k2=v2,..."

        `spec` is comma separated. Each token is either a `k` (key) or a `k=v` (key, value) pairs.
        """
        opts = BackendOptions()
        for token in spec.split(","):
            key_value = token.split("=")
            if len(key_value) == 1:
                key, value = key_value[0], ""
            elif len(key_value) == 2:
                key, value = key_value
            else:
                raise ValueError(f"Malformed backend option: {spec}. Backend options"
                                 f" have the form of \"k1,k2=v2,k3=v3\".")
            opts[key.strip()] = value.strip()
        return opts

    @staticmethod
    def from_pb(options: Sequence[pb.BackendOption]) -> "BackendOptions":
        opts = BackendOptions()
        for kv in options:
            opts[kv.key] = kv.value
        return opts

    def __str__(self):
        if len(self) == 0:
            return ""
        else:
            return "[" + ",".join(f"{k}={v}" if v != "" else k for k, v in self.items()) + "]"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(sorted(self.items())))

    def __eq__(self, other):
        return dict(self) == dict(other)


@dataclass(eq=True, frozen=True)
class BackendSpec:
    hardware_platform: str
    software_backend: str
    backend_options: BackendOptions = field(default_factory=BackendOptions)

    @staticmethod
    def parse(spec: str) -> 'BackendSpec':
        hw_and_sw = spec.split('/', maxsplit=1)
        if len(hw_and_sw) != 2:
            raise ValueError('Backend spec string must contain a hardware platform name'
                             ' and a software backend name, separated by a slash,'
                             ' e.g. "aws-v100/onnxrt-cuda"')
        hardware_platform, software_backend = hw_and_sw
        if software_backend.endswith("]"):
            option_begin = software_backend.find("[")
            if option_begin < 0:
                raise ValueError('Backend options must be included in [],'
                                 ' e.g. "g5.xlarge/torch-eager-cuda[fp16]')
            option_spec = software_backend[option_begin + 1: -1]
            software_backend = software_backend[:option_begin]
            backend_options = BackendOptions.parse(option_spec)
        else:
            backend_options = BackendOptions()
        return BackendSpec(hardware_platform, software_backend, backend_options)

    def __str__(self):
        return f"{self.hardware_platform}/{self.software_backend}{self.backend_options}"

    def __repr__(self):
        return str(self)

    def __format__(self, format_spec):
        return format(str(self), format_spec)


@dataclass
class ResultValue:
    outputs: Tuple[np.ndarray, ...]
    run_times_nanos: np.ndarray  # 1D array of int64


@dataclass
class RunResult:
    result_value: Optional[ResultValue]
    error_value: Optional[str]

    @staticmethod
    def from_pb(result: pb.RunResult) -> "RunResult":
        result_value, error_value = None, None
        if result.HasField("result_value"):
            result_value = ResultValue(
                outputs=tuple(proto_to_numpy(x) for x in result.result_value.outputs),
                run_times_nanos=np.array(result.result_value.run_times_nanos, dtype=np.int64)
            )
        else:
            error_value = result.error_value
        return RunResult(result_value, error_value)


class ModelRunner:
    def submit_run(self, inputs,
                   num_repeats=None,
                   num_warmups=None,
                   mode=None) -> Callable[[], Mapping[BackendSpec, RunResult]]:
        raise NotImplementedError


BytesLike = Union[bytes, bytearray, memoryview]


class FileDescription:
    def name(self) -> str:
        raise NotImplementedError()

    @contextmanager
    def open(self, chunk_size: int) -> Tuple[int, Iterator[bytes]]:
        raise NotImplementedError()

    def sha256(self):
        raise NotImplementedError()


class OnDiskFile(FileDescription):
    def __init__(self, model_dir, relative_filename):
        self._relative_filename = relative_filename
        self._full_name = os.path.join(model_dir, relative_filename)

    def name(self) -> str:
        return self._relative_filename

    @contextmanager
    def open(self, chunk_size: int) -> Tuple[int, Iterator[bytes]]:
        with open(self._full_name, "rb", buffering=0) as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(0, 0)
            yield size, iter(functools.partial(f.read, chunk_size), b'')

    def sha256(self):
        hash = hashlib.sha256()
        buf = bytearray(64 * 1024)
        view = memoryview(buf)
        with open(self._full_name, "rb", buffering=0) as file:
            while True:
                bytes_read = file.readinto(view)
                if bytes_read == 0:
                    break
                hash.update(view[:bytes_read])
        return hash.digest()


def _rechunk(original_chunks: Iterator[BytesLike],
             new_chunk_size: int) -> Iterator[bytes]:
    buf = bytearray(new_chunk_size)
    free = memoryview(buf)

    for orig_chunk in original_chunks:
        orig_view = memoryview(orig_chunk)
        while True:
            if len(orig_view) <= len(free):
                free[:len(orig_view)] = orig_view
                free = free[len(orig_view):]
                break
            elif len(free) == new_chunk_size:
                yield bytes(orig_view[:new_chunk_size])
                orig_view = orig_view[new_chunk_size:]
            else:
                free[:] = orig_view[:len(free)]
                yield bytes(buf)
                orig_view = orig_view[len(free):]
                free = memoryview(buf)

    remainder = len(buf) - len(free)
    if remainder > 0:
        del free  # remove reference to buf so that we can resize it
        del buf[remainder:]
        yield bytes(buf)


class LazyInMemoryFile(FileDescription):
    def __init__(self, filename: str,
                 contents_provider: Callable[[], Tuple[int, Iterator[BytesLike]]]):
        self._filename = filename
        self._contents_provider = contents_provider

    def name(self) -> str:
        return self._filename

    @contextmanager
    def open(self, chunk_size: int) -> Tuple[int, Iterator[bytes]]:
        len, chunks = self._contents_provider()
        yield len, _rechunk(chunks, chunk_size)

    def sha256(self):
        hash = hashlib.sha256()
        _len, chunks = self._contents_provider()
        for chunk in chunks:
            hash.update(chunk)
        return hash.digest()


class InferenceSession:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        raise NotImplementedError()

    def load_model(self,
                   model_id: int,
                   backend_ids: Sequence[int],
                   model_format: pb.ModelFormat,
                   model_files: Sequence[FileDescription],
                   input_names: Sequence[str],
                   output_names: Sequence[str]):
        raise NotImplementedError()

    def create_runner(self, model_id: int,
                      input_map_per_backend: Sequence[Sequence[int]]) -> ModelRunner:
        raise NotImplementedError()
