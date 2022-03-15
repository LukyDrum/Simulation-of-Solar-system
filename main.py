import pygame
import stellar_objects
from help_tools import Vector2D, meters_to_pixels, pixels_to_meters
from user_interface import Info_Box, Terminal


def move_view():
    keys = pygame.key.get_pressed()
    move_speed = 2
    move_vector = Vector2D(0, 0)
    multiplier = (10 if keys[pygame.K_LSHIFT] else 1)
    if keys[pygame.K_UP]: move_vector.y += move_speed * multiplier * (1/system.zoom)
    if keys[pygame.K_DOWN]: move_vector.y -= move_speed * multiplier * (1/system.zoom)
    if keys[pygame.K_LEFT]: move_vector.x += move_speed * multiplier * (1/system.zoom)
    if keys[pygame.K_RIGHT]: move_vector.x -= move_speed * multiplier * (1/system.zoom)

    move_vector.update()

    if move_vector.magnitude != 0:
        obj: stellar_objects.Object
        for obj in system.objects.values():
            obj.real_position[0] += move_vector.x
            obj.real_position[1] += move_vector.y

            for pos in obj.real_history_pos:
                pos[0] += move_vector.x
                pos[1] += move_vector.y


def zoom():
    keys = pygame.key.get_pressed()
    zoom = 1
    max_zoom = 200
    if not terminal.active:
        multiplier = (10 if keys[pygame.K_LSHIFT] else 1)
        if keys[pygame.K_e] and system.zoom < max_zoom: zoom += 0.01 * multiplier
        if keys[pygame.K_q]: zoom -= 0.01 * multiplier

        system.zoom *= zoom

    obj: stellar_objects.Object
    for obj in system.objects.values():
        obj.relative_position[0] = system.zoom * (obj.real_position[0] - center[0]) + center[0]
        obj.relative_position[1] = system.zoom * (obj.real_position[1] - center[1]) + center[1]

        magnify_coeff = 150 * system.zoom / max_zoom
        obj.screen_radius = obj.radius # * magnify_coeff

        for i in range(len(obj.real_history_pos)):
            obj.relative_history_pos[i][0] = system.zoom * (obj.real_history_pos[i][0] - center[0]) + center[0]
            obj.relative_history_pos[i][1] = system.zoom * (obj.real_history_pos[i][1] - center[1]) + center[1]


def focus():
    if terminal.active:
        return
    
    focus_position = system.objects[system.focus].relative_position[:]
    off_set = [focus_position[0] - center[0], focus_position[1] - center[1]]

    obj: stellar_objects.Object
    for obj in system.objects.values():
        obj.relative_position = [obj.relative_position[0] - off_set[0], obj.relative_position[1] - off_set[1]]
        for i in range(len(obj.relative_history_pos)):
            obj.relative_history_pos[i] = [obj.relative_history_pos[i][0] - off_set[0], obj.relative_history_pos[i][1] - off_set[1]]
    


pygame.init()
width = 1400
height = 1000
screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)
center = [width/2, height/2]
pygame.display.set_caption("Star System Simulator")

# 1 pixel = 10**6 km = 10**9 m
# Creating all planets of Solar system + Sun
objects = [
    stellar_objects.Sun(center),
    stellar_objects.Mercury(position= [width/2 - 57.909, height/2], velocity= Vector2D(0, 47360)),
    stellar_objects.Venus(position= [width/2 - 108.21, height/2], velocity= Vector2D(0, 35020)),
    stellar_objects.Earth(position= [width/2 - 149.598, height/2], velocity= Vector2D(0, 29780)),
    stellar_objects.Moon(position= [width/2 -149.598 - 0.3844, height/2], velocity= Vector2D(0, 29780+1082)),
    stellar_objects.Mars(position= [width/2 - 227.956, height/2], velocity= Vector2D(0, 24070)),
    stellar_objects.Jupiter(position= [width/2 - 778.479, height/2], velocity= Vector2D(0, 13060)),
    stellar_objects.Saturn(position= [width/2 - 1432, height/2], velocity= Vector2D(0, 9680)),
    stellar_objects.Uranus(position= [width/2 - 2867, height/2], velocity= Vector2D(0, 6800)),
    stellar_objects.Neptune(position= [width/2 - 4515, height/2], velocity= Vector2D(0, 5430))
]

