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
import torch
import contextlib
from torch._subclasses import FakeTensor
from torch.utils._python_dispatch import _disable_current_modes


def _in_torch_dynamo():
    # TODO: find a better way to determine whether we are inside dynamo
    return torch._guards.TracingContext.get() is not None


@contextlib.contextmanager
def _onnx_export_diagnostic_patch():
    # Hack to disable onnx export diagnostic from printing
    # Headers even when there is no diagnostic
    # Because this relies on private APIs, there are try/except
    # to make sure failure doesn't impact the user experience
    try:
        from torch.onnx._internal.diagnostics.infra import DiagnosticContext
    except ImportError:
        return

    try:
        original_pretty_print = DiagnosticContext.pretty_print
    except AttributeError:
        return

    def pretty_print_only_when_not_empty(self, *args, **kwargs):
        try:
            if len(self.diagnostics) > 0:
                original_pretty_print(self, *args, **kwargs)
        except Exception:
            pass

    DiagnosticContext.pretty_print = pretty_print_only_when_not_empty
    yield
    DiagnosticContext.pretty_print = original_pretty_print


def fake_tensor_unsupported(fn):
    """
    Decorator for backends that need real inputs.  We swap out fake
    tensors for zero tensors.
    """
    def collect_symbolic_hints(maybe_symbols):
        shape = []
        for s in maybe_symbols:
            if hasattr(s, 'node'):
                shape.append(s.node.shape_env.size_hint(s.node.expr))
            else:
                shape.append(s)
        return shape

    def defake(x):
        if not isinstance(x, FakeTensor):
            return x
        if x._has_symbolic_sizes_strides:
            size = collect_symbolic_hints(x.size())
            stride = collect_symbolic_hints(x.stride())
        else:
            size = x.size()
            stride = x.stride()
        y = torch.empty_strided(
            size,
            stride,
            dtype=x.dtype,
            device=x.device,
            requires_grad=x.requires_grad,
        )
        y.zero_()
        return y

    @functools.wraps(fn)
    def wrapper(model, inputs, **kwargs):
        with _disable_current_modes():
            inputs = list(map(defake, inputs))
            return fn(model, inputs, **kwargs)

    return wrapper
