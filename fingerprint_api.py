# fingerprint_api.py
import ctypes

# Assuming the fingerprint library's filename is "ZKFingerprint.dll"
fingerprint_lib = ctypes.WinDLL(r'E:\Biometric\management\sdk\ZAZAPIt.dll')

# Type for device handle
HANDLE = ctypes.c_void_p

# Function prototypes
fingerprint_lib.ZAZOpenDeviceEx.argtypes = [ctypes.POINTER(HANDLE), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
fingerprint_lib.ZAZOpenDeviceEx.restype = ctypes.c_int

fingerprint_lib.ZAZCloseDeviceEx.argtypes = [HANDLE]
fingerprint_lib.ZAZCloseDeviceEx.restype = ctypes.c_int

fingerprint_lib.ZAZGetImage.argtypes = [HANDLE, ctypes.c_int]
fingerprint_lib.ZAZGetImage.restype = ctypes.c_int

fingerprint_lib.ZAZGenChar.argtypes = [HANDLE, ctypes.c_int, ctypes.c_int]
fingerprint_lib.ZAZGenChar.restype = ctypes.c_int

# Initialize the device
def open_device():
    handle = ctypes.c_void_p()
    nDeviceType = 0  # Assuming USB device
    iCom, iBaud, nPackageSize, iDevNum = 0, 0, 2, 0
    print(f"Opening device with parameters: DeviceType={nDeviceType}, Com={iCom}, Baud={iBaud}, PackageSize={nPackageSize}, DevNum={iDevNum}")
    result = fingerprint_lib.ZAZOpenDeviceEx(ctypes.byref(handle), nDeviceType, iCom, iBaud, nPackageSize, iDevNum)
    if result != 0:
        print(f"Failed to open device: {error_message}")
        raise Exception(f"Failed to open device, error code: {result}")
    return handle

# Capture fingerprint image
def capture_image(handle):
    result = fingerprint_lib.ZAZGetImage(handle, 0xffffffff)
    if result != 0:
        raise Exception(f"Failed to capture image, error code: {result}")
    print("Image captured successfully.")

# Generate fingerprint feature
def generate_feature(handle, buffer_id=0x01):
    result = fingerprint_lib.ZAZGenChar(handle, 0xffffffff, buffer_id)
    if result != 0:
        raise Exception(f"Failed to generate feature, error code: {result}")
    print(f"Feature code generated in buffer {buffer_id} successfully.")

# Close the device
def close_device(handle):
    result = fingerprint_lib.ZAZCloseDeviceEx(handle)
    if result != 0:
        raise Exception(f"Failed to close device, error code: {result}")
    print("Device closed successfully.")