system = stellar_objects.System("Star system")
system.add(objects)

ui = Info_Box(screen)
terminal = Terminal(screen, [10, height-30])

object_selected = ""


running = True
while running:
    if system.simulation_speed != 0:
        ui.days += system.delta_time / 86_400
        pygame.time.delay(int(system.simulation_speed))
        system.simulate()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            # Check if planet was clicked on
            for object in system.objects.values():
                obj_pos = object.relative_position[:]
                off_set = object.screen_radius if object.screen_radius > 15 else 15
                if mouse_pos[1] > height - terminal.height:
                    break
                if  (obj_pos[0] - off_set) <= mouse_pos[0] <= (obj_pos[0] + off_set) and (obj_pos[1] - off_set) <= mouse_pos[1] <= (obj_pos[1] + off_set):
                    object_selected = object.name
                    break
                else:
                    object_selected = ""
            
            if system.placing_object:
                new_data = system.new_data
                new_object = stellar_objects.Object(new_data["Name"], new_data["Mass"], list(mouse_pos), new_data["Velocity"])
                system.add(new_object)
                system.placing_object = False
            
            # Check if terminal was clicked on
            elif mouse_pos[1] > height - terminal.height:
                terminal.active = True
            else:
                terminal.active = False

        # If terminal is active
        if terminal.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(terminal.text) > len("Terminal: "):
                        terminal.text = terminal.text[:-1]

                elif event.key == pygame.K_RETURN:
                    command = terminal.text.split(": ")[1]
                    terminal.text = "Terminal: "
                    system.execute_command(object_selected, command)
                    terminal.active = False
                else:
                    terminal.text += event.unicode

        # Enable / Disable focus on selected object
        if event.type == pygame.KEYDOWN and object_selected != "":
            if event.key == pygame.K_f:
                if system.focus == "":
                    system.focus = object_selected
                elif system.focus != "":
                    system.focus = ""
        


    screen.fill((0, 0, 0))

    # Moving view
    if system.focus == "":
        move_view()
    # Zoom in and out
    zoom()
    if system.focus != "":
        focus()

    # Ghost for placing object
    if system.placing_object:
        mouse_pos = pygame.mouse.get_pos()
        surf = pygame.Surface((50, 50))
        surf.set_alpha(100)
        pygame.draw.circle(surf, (255, 255, 255), (25, 25), 10)
        screen.blit(surf, (mouse_pos[0] - 25, mouse_pos[1] - 25))
    

    # Shows text
    ui.show_days()
    terminal.show_terminal()
    
    if object_selected in system.objects.keys():
        info = {
            "Name" : object_selected,
            "Mass" : str(round(system.objects[object_selected].mass, 3)) + " kg",
            "Velocity" : str(round(pixels_to_meters(system.objects[object_selected].velocity.magnitude), 4)) + " m/s"
        }
        ui.show_object_status(info)


    object: stellar_objects.Object
    for object in system.objects.values():
        # Draws paths of Objects of System on screen
        if system.duration_of_paths > 0:
            if system.simulation_speed != 0:
                # Add current position to history of positions
                if ui.days > system.duration_of_paths:
                    object.real_history_pos = object.real_history_pos[: system.duration_of_paths]
                object.real_history_pos.insert(0, object.real_position[:])
                object.relative_history_pos.insert(0, object.real_position[:])
            lenght = len(object.real_history_pos)-1
            for i in range(1, lenght):
                # Creates fading effect
                if i < 255:
                    shade = int(i) 
                else:
                    shade = 255
                pygame.draw.line(screen, (shade, shade, shade), object.relative_history_pos[lenght-i+1], object.relative_history_pos[lenght-i])

        # Draws Objects of System on screen
        pygame.draw.circle(screen, object.color, object.relative_position, object.screen_radius)

    pygame.display.update()


# END PROGRAM
pygame.quit()