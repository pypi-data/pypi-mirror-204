"""
This module encodes bilayer models into a SMTLib formula.  

"""
import logging
from functools import reduce
from typing import Dict, List, Set, Union

import pysmt
from pysmt.formula import FNode
from pysmt.shortcuts import (
    GE,
    GT,
    LE,
    LT,
    TRUE,
    And,
    Equals,
    Minus,
    Plus,
    Real,
    Symbol,
    Times,
    simplify,
)
from pysmt.typing import REAL

from funman.model.bilayer import (
    BilayerEdge,
    BilayerFluxNode,
    BilayerMeasurement,
    BilayerModel,
    BilayerNode,
    BilayerStateNode,
)
from funman.model.model import Model
from funman.representation import Parameter
from funman.representation.representation import Box, Interval
from funman.translate import Encoder, Encoding, EncodingOptions

l = logging.Logger(__name__)


# class BilayerEncodingOptions(EncodingOptions):
#     """
#     The BilayerEncodingOptions are:

#     * step_size: the number of time units separating encoding steps

#     * max_steps: the number of encoding steps

#     """

#     def __init__(self, step_size=1, max_steps=2) -> None:
#         super().__init__(max_steps)
#         self.step_size = step_size
#         self.max_steps = max_steps


class BilayerEncoder(Encoder):
    """
    The BilayerEncoder compiles a BilayerModel into a SMTLib formula.  The
    formula defines a series of steps that update a set of variables each step,
    as defined by a Bilayer model.
    """

    class Config:
        underscore_attrs_are_private = True

    _timed_symbols: Set[str] = set([])
    _untimed_symbols: Set[str] = set([])
    _timed_model_elements: Dict = None
    _untimed_constraints: FNode
    _min_time_point: int
    _min_step_size: int

    def get_structural_configurations(self, model: Model):
        configurations: List[Dict[str, int]] = []
        if len(model.structural_parameter_bounds) == 0:
            self._min_time_point = 0
            self._min_step_size = 1
            num_steps = [1, self.config.num_steps]
            step_size = [1, self.config.step_size]
            max_step_size = self.config.step_size
            max_step_index = self.config.num_steps * max_step_size
            configurations.append(
                {
                    "num_steps": self.config.num_steps,
                    "step_size": self.config.step_size,
                }
            )
        else:
            num_steps = model.structural_parameter_bounds["num_steps"]
            step_size = model.structural_parameter_bounds["step_size"]
            self._min_time_point = num_steps[0]
            self._min_step_size = step_size[0]
            max_step_size = step_size[1]
            max_step_index = num_steps[1] * max_step_size
            configurations += [
                {"num_steps": ns, "step_size": ss}
                for ns in range(num_steps[0], num_steps[1] + 1)
                for ss in range(step_size[0], step_size[1] + 1)
            ]
        return configurations, max_step_index, max_step_size

    def get_timepoints(self, num_steps, step_size):
        state_timepoints = range(
            0,
            (step_size * num_steps) + 1,
            step_size,
        )

        if len(list(state_timepoints)) == 0:
            raise Exception(
                f"Could not identify timepoints from step_size = {step_size} and num_steps = {num_steps}"
            )

        transition_timepoints = range(0, step_size * num_steps, step_size)
        return list(state_timepoints), list(transition_timepoints)

    def _encode_next_step(
        self,
        model: Model,
        step: int,
        next_step: int,
        time_dependent_parameters=None,
    ):
        transition = self._encode_bilayer(
            model.bilayer,
            [step, next_step],
            time_dependent_parameters=time_dependent_parameters,
        )
        if model.measurements:
            measurements = self._encode_measurements(
                model.measurements, [step + next_step]
            )
        else:
            measurements = TRUE()

        return And(transition, measurements).simplify()

    def _encode_untimed_constraints(
        self, model: Model, time_dependent_parameters=False
    ):
        untimed_constraints = []
        parameters = model._parameters()
        if not time_dependent_parameters:
            untimed_constraints.append(
                self.box_to_smt(
                    Box(
                        bounds={
                            p.name: Interval(lb=p.lb, ub=p.ub)
                            for p in parameters
                        },
                        closed_upper_bound=True,
                    )
                )
            )
            # Encode that all of the identical parameters are equal
            untimed_constraints.append(
                And(
                    [
                        Equals(Symbol(var1, REAL), Symbol(var2, REAL))
                        for group in model.identical_parameters
                        for var1 in group
                        for var2 in group
                        if var1 != var2
                    ]
                ).simplify()
            )
        return And(untimed_constraints).simplify()

    def _encode_timed_model_elements(
        self, model: Model, time_dependent_parameters=False
    ):
        # All state nodes correspond to timed symbols
        for idx, node in model.bilayer._state.items():
            self._timed_symbols.add(node.parameter)

        # All flux nodes correspond to untimed symbols
        for _, node in model.bilayer._flux.items():
            self._untimed_symbols.add(node.parameter)

        (
            configurations,
            max_step_index,
            max_step_size,
        ) = self.get_structural_configurations(model)
        self._timed_model_elements = {
            "init": self._define_init(model),
            "time_step_constraints": [
                [None for i in range(max_step_size)]
                for j in range(max_step_index)
            ],
            "configurations": configurations,
            "untimed_constraints": self._encode_untimed_constraints(model),
            "timed_parameters": [
                [None for i in range(max_step_size)]
                for j in range(max_step_index)
            ],
        }

    def encode_model_timed(
        self,
        model: Model,
        num_steps: int,
        step_size: int,
        time_dependent_parameters: bool = False,
    ):
        if self._timed_model_elements is None:
            self._timed_model_elements = self._encode_timed_model_elements(
                model, time_dependent_parameters=time_dependent_parameters
            )

        state_timepoints, transition_timepoints = self.get_timepoints(
            num_steps, step_size
        )
        parameters = model._parameters()

        constraints = []

        for i, timepoint in enumerate(transition_timepoints):
            c = self._timed_model_elements["time_step_constraints"][timepoint][
                step_size - self._min_step_size
            ]
            if c is None:
                c = self._encode_next_step(
                    model,
                    state_timepoints[i],
                    state_timepoints[i + 1],
                    time_dependent_parameters=None,
                )
                self._timed_model_elements["time_step_constraints"][timepoint][
                    step_size - self._min_step_size
                ] = c
            constraints.append(c)

            if time_dependent_parameters:
                params = self._timed_model_elements["timed_parameters"][
                    timepoint
                ][step_size - self._min_step_size]
                if params == []:
                    params = [p.timed_copy(timepoint) for p in parameters]
                    self._timed_model_elements["timed_parameters"][timepoint][
                        step_size - self._min_step_size
                    ] = params
                constraints.append(
                    self.box_to_smt(
                        Box(
                            bounds={
                                p.name: Interval(lb=p.lb, ub=p.ub)
                                for p in timed_parameters
                            }
                        ),
                        closed_upper_bound=True,
                    )
                )

        if time_dependent_parameters:
            # FIXME cache this computation
            ## Assume that all parameters are constant
            constraints.append(
                self._set_parameters_constant(
                    parameters,
                    constraints,
                ),
            )

        formula = And(
            And(
                [
                    self._timed_model_elements["init"],
                    self._timed_model_elements["untimed_constraints"],
                ]
                + constraints
            ).simplify(),
            (model._extra_constraints if model._extra_constraints else TRUE()),
        ).simplify()
        symbols = self._symbols(formula)
        return Encoding(_formula=formula, _symbols=symbols)

    def encode_model(self, model: Model, time_dependent_parameters=False):
        """
        Encode the model as an SMTLib formula.

        Parameters
        ----------
        model : Model
            model to encode

        Returns
        -------
        FNode
            formula encoding the model

        Raises
        ------
        Exception
            cannot identify encoding timepoints
        Exception
            cannot encode model type
        """
        if isinstance(model, BilayerModel):
            state_timepoints = range(
                0,
                (self.config.num_steps * self.config.step_size) + 1,
                self.config.step_size,
            )

            if len(list(state_timepoints)) == 0:
                raise Exception(
                    f"Could not identify timepoints from step_size = {self.config.step_size} and num_steps = {self.config.num_steps}"
                )

            transition_timepoints = range(
                0,
                self.config.num_steps * self.config.step_size,
                self.config.step_size,
            )

            # All state nodes correspond to timed symbols
            for idx, node in model.bilayer._state.items():
                self._timed_symbols.add(node.parameter)

            # All flux nodes correspond to untimed symbols
            for _, node in model.bilayer._flux.items():
                self._untimed_symbols.add(node.parameter)

            init = self._define_init(model)

            encoding = self._encode_bilayer(
                model.bilayer,
                state_timepoints,
                time_dependent_parameters=time_dependent_parameters,
            )

            if model.parameter_bounds:
                parameters = [
                    Parameter(
                        name=node.parameter,
                        lb=model.parameter_bounds[node.parameter][0],
                        ub=model.parameter_bounds[node.parameter][1],
                    )
                    for _, node in model.bilayer._flux.items()
                    if node.parameter in model.parameter_bounds
                    and model.parameter_bounds[node.parameter]
                ]
                if model.measurements:
                    parameters += [
                        Parameter(
                            name=node.parameter,
                            lb=model.parameter_bounds[node.parameter][0],
                            ub=model.parameter_bounds[node.parameter][1],
                        )
                        for _, node in model.measurements._flux.items()
                        if node.parameter in model.parameter_bounds
                        and model.parameter_bounds[node.parameter]
                    ]
                if time_dependent_parameters:
                    timed_parameters = [
                        p.timed_copy(timepoint)
                        for p in parameters
                        for timepoint in transition_timepoints
                    ]
                    parameter_box = Box(
                        bounds={
                            p.name: Interval(lb=p.lb, ub=p.ub)
                            for p in timed_parameters
                        }
                    )
                else:
                    parameter_box = Box(
                        bounds={
                            p.name: Interval(lb=p.lb, ub=p.ub)
                            for p in parameters
                        }
                    )
                parameter_constraints = self.box_to_smt(
                    parameter_box, closed_upper_bound=True
                )
            else:
                parameter_constraints = TRUE()

            if model.measurements:
                measurements = self._encode_measurements(
                    model.measurements, state_timepoints
                )
            else:
                measurements = TRUE()

            if time_dependent_parameters:
                ## Assume that all parameters are constant
                parameter_constraints = And(
                    parameter_constraints,
                    self._set_parameters_constant(
                        [v.parameter for v in model.bilayer._flux.values()],
                        encoding,
                    ),
                )
                if model.measurements:
                    parameter_constraints = And(
                        parameter_constraints,
                        self._set_parameters_constant(
                            [
                                v.parameter
                                for v in model.measurements._flux.values()
                            ],
                            measurements,
                        ),
                    )
            else:
                pass

            # Encode that all of the identical parameters are equal
            identical_parameters = And(
                [
                    Equals(Symbol(var1, REAL), Symbol(var2, REAL))
                    for group in model.identical_parameters
                    for var1 in group
                    for var2 in group
                    if var1 != var2
                ]
            ).simplify()

            formula = And(
                init,
                parameter_constraints,
                encoding,
                measurements,
                identical_parameters,
                (
                    model._extra_constraints
                    if model._extra_constraints
                    else TRUE()
                ),
            )
            symbols = self._symbols(formula)
            return Encoding(_formula=formula, _symbols=symbols)
        else:
            raise Exception(
                f"BilayerEncoder cannot encode model of type: {type(model)}"
            )

    def _define_init(self, model):
        if self.config.initial_state_tolerance == 0.0:
            return And(
                [
                    Equals(
                        self._encode_bilayer_state_node(node, timepoint=0),
                        Real(model.init_values[node.parameter]),
                    )
                    for idx, node in model.bilayer._state.items()
                ]
            )
        else:
            return And(
                [
                    And(
                        LE(
                            Real(-1.0 * self.config.initial_state_tolerance),
                            Minus(
                                self._encode_bilayer_state_node(
                                    node, timepoint=0
                                ),
                                Real(model.init_values[node.parameter]),
                            ),
                        ),
                        LE(
                            Minus(
                                self._encode_bilayer_state_node(
                                    node, timepoint=0
                                ),
                                Real(model.init_values[node.parameter]),
                            ),
                            Real(self.config.initial_state_tolerance),
                        ),
                    )
                    for idx, node in model.bilayer._state.items()
                ]
            )

    def _encode_measurements(
        self, measurements: BilayerMeasurement, timepoints
    ):
        ans = And(
            [
                self._encode_measurements_timepoint(
                    measurements, timepoints[i]
                )
                for i in range(len(timepoints))
            ]
        )
        return ans

    def _encode_measurements_timepoint(self, measurements, t):
        observable_defs = And(
            [
                Equals(
                    self._encode_bilayer_state_node(o, t),
                    self._observable_defn(measurements, o, t),
                )
                for o in measurements.observable.values()
            ]
        )
        return observable_defs

    def _encode_bilayer(
        self, bilayer, timepoints, time_dependent_parameters=False
    ):
        ans = simplify(
            And(
                [
                    self._encode_bilayer_timepoint(
                        bilayer,
                        timepoints[i],
                        timepoints[i + 1],
                        time_dependent_parameters=time_dependent_parameters,
                    )
                    for i in range(len(timepoints) - 1)
                ]
            )
        )
        return ans

    def _encode_bilayer_timepoint(
        self,
        bilayer,
        timepoint,
        next_timepoint,
        time_dependent_parameters=False,
    ):
        ## Calculate time step size
        time_step_size = next_timepoint - timepoint
        eqns = (
            []
        )  ## List of SMT equations for a given timepoint. These will be
        ## joined by an "And" command and returned

        for t in bilayer._tangent:  ## Loop over _tangents (derivatives)
            pos_derivative_expr_terms = []
            neg_derivative_expr_terms = []
            ## Get _tangent variable and translate it to SMT form tanvar_smt
            tanvar = bilayer._tangent[t].parameter
            tanvar_smt = self._encode_bilayer_state_node(
                bilayer._tangent[t],
                timepoint=timepoint,
            )
            state_var_next_step = bilayer._state[t].parameter
            state_var_smt = self._encode_bilayer_state_node(
                bilayer._state[t], timepoint=timepoint
            )
            state_var_next_step_smt = self._encode_bilayer_state_node(
                bilayer._state[t], timepoint=next_timepoint
            )

            relevant_output_edges = [
                (val, val.src.index)
                for val in bilayer._output_edges
                if val.tgt.index == bilayer._tangent[t].index
            ]
            for flux_sign_index in relevant_output_edges:
                flux_term = bilayer._flux[flux_sign_index[1]]
                output_edge = bilayer._output_edges[flux_sign_index[1]]
                expr = self._encode_bilayer_flux_node(
                    flux_term,
                    timepoint=(
                        timepoint if time_dependent_parameters else None
                    ),
                )
                ## Check which state vars go to that param
                relevant_input_edges = [
                    self._encode_bilayer_state_node(
                        bilayer._state[val2.src.index], timepoint=timepoint
                    )
                    for val2 in bilayer._input_edges
                    if val2.tgt.index == flux_sign_index[1]
                ]
                for state_var in relevant_input_edges:
                    expr = Times(expr, state_var)
                if (
                    self._encode_bilayer_edge(flux_sign_index[0], timepoint)
                    == "positive"
                ):
                    pos_derivative_expr_terms.append(expr)
                elif (
                    self._encode_bilayer_edge(flux_sign_index[0], timepoint)
                    == "negative"
                ):
                    neg_derivative_expr_terms.append(expr)
            # Assemble into equation of the form f(t + delta t) approximately =
            # f(t) + (delta t) f'(t)
            pos_terms = (
                reduce(lambda a, b: Plus(a, b), pos_derivative_expr_terms)
                if len(pos_derivative_expr_terms) > 0
                else Real(0.0)
            )
            neg_terms = (
                reduce(lambda a, b: Plus(a, b), neg_derivative_expr_terms)
                if len(neg_derivative_expr_terms) > 0
                else Real(0.0)
            )
            # noise = Symbol(f"noise_{state_var_next_step_smt}", REAL)
            # self._timed_symbols.add(f"{noise}".rsplit("_", 1)[0])
            eqn = simplify(
                And(
                    LE(
                        state_var_next_step_smt,
                        Plus(
                            state_var_smt,
                            Times(
                                Real(time_step_size),
                                Minus(pos_terms, neg_terms),
                            ),
                            Real(self.config.constraint_noise),
                        ),
                    ),
                    GE(
                        state_var_next_step_smt,
                        Plus(
                            state_var_smt,
                            Times(
                                Real(time_step_size),
                                Minus(pos_terms, neg_terms),
                            ),
                            Real(-self.config.constraint_noise),
                        ),
                    ),
                )
            )
            # print(eqn)
            eqns.append(eqn)
        return And(eqns)

    def _encode_bilayer_node(self, node, timepoint=None):
        if not isinstance(node, BilayerNode):
            raise Exception("Node is not a BilayerNode")
        param = node.parameter
        if timepoint is not None:
            ans = Symbol(f"{param}_{timepoint}", REAL)
        else:
            ans = Symbol(f"{param}", REAL)
        return ans

    def _encode_bilayer_state_node(self, node, timepoint=None):
        if not isinstance(node, BilayerStateNode):
            raise Exception("Node is not a BilayerStateNode")
        return self._encode_bilayer_node(node, timepoint=timepoint)

    def _encode_bilayer_flux_node(self, node, timepoint=None):
        if not isinstance(node, BilayerFluxNode):
            raise Exception("Node is not a BilayerFluxNode")
        return self._encode_bilayer_node(node, timepoint=timepoint)

    def _encode_bilayer_edge(self, edge, timepoint=None):
        if not isinstance(edge, BilayerEdge):
            raise Exception("Edge is not a BilayerEdge")
        return edge._get_label()

    def _observable_defn(self, measurements, obs, t):
        # flux * incoming1 * incoming2 ...
        obs_in_edges = measurements.node_incoming_edges[obs]
        result = Real(0.0)
        for src in obs_in_edges:
            # src is a flux
            f_t = self._encode_bilayer_flux_node(src, t)
            src_srcs = [
                self._encode_bilayer_edge(s, t)
                for s in measurements.node_incoming_edges[src]
            ]
            result = Plus(result, Times([f_t] + src_srcs)).simplify()
        # flux = next([measurements._output_edges])
        return result

    def _set_parameters_constant(self, parameters, formula):
        params = {
            parameter: Symbol(parameter, REAL) for parameter in parameters
        }
        # print(formula)
        symbols = self._symbols(formula)
        all_equal = And(
            [
                And([Equals(params[p], s) for t, s in symbols[p].items()])
                for p in params
            ]
        )
        return all_equal

    def _split_symbol(self, symbol):
        if symbol.symbol_name() in self._untimed_symbols:
            return symbol.symbol_name(), None
        else:
            s, t = symbol.symbol_name().rsplit("_", 1)
            if s not in self._timed_symbols or not t.isdigit():
                raise Exception(
                    f"Cannot determine if symbol {symbol} is timed."
                )
            return s, t

    def symbol_values(
        self, model_encoding: Encoding, pysmtModel: pysmt.solvers.solver.Model
    ) -> Dict[str, Dict[str, float]]:
        """
         Get the value assigned to each symbol in the pysmtModel.

        Parameters
        ----------
        model_encoding : Encoding
            encoding using the symbols
        pysmtModel : pysmt.solvers.solver.Model
            assignment to symbols

        Returns
        -------
        Dict[str, Dict[str, float]]
            mapping from symbol and timepoint to value
        """

        vars = model_encoding._symbols
        vals = {}
        for var in vars:
            vals[var] = {}
            for t in vars[var]:
                try:
                    symbol = vars[var][t]
                    vals[var][t] = float(pysmtModel.get_py_value(symbol))
                except OverflowError as e:
                    l.warning(e)
        return vals

    def parameter_values(
        self, model: Model, pysmtModel: pysmt.solvers.solver.Model
    ) -> Dict[str, List[Union[float, None]]]:
        """
        Gather values assigned to model parameters.

        Parameters
        ----------
        model : Model
            model encoded by self
        pysmtModel : pysmt.solvers.solver.Model
            the assignment to symbols

        Returns
        -------
        Dict[str, List[Union[float, None]]]
            mapping from parameter symbol name to value
        """
        try:
            parameters = {
                node.parameter: pysmtModel[node.parameter]
                for _, node in model.bilayer._flux.items()
            }
            return parameters
        except OverflowError as e:
            l.warning(e)
            return {}
