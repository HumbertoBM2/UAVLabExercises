import robomaster
from robomaster import robot


if __name__ == '__main__':
    tl_drone = robot.Drone()
    tl_drone.initialize()

    tl_flight = tl_drone.flight

    # Get battery status
    tl_battery = tl_drone.battery
    battery_info = tl_battery.get_battery()
    print("Drone battery soc: {0}".format(battery_info))

    # Despegar
    tl_flight.takeoff().wait_for_completed()

    # Subir 50 cm
    tl_flight.up(distance=50).wait_for_completed()

    # Cuadrado 80 cm por lado
    for i in range(4):
        tl_flight.forward(distance=80).wait_for_completed()
        tl_flight.rotate(angle=90).wait_for_completed()

    # Bajar 50 cm
    tl_flight.down(distance=50).wait_for_completed()

    # Aterrizar
    tl_flight.land().wait_for_completed()
