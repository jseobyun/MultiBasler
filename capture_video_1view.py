import cv2
import numpy as np
import argparse
import time
from pypylon import pylon
from utils.cam_utils import *
from utils.dir_utils import *


'''
libpython3.7m.so.1.0 error solution:

export LD_LIBRARY_PATH=/home/user/anaconda3/envs/MultiBasler/lib
'''
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
    if not args.no_save:
        mkdir_safe(os.path.join(args.save_dir, args.exp_name))
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    set_wh(camera, (2560, 2048))
    set_exposure_time(camera, 5000)

    converter = get_converter()
    camera.StartGrabbing()

    counter = 0
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data.
            k = cv2.waitKey(1)
            if k == 27: # esc
                cv2.destroyWindow('Vis Window')
                break
            image = converter.Convert(grabResult)
            canvas = image.GetArray()
            counter +=1
            if not args.no_vis:
                cv2.imshow('Vis Window', cv2.resize(canvas, (1280, 1024)))

            if not args.no_save:
                save_path = os.path.join(args.save_dir, args.exp_name, f"{counter:05d}.png")
                cv2.imwrite(save_path, canvas)
                print(f"Image is saved at {save_path}")
            if args.sleep:
                intv = float(args.sleep)/1000 #ms
                camera.StopGrabbing()
                time.sleep(intv)
                camera.StartGrabbing()

        grabResult.Release()
    camera.Close()