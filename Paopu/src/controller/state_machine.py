import types
import functools

from enum import Enum
from typing import NamedTuple, Union

from .exceptions import ConditionsNotMet, InvalidStartState

TRANSITION_ALLOWED_TYPES = (str, bool, int, Enum, list)

class StateMachine:
    def __init__(self):
        try:
            self.state
        except AttributeError:
            raise ValueError("Need to set a state instance variable")


class TransitionDetails(NamedTuple):
    name: str
    source: Union[list, bool, int, str]
    target: Union[bool, int, str]
    conditions: list
    on_error: Union[bool, int, str]


class transition:
    def __init__(self, source, target, conditions=[], on_error=None):
        self.check_types(source, target, conditions, on_error)
        self.source = source
        self.target = target
        self.conditions = conditions
        self.on_error = on_error

    def check_types(self, source, target, conditions, on_error):
        if not isinstance(source, list):
            source = [source]
        map(self.check, source)
        self.check(target)
        self.check(conditions, list)
        map(lambda x: self.check(x, types.FunctionType), source)
        if on_error:
            self.check(on_error, TRANSITION_ALLOWED_TYPES)

    def check(self, target, allowed_types=TRANSITION_ALLOWED_TYPES):
        if not isinstance(target, allowed_types):
            raise ValueError(f"Source can be {allowed_types}")

    def __call__(self, func):
        func._fsm = TransitionDetails(
            func.__name__,
            self.source,
            self.target,
            self.conditions,
            self.on_error,
        )

        @functools.wraps(func)
        def sync_callable(*args, **kwargs):
            state_machine = self.get_state_machine(*args)
            self.validate_source(state_machine, func.__name__)
            if not self.validate_conditions(*args, **kwargs):
                return (None, False)
            if not self.on_error:
                return (self.call(state_machine, func, *args, **kwargs), True)
            try:
                return (self.call(state_machine, func, *args, **kwargs), True)
            except Exception:
                state_machine.state = self.on_error
                return (None, False)

        return sync_callable

    def get_state_machine(self, *args):
        try:
            state_machine, _rest = args
        except ValueError:
            state_machine = args[0]
        return state_machine

    def validate_source(self, state_machine, current):
        if state_machine.state not in self.source:
            exception_message = (
                f"Current state is {state_machine.state}. "
                f"{current} allows transitions from {self.source}."
            )
            raise InvalidStartState(exception_message)

    def validate_conditions(self, *args, **kwargs):
        conditions_not_met = []
        for condition in self.conditions:
            if condition(*args, **kwargs) is not True:
                conditions_not_met.append(condition)
        if conditions_not_met:
            #raise ConditionsNotMet(conditions_not_met)
            return False
        return True

    def call(self, state_machine, func, *args, **kwargs):
        result = func(*args, **kwargs)
        state_machine.state = self.target
        return result