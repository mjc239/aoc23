import math
from dataclasses import dataclass
from abc import abstractmethod, ABC
from collections import deque


class Module(ABC):
    def __init__(self, connected):
        self.connected = connected
        super().__init__()

    @abstractmethod
    def process_pulse(self, pulse):
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        raise NotImplementedError()


@dataclass
class Pulse:
    pulse_type: str
    origin: Module
    destination: Module

    def __repr__(self):
        return f"{self.origin} -{self.pulse_type}-> {self.destination}"


class FlipFlop(Module):
    def __init__(self, name, connected):
        super().__init__(connected)
        self.name = name
        self.state = False

    def __repr__(self):
        return f"flipflop_{self.name}"

    def process_pulse(self, pulse):
        # Check that pulse is coming to this module
        assert pulse.destination == self.name

        # Do nothing if high pulse
        if pulse.pulse_type == "high":
            return []

        # If low pulse, send low/high pulse
        # and flip module state
        elif pulse.pulse_type == "low":
            pulses = [
                Pulse(
                    pulse_type="low" if self.state else "high",
                    origin=self.name,
                    destination=module,
                )
                for module in self.connected
            ]
            self.state = not self.state
            return pulses

    def reset(self):
        self.state = False


class Conjunction(Module):
    def __init__(self, name, connected):
        super().__init__(connected)
        self.name = name

        # Initially empty - needs to be
        # populated on initialization!
        self.states = {}

    def __repr__(self):
        return f"conj_{self.name}"

    def process_pulse(self, pulse):
        # Check that pulse is coming to this module
        assert pulse.destination == self.name

        # Update module memory
        origin = pulse.origin
        self.states[origin] = pulse.pulse_type

        # Sent pulse depends on memory of all inputs
        if all([pulse_type == "high" for pulse_type in self.states.values()]):
            out_pulse_type = "low"
        else:
            out_pulse_type = "high"

        # Send pulses to all connected modules
        return [
            Pulse(pulse_type=out_pulse_type, origin=self.name, destination=module)
            for module in self.connected
        ]

    def reset(self):
        self.states = {state: "low" for state in self.states}


class Broadcaster(Module):
    def __init__(self, name, connected):
        super().__init__(connected)
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    def process_pulse(self, pulse):
        # Broadcast pusle to all connected modules
        return [
            Pulse(pulse_type=pulse.pulse_type, origin=self.name, destination=module)
            for module in self.connected
        ]

    def reset(self):
        pass


class UntypedModule(Module):
    def __init__(self, name, connected):
        super().__init__(connected)
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    def process_pulse(self, pulse):
        # No pulses transmitted
        return []

    def reset(self):
        pass


def process_input(input_lines):
    modules = {}

    for line in input_lines:
        module_string, conn_string = line.split(" -> ")
        connected = conn_string.split(", ")
        # Flip-flops
        if module_string[0] == "%":
            name = module_string[1:]
            modules[name] = FlipFlop(name, connected)

        # Conjunctions
        elif module_string[0] == "&":
            name = module_string[1:]
            modules[name] = Conjunction(name, connected)

        # Broadcasters
        elif module_string == "broadcaster":
            modules["broadcaster"] = Broadcaster("broadcaster", connected)

        # Untyped
        else:
            modules[module_string] = UntypedModule(module_string, connected)

    # Check for any uninitialised modules
    # and in the meantime initialise the
    # states for Conjunction modules
    unfound_modules = {}
    for module_name, module in modules.items():
        for out in module.connected:
            if out not in modules:
                # Uninitialised module
                unfound_modules[out] = UntypedModule(out, [])

            elif isinstance(modules[out], Conjunction):
                # Conjunction module - add to state
                modules[out].states[module_name] = "low"

    return {**modules, **unfound_modules}


def reset_modules(modules):
    # Reset modules to their initial states
    for module_string in modules:
        modules[module_string].reset()


def send_n_pulses(modules, n, reset=True, print_pulses=False):
    # Hit the button n times, transmitting n low pulses
    # to the broadcaster module. Count the total number
    # of low and high pulses transmitted

    # Reset all modules if necessary
    if reset:
        reset_modules(modules)

    n_pulses = {"low": 0, "high": 0}
    for _ in range(n):
        # Use a double-ended queue to track the pulses
        pulses = deque()

        # Transmit pulse from button
        pulses.append(Pulse("low", "button", "broadcaster"))
        n_pulses["low"] += 1

        while len(pulses) > 0:
            # Take pulse from the front of the queue
            pulse = pulses.popleft()
            if print_pulses:
                print(pulse)

            # Process pulse and create new pulses
            # to add to end of priority queue
            module = modules[pulse.destination]
            out_pulses = module.process_pulse(pulse)
            for out_pulse in out_pulses:
                n_pulses[out_pulse.pulse_type] += 1
                pulses.append(out_pulse)

    return n_pulses


def binary_states(modules, names):
    ret = ""
    for name in names:
        mod = modules[name]
        ret += "1" if mod.state else "0"
    return ret
