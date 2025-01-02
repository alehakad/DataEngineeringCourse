from enum import Enum, auto
from datetime import datetime


class Machine:
    class MachineType(Enum):
        first_type = auto()
        second_type = auto()

    class MachineState(Enum):
        RUNNING = "up"
        DOWN = "down"

    pays_per_hour = {MachineType.first_type: 2, MachineType.second_type: 3}
    all_machines = {}

    @classmethod
    def get_prices(cls):
        total_costs = 0
        for machine in Machine.all_machines.values():
            total_costs += (
                machine.working_time * cls.pays_per_hour[machine.machine_type]
            )
        return total_costs

    def __init__(self, machine_type: MachineType):
        self.machine_type = machine_type
        self.working_time = 0
        self.total_cost = 0
        self.state = Machine.MachineState.DOWN
        self.start_working_time = None
        self.id = id(self)
        Machine.all_machines[self.id] = self

    def start_machine(self):
        self.state = Machine.MachineState.RUNNING
        print(f"Starting machine {self.id} at {datetime.now()}")
        self.start_working_time = datetime.now()

    def stop_machine(self):
        self.state = Machine.MachineState.DOWN
        self.working_time += (
            datetime.now() - self.start_working_time
        ).total_seconds() / 60
        self.total_cost += self.working_time * Machine.pays_per_hour[self.machine_type]
        self.start_working_time = None


if __name__ == "__main__":
    pass
