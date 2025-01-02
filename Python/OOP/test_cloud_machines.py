import pytest
from cloud_machines import Machine
import time


def test_cloud_machine_states():
    machine1 = Machine(Machine.MachineType.first_type)
    machine2 = Machine(Machine.MachineType.second_type)
    machine1.start_machine()
    machine2.start_machine()
    machine1.stop_machine()
    machine2.stop_machine()
    assert machine1.state == Machine.MachineState.DOWN
    assert machine2.state == Machine.MachineState.DOWN


def test_cloud_machine_prices():
    machine1 = Machine(Machine.MachineType.first_type)
    machine2 = Machine(Machine.MachineType.second_type)
    machine1.start_machine()
    machine2.start_machine()
    time.sleep(1)
    machine1.stop_machine()
    machine2.stop_machine()
    assert Machine.get_prices() >= 0
