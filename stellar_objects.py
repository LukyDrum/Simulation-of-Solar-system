from help_tools import *


class Object:
    def __init__(self, name: str, mass: int|float, position: list[float, float], velocity: Vector2D, screen_radius: float = 10, color: tuple() = (255, 255, 255) ) -> None:
        self.name = name
        self.mass = mass
        self.real_position = position[:]
        self.relative_position = position[:]
        self.velocity = Vector2D(meters_to_pixels(velocity.x), meters_to_pixels(velocity.y))
        self.radius = screen_radius
        self.screen_radius = screen_radius
        self.color = color

        self.real_history_pos = []
        self.relative_history_pos = []


class Sun(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D = Vector2D(0, 0)) -> None:
        super().__init__("Sun", 1.989e30, position, velocity, screen_radius= 25, color=(255, 0, 0))

class Mercury(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Mercury", 0.3301e24, position, velocity, screen_radius= 3, color=(130, 130, 130))

class Venus(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Venus", 4.8673e24, position, velocity, screen_radius= 9.49, color=(255, 102, 0))

class Earth(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Earth", 5.97e24, position, velocity, screen_radius= 10, color=(0, 0, 255))

class Moon(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Moon", 0.07346e24, position, velocity, screen_radius= 2.725, color=(130, 130, 130))

class Mars(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Mars", 0.64169e24, position, velocity, screen_radius= 5.32, color=(255, 0, 0))

class Jupiter(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Jupiter", 1898.13e24, position, velocity, screen_radius=20, color=(255, 140, 0))

class Saturn(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Saturn", 568e24, position, velocity, screen_radius=18, color=(255, 228, 181))

class Uranus(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Uranus", 86.811e24, position, velocity, screen_radius=14, color=(240, 248, 255))

class Neptune(Object):
    def __init__(self, position: list[float, float], velocity: Vector2D) -> None:
        super().__init__("Neptune", 102.409e24, position, velocity, screen_radius=14, color=(0, 0, 255))


class System:
    def __init__(self, name="System") -> None:
        self.name = name
        self.objects = dict()
        self.delta_time = 86_400 # seconds
        self.duration_of_paths = 300 # days
        self.simulation_speed = 30
        self.zoom = 1

        self.simulation_speed_before = self.simulation_speed
        self.placing_object = False
        self.focus = ""

    def add(self, to_add: Object|list[Object]):
        if isinstance(to_add, list):
            for obj in to_add:
                self.objects[obj.name] = obj
        else:
            self.objects[to_add.name] = to_add

    def __grav_force(self, object1: Object, object2: Object) -> float:
        """
        Calculates gravitational force between 2 objects using Newton's universal law of gravitation.
        [F] = [N]
        """
        G = 6.67408e-11
        distance = distance_of_two_points(object1.real_position, object2.real_position)
        grav_force = G * object1.mass * object2.mass / (distance * 10**9)**2
        return grav_force

    def simulate(self, step:float|int = 1):
        forces = dict()
        for key in self.objects:
            forces[key] = []

        # Calculates all gravitational forces on all obejcts in the system
        for key1, obj1 in self.objects.items():
            for key2, obj2 in self.objects.items():
                if key1 == key2:
                    continue
                
                force = vector_between_two_points(obj1.real_position, obj2.real_position)
                force.normalize()
                magnitude = self.__grav_force(obj1, obj2)
                force *= magnitude
                forces[key1].append(force)

        # Final gravitational force on each object in the system
        for key, item in forces.items():
            fin_force = Vector2D(0, 0)
            for force in item:
                fin_force += force
            forces[key] = fin_force
        

        for name, obj in self.objects.items():
            acceleration = meters_to_pixels(forces[name] / obj.mass)
            obj.velocity += acceleration * self.delta_time
            obj.real_position[0] += obj.velocity.x * self.delta_time
            obj.real_position[1] += obj.velocity.y * self.delta_time

    def execute_command(self, selected_object: str, command: str):
        if command.split(" ")[0] == "new":
            command = command.split(" ")[1:]
            name = str(command[0])
            mass = float(command[1])
            velocity = command[2].strip("()").split(",")
            velocity = Vector2D(float(velocity[0]), float(velocity[1]))
            self.new_data = {
                "Name" : name,
                "Mass" : mass,
                "Velocity" : velocity
            }
            self.placing_object = True

        elif command == "remove":
            self.objects.pop(selected_object)
        
        elif "mass" in command or "velocity" in command:
            if "=" in command: operation = "="
            elif "+" in command: operation = "+"
            elif "-" in command: operation = "-"
            elif "*" in command: operation = "*"
            elif "/" in command: operation = "/"

            command = command.split(operation)
            try:
                new = float(command[1])
                if "mass" in command[0]:
                    if operation == "=": self.objects[selected_object].mass = new
                    else:
                        eq = f"{self.objects[selected_object].mass} {operation} {new}"
                        new = eval(eq)
                        self.objects[selected_object].mass = new
                elif "velocity" in command[0]:
                    if operation == "=":
                        new = meters_to_pixels(new)
                    else:
                        eq = f"{self.objects[selected_object].velocity.magnitude} {operation} {new}"
                        new = eval(eq)
                    self.objects[selected_object].velocity.normalize()
                    self.objects[selected_object].velocity *= new
            except ValueError:
                print("Invalid command")

        elif "speed" in command:
            max = 50
            command = command.split("=")
            try:
                new = float(command[1])
                if new == 0:
                    self.simulation_speed_before = self.simulation_speed
                    self.simulation_speed = new
                elif new == 1:
                    self.simulation_speed = 1
                elif 0 < new < 1:
                    new =  max*(1 - new)
                    self.simulation_speed = new
                else:
                    print("Invalid command")
            except ValueError:
                if command[1] == "default":
                    self.simulation_speed = 30
                else:
                    print("Invalid command")

        elif command == "pause":
            self.simulation_speed_before = self.simulation_speed
            self.simulation_speed = 0
        elif command == "unpause" or command == "resume":
            self.simulation_speed =  self.simulation_speed_before
        
        elif "path_duration" in command:
            command = command.split("=")
            try:
                new = int(command[1])
                self.duration_of_paths = new
            except ValueError:
                print("Invalid command")
        
        else:
            print("Invalid command")