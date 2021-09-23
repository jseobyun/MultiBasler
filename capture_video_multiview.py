import cv2
import numpy as np
import argparse
import time
from pypylon import pylon
from utils.cam_utils import *
from utils.dir_utils import *



def parse_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_name', default='default')
    parser.add_argument('--save_dir', default=os.getcwd())
    parser.add_argument('--no_vis', action='store_true', default=False)
    parser.add_argument('--no_save', action='store_true', default=False)
    parser.add_argument('--sleep', type=int)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_config()
    tlFactory = pylon.TlFactory.GetInstance()

    # Get all attached devices and exit application if no device is found.
    devices = tlFactory.EnumerateDevices()
    print(f"{len(devices)} devices are found")
    if len(devices) == 0:
        raise Exception("No camera present.")
    if not args.no_save:
        mkdir_safe(os.path.join(args.save_dir, args.exp_name))
        save_dirs = []
        for i in range(len(devices)):
            dir_path = os.path.join(args.save_dir, args.exp_name, f'view{i}')
            mkdir_safe(dir_path)
            save_dirs.append(dir_path)

    cameras = pylon.InstantCameraArray(len(devices))
    for i, camera in enumerate(cameras):
        camera.Attach(tlFactory.CreateDevice(devices[i]))
        camera.Open()
        camera.Width.SetValue(2560)
        camera.Height.SetValue(2048)

    cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    # Grab c_countOfImagesToGrab from the cameras.
    counter = 0
    while cameras.IsGrabbing():
        img_repos = []
        for i, camera in enumerate(cameras):
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                cameraContextValue = grabResult.GetCameraContext()


                image = converter.Convert(grabResult)
                canvas = image.GetArray()
                img_repos.append(canvas)

        if len(img_repos) != len(devices):
            continue
        else:
            if not args.no_vis:
                for i in range(len(devices)):
                    cv2.imshow(str(i), cv2.resize(img_repos[i], (1280, 1024)))

            if not args.no_save:
                for i in range(len(devices)):
                    save_path = os.path.join(save_dirs[i],f"{counter:05d}.png")
                    cv2.imwrite(save_path, img_repos[i])
                    print(f"View {i} Image is saved at {save_path}")
            if args.sleep:
                intv = float(args.sleep) / 1000  # ms
                cameras.StopGrabbing()
                time.sleep(intv)
                cameras.StartGrabbing()
        k = cv2.waitKey(1)
        if k == 27:  # esc
            for i in range(len(devices)):
                cv2.destroyWindow(str(i))
            cameras.Close()
            break
        counter +=1

