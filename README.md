<div align="center">

# UAV Lab Exercises

##### Code and practical exercises for UAV lab sessions using the DJI RoboMaster Tello Talent.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![opencv](https://img.shields.io/badge/opencv-3670A0?style=for-the-badge&logo=opencv)
![robomaster](https://img.shields.io/badge/DJI_RoboMaster-3670A0?style=for-the-badge&logo=robomaster-sdk&logoColor=ffdd54)
</div>


## Folder Structure

- **p1Drones**  
  - Scripts to verify drone connection.  
  - Basic flight command: hover for 5 seconds.

- **p2Drones**  
  - Scripts to perform geometric flight patterns:  
    - Square trajectory.  
    - Triangle trajectory.

- **p3Drones**  
  - Circular flight while recording onboard video.

- **p4Drones**  
  - Green color detection and tracking:  
    - The drone activates the camera, identifies green objects, and follows them in flight.

## Environment

An `environment.yml` file is included to create the required **Anaconda environment**, which contains all dependencies needed to run the scripts and upload them to the drone.

To create the environment, run:

```bash
conda env create -f environment.yml
conda activate tello-env
