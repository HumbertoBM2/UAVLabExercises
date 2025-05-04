import robomaster
from robomaster import robot
import time
import cv2
import numpy as np

if __name__ == '__main__':
    # Inicializa el dron y sus módulos
    drone = robot.Drone()
    drone.initialize()
    camera = drone.camera
    flightController = drone.flight

    # Inicia transmisión de video sin mostrar por defecto
    camera.start_video_stream(display=False)

    # Despega y espera estabilización
    flightController.takeoff().wait_for_completed()
    time.sleep(2)

    # Constantes PD para control de yaw y altura
    kpYaw = 0.4
    kdYaw = 0.2
    kpAltitude = 0.3
    kdAltitude = 0.1
    prevYawError = 0
    prevAltitudeError = 0

    # Umbrales HSV para detección de verde
    lowerGreenHSV = np.array([50, 100, 100])
    upperGreenHSV = np.array([70, 255, 255])

    try:
        while True:
            # Captura, redimensiona y convierte a HSV
            imageFrame = camera.read_cv2_image(strategy="newest", timeout=5)
            imageFrame = cv2.resize(imageFrame, (480, 360))
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

            # Máscara y extracción de contornos verdes
            mask = cv2.inRange(hsvFrame, lowerGreenHSV, upperGreenHSV)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Mayor contorno y su centro
                largestContour = max(contours, key=cv2.contourArea)
                x, y, width, height = cv2.boundingRect(largestContour)
                centerX, centerY = x + width // 2, y + height // 2

                # Cálculo PD para yaw
                yawError = centerX - 240
                yawDerivative = yawError - prevYawError
                yawSpeed = int(kpYaw * yawError + kdYaw * yawDerivative)
                yawSpeed = np.clip(yawSpeed, -90, 90)

                # Cálculo PD para altura
                altitudeError = 180 - centerY
                altitudeDerivative = altitudeError - prevAltitudeError
                verticalVelocity = int(kpAltitude * altitudeError + kdAltitude * altitudeDerivative)
                verticalVelocity = np.clip(verticalVelocity, -20, 20)

                # Envío de comandos al dron
                flightController.rc(0, 0, verticalVelocity, yawSpeed)

                # Actualiza errores previos
                prevYawError = yawError
                prevAltitudeError = altitudeError

                # Dibuja rectángulo y centro detectado
                cv2.rectangle(imageFrame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                cv2.circle(imageFrame, (centerX, centerY), 5, (255, 0, 0), -1)
                cv2.putText(imageFrame, "Verde detectado", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                # Detiene motors si no hay detección
                flightController.rc(0, 0, 0, 0)
                print("[INFO] No se detecta verde.")

            cv2.imshow("Camera", imageFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[INFO] Finalizando vuelo...")
                break

    except KeyboardInterrupt:
        print("[INFO] Interrupción recibida, aterrizando...")

    finally:
        # Aterriza y libera recursos
        flightController.land().wait_for_completed()
        camera.stop_video_stream()
        drone.close()
        cv2.destroyAllWindows()
