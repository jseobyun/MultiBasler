from pypylon import pylon
def set_width(camera, value):
    cur_width = camera.Width.GetValue()
    camera.Width.SetValue(value)
    print(f"Camera width : {cur_width} -> {value}")

def set_height(camera, value):
    cur_height = camera.Width.GetValue()
    camera.Height.SetValue(value)
    print(f"Camera height : {cur_height} -> {value}")

def set_wh(camera, wh):
    cur_width = camera.Width.GetValue()
    cur_height = camera.Width.GetValue()
    camera.Width.SetValue(wh[0])
    camera.Height.SetValue(wh[1])
    print(f"Camera dimension : {(cur_width, cur_height)} -> {wh}")

def set_exposure_time(camera, time): # micro seconds
    cur_exp = camera.ExposureTime.GetValue()
    print(f"Exposure time : {cur_exp} -> {time}")
    camera.ExposureTime.SetValue(time)

def set_gain(camera, gain):
    cur_gain = camera.Gain.GetValue()
    #camera.Gain.SetValue(gain)
    print(f"Camera gain : {cur_gain} -> {gain}")
    print("gain is not saved. check this after debug")

def set_acqusition_fps(camera, fps):
    cur_fps = camera.AcquisitionFrameRate.GetValue()
    camera.AcquisitionFrameRateEnable.SetValue(True)
    #camera.AcquisitionFrameRate.SetValue(fps)
    print(f"Camera acquisition fps : {cur_fps} -> {fps}")
    print(f"Camera resulting fps : {camera.ResultingFrameRate.GetValue()}")
    print("fps is not saved. check this after debug")

def get_converter():
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    return converter
