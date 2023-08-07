from __future__ import annotations

import typing as t

import pyarrow as pa

from sarus_data_spec.arrow.admin_utils import (
    async_admin_data,
    validate_admin_data,
)
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

from .utils import static_arguments

STATIC = "static"


class ExternalSignature:
    def __init__(
        self,
        transform: st.Transform,
        ds_args: t.Collection[st.DataSpec],
        ds_kwargs: t.Dict[str, st.DataSpec],
    ):
        py_args, py_kwargs, ds_args_pos, ds_types = static_arguments(transform)
        if len(ds_types) != len(ds_args) + len(ds_kwargs):
            raise ValueError(
                "Incorrect number of types specified in the external protobuf."
            )
        pos_values = {pos: val for pos, val in zip(ds_args_pos, ds_args)}
        pos_args = {**pos_values, **py_args}

        self._kwargs = {**py_kwargs, **ds_kwargs}
        self._args = [pos_args[i] for i in range(len(pos_args))]
        self.args_types = [
            ds_types.get(pos, STATIC) for pos in range(len(self._args))
        ]
        self.kwargs_types = {
            name: ds_types.get(name, STATIC) for name in self._kwargs.keys()
        }

    def args(self) -> t.List[t.Any]:
        return self._args

    def kwargs(self) -> t.Dict[str, t.Any]:
        return self._kwargs

    @staticmethod
    def from_dataspec(dataspec: st.DataSpec) -> ExternalSignature:
        transform = dataspec.transform()
        ds_args, ds_kwargs = dataspec.parents()
        return ExternalSignature(transform, ds_args, ds_kwargs)

    async def arguments_values(
        self,
    ) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
        """Evaluate the transform arguments, named arguments"""
        arg_values_and_pe = [
            await self.evaluate_value_and_admin_data(arg, arg_type)
            for arg, arg_type in zip(self.args(), self.args_types)
        ]
        args_values = [data for data, _ in arg_values_and_pe]

        kwarg_values_and_pe = {
            name: await self.evaluate_value_and_admin_data(
                arg, self.kwargs_types[name]
            )
            for name, arg in self.kwargs().items()
        }
        kwargs_values = {
            name: data for name, (data, _) in kwarg_values_and_pe.items()
        }

        return args_values, kwargs_values

    async def arguments_values_and_admin_data(
        self,
    ) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any], pa.Table]:
        """Evaluate the transform arguments, named arguments and
        protected entity.
        """
        arg_values_and_pe = [
            await self.evaluate_value_and_admin_data(arg, arg_type)
            for arg, arg_type in zip(self.args(), self.args_types)
        ]
        args_values = [data for data, _ in arg_values_and_pe]
        args_pe = [pe for _, pe in arg_values_and_pe]

        kwarg_values_and_pe = {
            name: await self.evaluate_value_and_admin_data(
                arg, self.kwargs_types[name]
            )
            for name, arg in self.kwargs().items()
        }
        kwargs_values = {
            name: data for name, (data, _) in kwarg_values_and_pe.items()
        }
        kwargs_pe = [pe for _, pe in kwarg_values_and_pe.values()]

        input_protected_entities = list(
            filter(lambda x: x is not None, args_pe + kwargs_pe)
        )
        protected_entity = validate_admin_data(input_protected_entities)

        return args_values, kwargs_values, protected_entity

    async def evaluate_value_and_admin_data(
        self, arg: t.Any, arg_type: str
    ) -> t.Tuple[t.Any, t.Optional[pa.Table]]:
        """Evaluate an argument.

        - Datasets are evaluated to the specified type using
          `dataset.to(type)`.
        - Scalar are evaluated using `scalar.value()`.
        - Static arguments are return as such.

        Returns a Tuple with the data and the protected entity if present. The
        protected entity is represented as pyarrow Table.
        """
        type_mapping = {
            str(kind): kind for kind in t.get_args(st.DatasetCastable)
        }
        protected_entity: t.Optional[pa.Table]
        if arg_type == STATIC:
            protected_entity = None
            return arg, protected_entity

        dataspec = t.cast(st.DataSpec, arg)
        if dataspec.prototype() == sp.Scalar:
            scalar = t.cast(st.Scalar, arg)
            protected_entity = None
            return await scalar.async_value(), protected_entity
        else:
            dataset = t.cast(st.Dataset, arg)
            protected_entity = await async_admin_data(dataset)
            return (
                await dataset.async_to(type_mapping[arg_type]),
                protected_entity,
            )

    async def _value_and_pe(
        self, name: str, position: t.Optional[int] = None
    ) -> t.Any:
        """Evaluate an argument by name or position.

        This is a helper function that will be removed in further iterations.
        """
        if name in self.kwargs():
            arg = self.kwargs().get(name)
            arg_type = self.kwargs_types[name]
        elif position is None:
            raise ValueError(
                f"Could not find {name} in kwargs. Please specify a position."
            )
        else:
            arg = self.args()[position]
            arg_type = self.args_types[position]
        return await self.evaluate_value_and_admin_data(arg, arg_type)
