import time
import cv2
from robomaster import robot

def getKeyInput():
    k = cv2.waitKey(1) & 0xFF
    return chr(k).lower() if k != 255 else ''

if __name__ == '__main__':
    # Inicializa dron
    drn = robot.Drone()
    drn.initialize()

    # Configura cámara
    cam = drn.camera
    cam.start_video_stream(display=False)
    cam.set_fps("high")
    cam.set_resolution("high")
    cam.set_bitrate(6)

    # Obtiene tamaño de cuadro
    time.sleep(1)
    initFrame = cam.read_cv2_image()
    frameHeight, frameWidth, _ = initFrame.shape

    # Prepara video
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(
        "video_circular.mp4", codec, 20.0, (frameWidth, frameHeight)
    )

    # Despega
    flt = drn.flight
    print("Despegando...")
    flt.takeoff().wait_for_completed()
    time.sleep(2)

    print("Volando en círculo. Presiona 'q' para aterrizar.")

    # Graba vuelo circular
    while True:
        flt.rc(a=0, b=30, c=0, d=30)
        frm = cam.read_cv2_image()
        writer.write(frm)
        cv2.imshow("Vista del dron", frm)

        if getKeyInput() == 'q':
            print("Aterrizando...")
            break

        time.sleep(0.05)

    # Detiene movimiento
    flt.rc(a=0, b=0, c=0, d=0)
    time.sleep(1)

    # Aterriza
    flt.land().wait_for_completed()

    # Libera recursos
    writer.release()
    cam.stop_video_stream()
    cv2.destroyAllWindows()
    drn.close()
    print("Video guardado: 'video_circular.mp4'")
