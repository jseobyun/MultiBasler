
import os
import cv2
import numpy as np
#os.environ["PYLON_CAMEMU"] = "1"

from pypylon import genicam
from pypylon import pylon
import sys

# Number of images to be grabbed.
countOfImagesToGrab = 10

# Limits the amount of cameras used for grabbing.
# It is important to manage the available bandwidth when grabbing with multiple cameras.
# This applies, for instance, if two GigE cameras are connected to the same network adapter via a switch.
# To manage the bandwidth, the GevSCPD interpacket delay parameter and the GevSCFTD transmission delay
# parameter can be set for each GigE camera device.
# The "Controlling Packet Transmission Timing with the Interpacket and Frame Transmission Delays on Basler GigE Vision Cameras"
# Application Notes (AW000649xx000)
# provide more information about this topic.
# The bandwidth used by a FireWire camera device can be limited by adjusting the packet size.
maxCamerasToUse = 3

# The exit code of the sample application.
exitCode = 0



# Get the transport layer factory.
tlFactory = pylon.TlFactory.GetInstance()

# Get all attached devices and exit application if no device is found.
devices = tlFactory.EnumerateDevices()
print(f"{len(devices)} devices are found")
if len(devices) == 0:
    raise pylon.RuntimeException("No camera present.")

# Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))

l = cameras.GetSize()

# Create and attach all Pylon Devices.
for i, cam in enumerate(cameras):
    cam.Attach(tlFactory.CreateDevice(devices[i]))
    cam.Open()
    cam.Width.SetValue(2590)
    cam.Height.SetValue(2048)
    print("Using device ", cam.GetDeviceInfo().GetModelName())
    print("Camera width", cam.Width.GetValue())
    print("Camera height", cam.Height.GetValue())

# Starts grabbing for all cameras starting with index 0. The grabbing
# is started for one camera after the other. That's why the images of all
# cameras are not taken at the same time.
# However, a hardware trigger setup can be used to cause all cameras to grab images synchronously.
# According to their default configuration, the cameras are
# set up for free-running continuous acquisition.
cameras.StartGrabbing()

converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
# Grab c_countOfImagesToGrab from the cameras.
while cameras.IsGrabbing():

    grabResult = cameras.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        # When the cameras in the array are created the camera context value
        # is set to the index of the camera in the array.
        # The camera context is a user settable value.
        # This value is attached to each grab result and can be used
        # to determine the camera that produced the grab result.
        cameraContextValue = grabResult.GetCameraContext()

        # Print the index and the model name of the camera.
        # print("Camera ", cameraContextValue, ": ", cameras[cameraContextValue].GetDeviceInfo().GetModelName())
        # print("GrabSucceeded: ", grabResult.GrabSucceeded())
        # print("SizeX: ", grabResult.GetWidth())
        # print("SizeY: ", grabResult.GetHeight())

        image = converter.Convert(grabResult)
        canvas = image.GetArray()
        # canvas = grabResult.GetArray()
        # canvas = np.array(canvas, dtype=np.uint8)
        print(np.shape(canvas))
        #img = grabResult.GetArray()
        cv2.imshow(f'{cameraContextValue}', canvas)
        cv2.waitKey(1)


# Comment the following two lines to disable waiting on exit.
sys.exit(exitCode)