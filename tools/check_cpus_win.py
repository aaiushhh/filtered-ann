import ctypes
from ctypes import wintypes

class GROUP_AFFINITY(ctypes.Structure):
    _fields_ = [
        ("Mask", ctypes.c_size_t),
        ("Group", wintypes.WORD),
        ("Reserved", wintypes.WORD * 3),
    ]

class PROCESSOR_RELATIONSHIP(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.BYTE),
        ("EfficiencyClass", wintypes.BYTE),
        ("Reserved", wintypes.BYTE * 20),
        ("GroupCount", wintypes.WORD),
        ("GroupMask", GROUP_AFFINITY * 1),
    ]

class SYSTEM_LOGICAL_PROCESSOR_INFORMATION_EX(ctypes.Structure):
    _fields_ = [
        ("Relationship", wintypes.DWORD),
        ("Size", wintypes.DWORD),
        ("Processor", PROCESSOR_RELATIONSHIP),
    ]

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
GetLogicalProcessorInformationEx = kernel32.GetLogicalProcessorInformationEx
GetLogicalProcessorInformationEx.argtypes = [wintypes.DWORD, ctypes.c_void_p, ctypes.POINTER(wintypes.DWORD)]
GetLogicalProcessorInformationEx.restype = wintypes.BOOL

RelationProcessorCore = 0

buf_size = wintypes.DWORD(0)
GetLogicalProcessorInformationEx(RelationProcessorCore, None, ctypes.byref(buf_size))
buf = (ctypes.c_byte * buf_size.value)()
if not GetLogicalProcessorInformationEx(RelationProcessorCore, buf, ctypes.byref(buf_size)):
    raise ctypes.WinError(ctypes.get_last_error())

offset = 0
core_idx = 0
print(f"Total buffer size: {buf_size.value} bytes")
while offset < buf_size.value:
    info_ptr = ctypes.cast(ctypes.byref(buf, offset), ctypes.POINTER(SYSTEM_LOGICAL_PROCESSOR_INFORMATION_EX))
    info = info_ptr.contents
    if info.Relationship == RelationProcessorCore:
        mask = info.Processor.GroupMask[0].Mask
        eff = info.Processor.EfficiencyClass
        flags = info.Processor.Flags
        # List of logical processor IDs in this mask
        cpus = [b for b in range(64) if (mask & (1 << b))]
        core_type = "P-core" if eff > 0 else "E-core"
        print(f"Core {core_idx}: EfficiencyClass={eff} ({core_type}), Flags={flags}, Mask=0x{mask:X}, Logical CPUs={cpus}")
        core_idx += 1
    offset += info.Size
