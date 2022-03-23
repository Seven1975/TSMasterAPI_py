#!/usr/bin/env python
# @Time   :2021/10/30 12:24
# @Author :SEVEN
# @File   :TSMater.py
# @Comment:use func with TSMaster.dll
# ------------------------------------------------
from ctypes import *
from enum import Enum
import copy


# Enum
class CHANNEL_INDEX(Enum):
    (
        CHN1, CHN2, CHN3, CHN4, CHN5, CHN6, CHN7, CHN8, CHN9, CHN10, CHN11, CHN12, CHN13, CHN14, CHN15, CHN16, CHN17,
        CHN18, CHN19, CHN20, CHN21, CHN22, CHN23, CHN24, CHN25, CHN26, CHN27, CHN28, CHN29, CHN30, CHN31, CHN32) = (
        c_int(0), c_int(1), c_int(2), c_int(3), c_int(4), c_int(5), c_int(6), c_int(7), c_int(8), c_int(9), c_int(10),
        c_int(11), c_int(12), c_int(13), c_int(14), c_int(15), c_int(16), c_int(17), c_int(18), c_int(19), c_int(20),
        c_int(21), c_int(22), c_int(23), c_int(24), c_int(25), c_int(26), c_int(27), c_int(28), c_int(29),
        c_int(30),
        c_int(31)
    )


class TLIB_TS_Device_Sub_Type(Enum):
    TS_UNKNOWN_DEVICE = c_int(0)
    TSCAN_PRO = c_int(1)
    TSCAN_Lite1 = c_int(2)
    TC1001 = c_int(3)
    TL1001 = c_int(4)
    TC1011 = c_int(5)
    TSInterface = c_int(6)
    TC1002 = c_int(7)
    TC1014 = c_int(8)
    TSCANFD2517 = c_int(9)
    TC1026 = c_int(10)


class TLIBBusToolDeviceType(Enum):
    BUS_UNKNOWN_TYPE = c_int(0)
    TS_TCP_DEVICE = c_int(1)
    XL_USB_DEVICE = c_int(2)
    TS_USB_DEVICE = c_int(3)
    PEAK_USB_DEVICE = c_int(4)
    KVASER_USB_DEVICE = c_int(5)
    RESERVED_DEVICE = c_int(6)
    ICS_USB_DEVICE = c_int(7)
    TS_TC1005_DEVICE = c_int(8)


class TLIBApplicationChannelType(Enum):
    APP_CAN = c_int(0)
    APP_LIN = c_int(1)


class READ_TX_RX_DEF(Enum):
    ONLY_RX_MESSAGES = False
    TX_RX_MESSAGES = True


class LIN_PROTOCOL(Enum):
    LIN_PROTOCOL_13 = c_int(0)
    LIN_PROTOCOL_20 = c_int(1)
    LIN_PROTOCOL_21 = c_int(2)
    LIN_PROTOCOL_J2602 = c_int(3)


class T_LIN_NODE_FUNCTION(Enum):
    T_MASTER_NODE = c_int(0)
    T_SLAVE_NODE = c_int(1)
    T_MONITOR_NODE = c_int(2)


class TLIBCANFDControllerType(Enum):
    lfdtCAN = c_int(0)
    lfdtISOCAN = c_int(1)
    lfdtNonISOCAN = c_int(2)


class TLIBCANFDControllerMode(Enum):
    lfdmNormal = c_int(0)
    lfdmACKOff = c_int(1)
    lfdmRestricted = c_int(2)

class TSupportedObjType(Enum):
        sotCAN = c_int(0)
        sotLIN = c_int(1)
        sotCANFD = c_int(2)
        sotRealtimeComment = c_int(3)
        sotUnknown = c_int(0xFFFFFFF)



AppName = "TSMasterCDemo".encode("utf8")
dll = WinDLL(r".\TSMaster.dll")

# Struct
class TLIBTSMapping(Structure):
    _pack_ = 1
    _fields_ = [("FAppName", c_char * 32),
                ("FAppChannelIndex", c_int32),
                ("FAppChannelType", c_int),
                ("FHWDeviceType", c_int),
                ("FHWIndex", c_int32),
                ("FHWChannelIndex", c_int32),
                ("FHWDeviceSubType", c_int32),
                ("FHWDeviceName", c_char * 32),
                ("FMappingDisabled", c_bool),
                ]


class TLIBCAN(Structure):
    _pack_ = 1
    _fields_ = [("FIdxChn", c_uint8),
                ("FProperties", c_uint8),
                ("FDLC", c_uint8),
                ("FReserved", c_uint8),
                ("FIdentifier", c_int32),
                ("FTimeUs", c_int64),
                ("FData", c_uint8 * 8),
                ]


class TLIBCANFD(Structure):
    _pack_ = 1
    _fields_ = [("FIdxChn", c_uint8),
                ("FProperties", c_uint8),  # 定义canfd数据类型  1:FD标准帧 5:FD扩展帧
                ("FDLC", c_uint8),
                ("FFDProperties", c_uint8),  # 0:普通can数据帧 1：canfd数据帧
                ("FIdentifier", c_int32),
                ("FTimeUs", c_ulonglong),
                ("FData", c_ubyte * 64),
                ]


class TLIBLIN(Structure):
    _pack_ = 1
    _fields_ = [("FIdxChn", c_uint8),
                ("FErrStatus", c_uint8),
                ("FProperties", c_uint8),
                ("FDLC", c_uint8),
                ("FIdentifier", c_int8),
                ("FChecksum", c_uint8),
                ("FStatus", c_uint8),
                ("FTimeUs", c_int64),
                ("FData", c_uint8 * 8),
                ]


class TLIBHWInfo(Structure):
    _pack_ = 1
    _fields_ = [("FDeviceType", c_int32),
                ("FDeviceIndex", c_int32),
                ("FVendorName", c_char * 32),
                ("FDeviceName", c_char * 32),
                ("FSerialString", c_char * 64),
                ]


# 释放
def finalize_lib_tsmaster():
    dll.finalize_lib_tsmaster()


#  TSMasterAPI必须先调用该初始化函数，才可进行后续操作
def initialize_lib_tsmaster(AppName: str):
    dll.initialize_lib_tsmaster(AppName)


# 设置can通道数
def tsapp_set_can_channel_count(count: c_int32):
    r = dll.tsapp_set_can_channel_count(count)
    return r


# 获取can通道数
def tsapp_get_can_channel_count(count: c_int32):
    r = dll.tsapp_get_can_channel_count(count)
    return r


# 设置lin通道数
def tsapp_set_lin_channel_count(count: c_int32):
    r = dll.tsapp_set_lin_channel_count(count)
    return r


# 获取lin通道数
def tsapp_get_lin_channel_count(count: c_int32):
    r = dll.tsapp_get_lin_channel_count(count)
    return r


# 按需创建通道映射
def tsapp_set_mapping(mapping:TLIBTSMapping):
    r = dll.tsapp_set_mapping(byref(mapping))
    return r

def tsapp_set_mapping_verbose(AppName: str, TLIBApplicationChannelType: c_uint8, CHANNEL_INDEX: CHANNEL_INDEX, HW_name: str,
                              BusToolDeviceType: c_int32, HW_Type: c_int32, AHardwareChannel: CHANNEL_INDEX,
                              AEnableMapping: c_bool):
    r = dll.tsapp_set_mapping_verbose(AppName, TLIBApplicationChannelType, CHANNEL_INDEX, HW_name, BusToolDeviceType,
                                      HW_Type, 0, AHardwareChannel, AEnableMapping)
    return r


# 删除硬件通道映射
def tsapp_del_mapping_verbose(AppName: str, TLIBApplicationChannelType: c_uint8, APP_Channel: CHANNEL_INDEX):
    r = dll.tsapp_del_mapping_verbose(AppName, TLIBApplicationChannelType, APP_Channel)
    return r


# 设置can通道参数 bps
def tsapp_configure_baudrate_can(APP_Channel: CHANNEL_INDEX, ABaudrateKbps: c_float, AListenOnly: c_bool,
                                 AInstallTermResistor120Ohm: c_bool):
    r = dll.tsapp_configure_baudrate_can(APP_Channel, c_float(ABaudrateKbps), AListenOnly, AInstallTermResistor120Ohm)
    return r


# 设置canfd通道波特率
def tsapp_configure_baudrate_canfd(AIdxChn: CHANNEL_INDEX, ABaudrateArbKbps: c_float, ABaudrateDataKbps: c_float,
                                   AControllerType: c_int16, AControllerMode: c_int16,
                                   AInstallTermResistor120Ohm: c_bool):
    r = dll.tsapp_configure_baudrate_canfd(AIdxChn, c_float(ABaudrateArbKbps), c_float(ABaudrateDataKbps),
                                           AControllerType, AControllerMode, AInstallTermResistor120Ohm)
    return r

#can brs 采样率设置
def tsapp_configure_can_regs(AIdxChn: CHANNEL_INDEX, ABaudrateKbps: float, ASEG1: int, ASEG2: int, APrescaler: int,
                             ASJ2: int, A120: bool):
    r = dll.tsapp_configure_can_regs(AIdxChn, c_float(ABaudrateKbps), c_int32(ASEG1),c_int32(ASEG2),
                                     c_int32(APrescaler), c_int32(ASJ2), A120)
    return r

# canfd brs 采样率设置
def tsapp_configure_canfd_regs(AIdxChn: CHANNEL_INDEX, AArbBaudrateKbps: float, AArbSEG1: int, AArbSEG2: int,
                               AArbPrescaler: int,
                               AArbSJ2: int, ADataBaudrateKbps: float, ADataSEG1: int, ADataSEG2: int,
                               ADataPrescaler: int,
                               ADataSJ2: int, AControllerType: TLIBCANFDControllerType,
                               AControllerMode: TLIBCANFDControllerMode,
                               AInstallTermResistor120Ohm: c_bool):
    r = dll.tsapp_configure_canfd_regs(AIdxChn, c_float(AArbBaudrateKbps), c_int32(AArbSEG1), c_int32(AArbSEG2),
                                     c_int32(AArbPrescaler), c_int32(AArbSJ2),
                                     c_float(ADataBaudrateKbps), c_int32(ADataSEG1),
                                     c_int32(ADataSEG2), c_int32(ADataPrescaler), c_int32(ADataSJ2), AControllerType,
                                     AControllerMode,
                                     AInstallTermResistor120Ohm)
    return r


# 设置lin通道波特率
def tsapp_configure_baudrate_lin(AIdxChn: CHANNEL_INDEX, ABaudrateKbps: int, LIN_PROTOCOL: LIN_PROTOCOL):
    r = dll.tsapp_configure_baudrate_lin(AIdxChn, c_float(ABaudrateKbps), LIN_PROTOCOL)
    return r


# 设置LIN模式
def tslin_set_node_funtiontype(AIdxChn: CHANNEL_INDEX, TLINNodeType: T_LIN_NODE_FUNCTION):
    r = dll.tslin_set_node_funtiontype(AIdxChn, TLINNodeType)
    return r


# 程序启动
def tsapp_connect():
    r = dll.tsapp_connect()
    return r


# 程序关闭
def tsapp_disconnect():
    r = dll.tsapp_disconnect()
    return r


def tsapp_add_application(AppName: str):
    r = tsapp_add_application(AppName)
    return r


def tsapp_del_application(AppName: str):
    r = tsapp_del_application(AppName)
    return r


# 以APeriodMS为周期循环发送can报文
def tsapp_add_cyclic_msg_can(Msg: TLIBCAN, APeriodMS: c_float):
    r = dll.tsapp_add_cyclic_msg_can(byref(Msg), c_float(APeriodMS))
    return r


# 删除循环发送can报文
def tsapp_del_cyclic_msg_can(Msg: TLIBCAN):
    r = dll.tsapp_delete_cyclic_msg_can(byref(Msg))
    return r


# 以APeriodMS为周期循环发送canfd报文
def tsapp_add_cyclic_msg_canfd(Msg: TLIBCANFD, APeriodMS: c_float):
    r = dll.tsapp_add_cyclic_msg_canfd(byref(Msg), c_float(APeriodMS))
    return r


# 删除循环发送canfd报文
def tsapp_del_cyclic_msg_canfd(Msg: TLIBCANFD):
    r = dll.tsapp_delete_cyclic_msg_canfd(byref(Msg))
    return r


# 删除所有循环发送报文
def tsapp_delete_cyclic_msgs():
    r = dll.tsapp_delete_cyclic_msgs()
    return r


# 是否使能总线数据统计
def tsapp_enable_bus_statistics(AEnable: c_bool):
    r = dll.tsapp_enable_bus_statistics(AEnable)
    return r


def tsapp_enumerate_hw_devices(ACount: c_int32):
    r = dll.tsapp_enumerate_hw_devices(byref(ACount))
    return r


def tsapp_get_hw_info_by_index(AIndex: int, PLIBHWInfo: TLIBHWInfo):
    r = dll.tsapp_get_hw_info_by_index(c_int32(AIndex), byref(PLIBHWInfo))
    return r


# 错误信息描述
def tsapp_get_error_description(ACode: c_int32):
    errorcode = POINTER(POINTER(c_char))()
    if ACode ==0:
        return "确定"
    else:
        r = dll.tsapp_get_error_description(c_int32(ACode), byref(errorcode))
        if r == 0:
            ADesc = string_at(errorcode).decode("utf-8")
            return ADesc
        else:
            return r


# 获取can每秒帧数，需要先使能总线统计
def tsapp_get_fps_can(AIdxChn: CHANNEL_INDEX, AIdentifier: c_int32, AFPS: c_int32):
    r = dll.tsapp_get_fps_can(AIdxChn, AIdentifier, byref(AFPS))
    return r


# 获取canfd每秒帧数，需要先使能总线统计
def tsapp_get_fps_canfd(AIdxChn: CHANNEL_INDEX, AIdentifier: c_int32, AFPS: c_int32):
    r = dll.tsapp_get_fps_canfd(AIdxChn, AIdentifier, byref(AFPS))
    return r


# 获取canfd每秒帧数，需要先使能总线统计
def tsapp_get_fps_lin(AIdxChn: CHANNEL_INDEX, AIdentifier: c_int32, AFPS: c_int32):
    r = dll.tsapp_get_fps_lin(AIdxChn, AIdentifier, byref(AFPS))
    return r


# 获取硬件映射信息
def tsapp_get_mapping(AMapping: TLIBTSMapping):
    r = dll.tsapp_get_mapping(byref(AMapping))
    return r


# 获取详细硬件映射信息
def tsapp_get_mapping_verbose(APPName: str, ApplicationChannelType: c_int32, AMapping: TLIBTSMapping):
    r = dll.tsapp_get_mapping_verbose(APPName, ApplicationChannelType, byref(AMapping))
    return r


# 获取时间戳
def tsapp_get_timestamp(ATimestamp: c_int32):
    r = dll.tsapp_get_timestamp(byref(ATimestamp))
    return r


# 获取极速模式是否开启
def tsapp_get_turbo_mode(AEnable: c_bool):
    r = dll.tsapp_get_turbo_mode(byref(AEnable))
    return r


# 是否开启极速模式
def tsapp_set_turbo_mode(AEnable: c_bool):
    r = dll.tsapp_set_turbo_mode(AEnable)
    return r


# 开启接受FIFO模式
def tsfifo_enable_receive_fifo():
    dll.tsfifo_enable_receive_fifo()


# 关闭接受FIFO模式
def tsfifo_disable_receive_fifo():
    dll.tsfifo_disable_receive_fifo()


# 关闭错误帧接受模式
def tsfifo_disable_receive_error_frames():
    dll.tsfifo_disable_receive_error_frames()


# 读取通道can缓冲帧数量
def tsfifo_read_can_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_can_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道can Tx数量
def tsfifo_read_can_tx_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_can_tx_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道can Rx数量
def tsfifo_read_can_rx_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_can_rx_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道canfd Tx数量
def tsfifo_read_canfd_tx_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_canfd_tx_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道canfd Rx数量
def tsfifo_read_canfd_rx_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_canfd_rx_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道fastlin缓冲帧数量
def tsfifo_read_fastlin_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_fastlin_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道fastlin Tx数量
def tsfifo_read_fastlin_tx_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_fastlin_tx_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道fastlin Rx数量
def tsfifo_read_fastlin_rx_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_fastlin_rx_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道lin缓冲帧数量
def tsfifo_read_lin_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_lin_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道lin Tx数量
def tsfifo_read_lin_tx_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_lin_tx_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 读取通道lin Rx数量
def tsfifo_read_lin_rx_buffer_frame_count(AIdxChn: CHANNEL_INDEX, ACount: c_int32):
    r = dll.tsfifo_read_lin_rx_buffer_frame_count(AIdxChn, byref(ACount))
    return r


# 清除 通道can_receive_buffers
def tsfifo_clear_can_receive_buffers(AIdxChn: CHANNEL_INDEX):
    r = dll.tsfifo_clear_can_receive_buffers(AIdxChn)
    return r


# 清除 通道canfd_receive_buffers
def tsfifo_clear_canfd_receive_buffers(AIdxChn: CHANNEL_INDEX):
    r = dll.tsfifo_clear_canfd_receive_buffers(AIdxChn)
    return r


# 清除 通道fastlin_receive_buffers
def tsfifo_clear_fastlin_receive_buffers(AIdxChn: CHANNEL_INDEX):
    r = dll.tsfifo_clear_fastlin_receive_buffers(AIdxChn)
    return r


# 清除 通道lin_receive_buffers
def tsfifo_clear_lin_receive_buffers(AIdxChn: CHANNEL_INDEX):
    r = dll.tsfifo_clear_lin_receive_buffers(AIdxChn)
    return r


PCANFD = POINTER(TLIBCANFD)
OnTx_RxFUNC_CANFD = WINFUNCTYPE(None, POINTER(c_int32), PCANFD)

PCAN = POINTER(TLIBCAN)
OnTx_RxFUNC_CAN = WINFUNCTYPE(None, POINTER(c_int32), PCAN)

PLIN = POINTER(TLIBLIN)
OnTx_RxFUNC_LIN = WINFUNCTYPE(None, POINTER(c_int32), PLIN)


# 注册canfd预发送事件
def tsapp_register_pretx_event_canfd(obj: c_int32, OnFUNC):
    r = dll.tsapp_register_pretx_event_canfd(byref(obj), OnFUNC)
    return r


# 注册can预发送事件
def tsapp_register_pretx_event_can(obj: c_int32, OnFUNC):
    r = dll.tsapp_register_pretx_event_can(byref(obj), OnFUNC)
    return r


# 注册lin预发送事件
def tsapp_register_pretx_event_lin(obj: c_int32, OnFUNC):
    r = dll.tsapp_register_pretx_event_lin(byref(obj), OnFUNC)
    return r


# 注册canfd发送—接收事件
def tsapp_register_event_canfd(obj: c_int32, OnFUNC):
    r = dll.tsapp_register_event_canfd(byref(obj), OnFUNC)
    return r


# 注册can发送—接收事件
def tsapp_register_event_can(obj: c_int32, OnFUNC):
    r = dll.tsapp_register_event_can(byref(obj), OnFUNC)
    return r


# 注册lin发送—接收事件
def tsapp_register_event_lin(obj: c_int32, OnFUNC):
    r = dll.tsapp_register_event_lin(byref(obj), OnFUNC)
    return r


# 注销canfd预发送事件
def tsapp_unregister_pretx_event_canfd(obj: c_int32, OnFUNC):
    r = dll.tsapp_unregister_pretx_event_canfd(byref(obj), OnFUNC)
    return r


# 注销can预发送事件
def tsapp_unregister_pretx_event_can(obj: c_int32, OnFUNC):
    r = dll.tsapp_unregister_pretx_event_can(byref(obj), OnFUNC)
    return r


# 注销lin预发送事件
def tsapp_unregister_pretx_event_lin(obj: c_int32, OnFUNC):
    r = dll.tsapp_unregister_pretx_event_lin(byref(obj), OnFUNC)
    return r


# 注销canfd发送—接收事件
def tsapp_unregister_event_canfd(obj: c_int32, OnFUNC):
    r = dll.tsapp_unregister_event_canfd(byref(obj), OnFUNC)
    return r


# 注销can发送—接收事件
def tsapp_unregister_event_can(obj: c_int32, OnFUNC):
    r = dll.tsapp_unregister_event_can(byref(obj), OnFUNC)
    return r


# 注销lin发送—接收事件
def tsapp_unregister_event_lin(obj: c_int32, OnFUNC):
    r = dll.tsapp_unregister_event_lin(byref(obj), OnFUNC)
    return r


# 注销canfd预发送事件
def tsapp_unregister_pretx_events_canfd(obj: c_int32):
    r = dll.tsapp_unregister_pretx_events_canfd(byref(obj))
    return r


# 注销can预发送事件
def tsapp_unregister_pretx_events_can(obj: c_int32):
    r = dll.tsapp_unregister_pretx_events_can(byref(obj))
    return r


# 注销lin预发送事件
def tsapp_unregister_pretx_events_lin(obj: int):
    r = dll.tsapp_unregister_pretx_events_lin(byref(obj))
    return r


# 注销canfd发送—接收事件
def tsapp_unregister_events_canfd(obj: c_int32):
    r = dll.tsapp_unregister_events_canfd(byref(obj))
    return r


# 注销can发送—接收事件
def tsapp_unregister_events_can(obj: int):
    r = dll.tsapp_unregister_events_can(byref(obj))
    return r


# 注销lin发送—接收事件
def tsapp_unregister_events_lin(obj: int):
    r = dll.tsapp_register_event_lin(byref(obj))
    return r


# 注销预发送事件
def tsapp_unregister_pretx_events_all():
    r = dll.tsapp_unregister_pretx_events_all()
    return r


# 注销发送—接收事件
def tsapp_unregister_events_all():
    r = dll.tsapp_unregister_events_all()
    return r


# 打开TsMaster窗口
def tsapp_show_tsmaster_window(AWindowName: str):
    r = dll.tsapp_show_tsmaster_window(AWindowName, False)
    return r


# 开始录制报文
def tsapp_start_logging(filename: str):
    r = dll.tsapp_start_logging(filename)
    return r


# 停止录制报文
def tsapp_stop_logging():
    r = dll.tsapp_stop_logging()
    return r


# 异步发送单帧can报文
def tsapp_transmit_can_async(Msg: TLIBCAN):
    r = dll.tsapp_transmit_can_async(byref(Msg))
    return r


# can fifo接收
def tsapp_receive_can_msgs(ACANBuffers: TLIBCAN, ACANBufferSize: c_uint, AChn: CHANNEL_INDEX,
                           ARxTx: READ_TX_RX_DEF):
    temp = copy.copy(c_uint32(ACANBufferSize))
    data = POINTER(TLIBCAN * len(ACANBuffers))((TLIBCAN * len(ACANBuffers))(*ACANBuffers))
    r = dll.tsfifo_receive_can_msgs(data, byref(temp), AChn, ARxTx)
    # for i in range(temp.value):
    #     print("data.contents[i].FIdentifier=",data.contents[i].FIdentifier)
    for i in range(len(data.contents)):
        ACANBuffers[i] = data.contents[i]
    return r, temp


# 发送头帧接收数据
def tsapp_transmit_header_and_receive_msg(AChn: CHANNEL_INDEX, ID: int, FDlc: c_uint8, receivedMsg: TLIBLIN,
                                          Timeout: c_int):
    r = dll.tsapp_transmit_header_and_receive_msg(AChn, ID, FDlc, byref(receivedMsg), c_int32(Timeout))
    return r


# 异步发送单帧canfd报文
def tsapp_transmit_canfd_async(Msg: TLIBCANFD):
    r = dll.tsapp_transmit_canfd_async(byref(Msg))
    return r


# canfd报文接收
def tsapp_receive_canfd_msgs(ACANFDBuffers: TLIBCANFD, ACANFDBufferSize: c_uint, AChn: CHANNEL_INDEX,
                             ARxTx: READ_TX_RX_DEF):
    temp = copy.copy(c_uint32(ACANFDBufferSize))
    data = POINTER(TLIBCANFD * len(ACANFDBuffers))((TLIBCANFD * len(ACANFDBuffers))(*ACANFDBuffers))
    r = dll.tsfifo_receive_canfd_msgs(data, byref(temp), AChn, ARxTx)
    for i in range(len(data.contents)):
        ACANFDBuffers[i] = data.contents[i]
    return r, temp


# 异步发送单帧lin报文
def tsapp_transmit_lin_async(Msg: TLIBLIN):
    r = dll.tsapp_transmit_lin_async(byref(Msg))
    return r


# lin报文接收
def tsapp_receive_lin_msgs(ALINBuffers: TLIBLIN, ALINBufferSize: c_int, AChn: CHANNEL_INDEX,
                           ARxTx: READ_TX_RX_DEF):
    temp = copy.copy(c_uint32(ALINBufferSize))
    data = POINTER(TLIBLIN * len(ALINBuffers))((TLIBLIN * len(ALINBuffers))(*ALINBuffers))
    r = dll.tsfifo_receive_lin_msgs(data, byref(temp), AChn, ARxTx)
    for i in range(len(data.contents)):
        ALINBuffers[i] = data.contents[i]
    return r, temp


def tsfifo_receive_fastlin_msgs(ALINBuffers: TLIBLIN, ALINBufferSize: c_int, AChn: CHANNEL_INDEX,
                                ARxTx: READ_TX_RX_DEF):
    temp = copy.copy(c_uint32(ALINBufferSize))
    data = POINTER(TLIBLIN * len(ALINBuffers))((TLIBLIN * len(ALINBuffers))(*ALINBuffers))
    r = dll.tsfifo_receive_fastlin_msgs(data, byref(temp), AChn, ARxTx)
    for i in range(len(data.contents)):
        ALINBuffers[i] = data.contents[i]
    return r, temp


# 同步发送单帧can报文
def tsapp_transmit_can_sync(Msg: TLIBCAN, ATimeoutMS: c_int32):
    r = dll.tsapp_transmit_can_sync(byref(Msg), c_int32(ATimeoutMS))
    return r


# 同步发送单帧canfd报文
def tsapp_transmit_canfd_sync(Msg: TLIBCANFD, ATimeoutMS: c_int32):
    r = dll.tsapp_transmit_canfd_sync(byref(Msg), c_int32(ATimeoutMS))
    return r


# 同步发送单帧lin报文
def tsapp_transmit_lin_sync(Msg: TLIBLIN, ATimeoutMS: c_int32):
    r = dll.tsapp_transmit_lin_sync(byref(Msg), c_int32(ATimeoutMS))
    return r


# 开启rbs
def tsapp_tscom_can_rbs_start():
    r = dll.tscom_can_rbs_start()
    return r


# 停止rbs
def tscom_can_rbs_stop():
    r = dll.tscom_can_rbs_stop()
    return r


# rbs是否开启
def tscom_can_rbs_is_running(AIsRunning: c_bool):
    r = dll.tscom_can_rbs_is_running(byref(AIsRunning))
    return r


# rbs配置
def tscom_can_rbs_configure(AAutoStart: c_bool, AAutoSendOnModification: c_bool, AActivateNodeSimulation: c_bool,
                            TLIBRBSInitValueOptions: c_int):
    r = dll.tscom_can_rbs_configure(AAutoStart, AAutoSendOnModification, AActivateNodeSimulation,
                                    TLIBRBSInitValueOptions)
    return r


# 获取can信号值
def tsdb_get_signal_value_can(ACAN: TLIBCAN, AMsgName: str, ASgnName: str, AValue: c_double):
    r = dll.tsdb_get_signal_value_can(byref(ACAN), AMsgName, ASgnName, byref(AValue))
    return r


# 获取canfd信号值
def tsdb_get_signal_value_canfd(ACANFD: TLIBCANFD, AMsgName: str, ASgnName: str, AValue: c_double):
    r = dll.tsdb_get_signal_value_canfd(byref(ACANFD), AMsgName, ASgnName, byref(AValue))
    return r


# 设置can信号值
def tsdb_set_signal_value_can(ACAN: TLIBCAN, AMsgName: str, ASgnName: str, AValue: c_double):
    r = dll.tsdb_set_signal_value_can(byref(ACAN), AMsgName.encode, ASgnName, AValue)
    return r


# 设置canfd信号值
def tsdb_set_signal_value_canfd(ACANFD: TLIBCANFD, AMsgName: str, ASgnName: str, AValue: c_double):
    r = dll.tsdb_set_signal_value_canfd(byref(ACANFD), AMsgName, ASgnName, AValue)
    return r


# 加载dbc并绑定通道 注意idDBC 必须是c_uint32类型
def tsdb_load_can_db(DBC_ADDRESS, ASupportedChannelsBased, idDBC: c_uint32):
    r = dll.tsdb_load_can_db(DBC_ADDRESS.encode("utf8"), ASupportedChannelsBased.encode("utf8"), byref(idDBC))
    return r


# 解绑所有dbc
def tsdb_unload_can_dbs():
    r = dll.tsdb_unload_can_dbs()
    return r


# 获取dbc数量
def tsdb_get_can_db_count(ACount: c_uint32):
    r = dll.tsdb_get_can_db_count(byref(ACount))
    return r


# 获取dbc AId
def tsdb_get_can_db_id(AIndex: c_int32, AId: c_uint32):
    r = dll.tsdb_get_can_db_id(AIndex, byref(AId))
    return r


# 获取dbc信息
def tsdb_get_can_db_info(ADatabaseId: c_int32, AType: c_int32, AIndex: c_int32, ASubIndex: c_int32):
    AValue = POINTER(POINTER(c_char))()
    r = dll.tsdb_get_can_db_info(ADatabaseId, c_int32(AType), c_int32(AIndex), c_uint32(ASubIndex), byref(AValue))
    AValue = string_at(AValue).decode("utf8")
    return r,AValue




# 添加在线回放配置
def tslog_add_online_replay_config(AFileName: str, AIndex: c_int32):
    r = dll.tslog_add_online_replay_config(AFileName.encode("utf8"), byref(AIndex))
    return r


# 设置在线回放配置
def tslog_set_online_replay_config(AIndex: c_int32, AName: str, AFileName: str, AAutoStart: c_bool,
                                   AIsRepetitiveMode: c_bool, AStartTimingMode: c_int32, AStartDelayTimeMs: c_int32,
                                   ASendTx: c_bool, ASendRx: c_bool, AMappings: c_char * 32):
    r = dll.tslog_set_online_replay_config(AIndex, AName, AFileName, AAutoStart, AIsRepetitiveMode, AStartTimingMode,
                                           AStartDelayTimeMs, ASendTx, ASendRx, AMappings)
    return r


# 获取在线回放文件数量
def tslog_get_online_replay_count(ACount: c_int32):
    r = dll.tslog_get_online_replay_count(byref(ACount))
    return r


# 获取在线回放配置
def tslog_get_online_replay_config(AIndex: c_int32, AName: str, AFileName: str, AAutoStart: c_bool,
                                   AIsRepetitiveMode: c_bool, AStartTimingMode: c_int32, AStartDelayTimeMs: c_int32,
                                   ASendTx: c_bool, ASendRx: c_bool, AMappings: c_char * 32):
    r = dll.tslog_get_online_replay_config(AIndex, byref(AName), byref(AFileName), byref(AAutoStart),
                                           byref(AIsRepetitiveMode), byref(AStartTimingMode), byref(AStartDelayTimeMs),
                                           byref(ASendTx), byref(ASendRx), byref(AMappings))
    return r


# 删除在线回放配置
def tslog_del_online_replay_config(AIndex: c_int32):
    r = dll.tslog_del_online_replay_config(AIndex)
    return r


# 删除所有在线回放配置
def tslog_del_online_replay_configs():
    r = dll.tslog_del_online_replay_configs()
    return r


# 开始在线回放
def tslog_start_online_replay(AInde: c_int32):
    r = dll.tslog_del_online_replay_configs(AInde)
    return r


# 所有文件开始回放
def tslog_start_online_replays():
    r = dll.tslog_start_online_replays()
    return r


# 暂停在线回放
def tslog_pause_online_replay(AInde: c_int32):
    r = dll.tslog_pause_online_replay(AInde)
    return r


# 所有文件暂停回放
def tslog_pause_online_replays():
    r = dll.tslog_pause_online_replays()
    return r


# 停止在线回放
def tslog_stop_online_replay(AInde: c_int32):
    r = dll.tslog_stop_online_replay(AInde)
    return r


# 所有文件停止回放
def tslog_stop_online_replays():
    r = dll.tslog_stop_online_replays()
    return r


# 获取在线回放状态
def tslog_get_online_replay_status(AIndex: c_int32, AStatus: c_int32, AProgressPercent100: c_float):
    r = dll.tslog_get_online_replay_status(AIndex, byref(AStatus), byref(AProgressPercent100))
    return r


# 开始读取blf
def tslog_blf_read_start(Pathfile: str, AHeadle: c_int32, ACount: c_int32):
    r = dll.tslog_blf_read_start(Pathfile.encode("utf8"), byref(AHeadle), byref(ACount))
    return r


def tslog_blf_read_object(AHandle: c_int32, AProgressedCnt: c_int32, AType: TSupportedObjType, ACAN: TLIBCAN,
                          ALIN: TLIBLIN, ACANFD: TLIBCANFD):
    r = dll.tslog_blf_read_object(AHandle, byref(AProgressedCnt), byref(AType), byref(ACAN), byref(ALIN), byref(ACANFD))
    return r

def tslog_blf_read_end(AHeadle: c_int64):
    r = dll.tslog_blf_read_end(AHeadle)
    return r


def tslog_blf_write_start(Pathfile: str, AHeadle: c_int32):
    r = dll.tslog_blf_write_start(Pathfile, byref(AHeadle))
    return r

def tslog_blf_write_can(AHeadle:c_int32,ACAN:TLIBCAN):
    r = dll.tslog_blf_write_can(AHeadle,byref(ACAN))
    return r

def tslog_blf_write_canfd(AHeadle:c_int32,ACANFD:TLIBCANFD):
    r = dll.tslog_blf_write_canfd(AHeadle,byref(ACANFD))
    return r

def tslog_blf_write_lin(AHeadle:c_int32,ALIN:TLIBLIN):
    r = dll.tslog_blf_write_lin(AHeadle,byref(ALIN))
    return r

def tslog_blf_write_end(AHeadle: c_int64):
    r = dll.tslog_blf_write_end(AHeadle)
    return r


# 诊断相关API

# 创建诊断服务
def tsdiag_can_create(udsHandle: c_int32, ChnIndex: CHANNEL_INDEX, ASupportFD: c_byte, AMaxdlc: c_byte, reqID: c_int32,
                      ARequestIDIsStd: c_bool,
                      resID: c_int32, resIsStd: c_bool, AFctID: c_int32, fctIsStd: c_bool):
    r = dll.tsdiag_can_create(byref(udsHandle), ChnIndex, c_byte(ASupportFD), c_byte(AMaxdlc), reqID,
                              c_bool(ARequestIDIsStd),resID,c_bool(resIsStd),AFctID,c_bool(fctIsStd))
    return r

def tsdiag_can_delete(pDiagModuleIndex: c_int32):
    r = tsdiag_can_delete(pDiagModuleIndex)
    return r


def tsdiag_can_delete_all():
    r = dll.tsdiag_can_delete_all()
    return r


def tstp_can_send_functional(pDiagModuleIndex: c_int32, AReqDataArray: bytearray, AReqDataSize: c_int32,
                             ATimeOutMs: c_int32):
    data = POINTER(c_ubyte * len(AReqDataArray))((c_ubyte * len(AReqDataArray))(*AReqDataArray))
    r = dll.tstp_can_send_functional(pDiagModuleIndex, data, AReqDataSize, c_int32(ATimeOutMs))
    return r


def tstp_can_send_request(pDiagModuleIndex: c_int32, AReqDataArray: bytearray, AReqDataSize: c_int32,
                          ATimeOutMs: c_int32):
    data = POINTER(c_ubyte * len(AReqDataArray))((c_ubyte * len(AReqDataArray))(*AReqDataArray))
    r = dll.tstp_can_send_request(pDiagModuleIndex, data, AReqDataSize, c_int32(ATimeOutMs))
    return r


def tstp_can_request_and_get_response(udsHandle: c_int32, dataIn: bytearray, ReqSize: c_int32, dataOut: bytearray,
                            resSize: c_int32, TimeOut: c_int32):

    r = dll.tstp_can_request_and_get_response(udsHandle, dataIn, ReqSize, dataOut,pointer(resSize),
                                          c_int32(TimeOut))

    return r

# AReqDataArray = [0x22,0xf1,0x90]
# size = c_int32(100)
# AResponseDataArray = []
# for i in range(100):
#     item = 0
#     AResponseDataArray.append(item)
# tstp_can_request_and_get_response_s(udsHandle,AReqDataArray,3,AResponseDataArray,size,100)
def tstp_can_request_and_get_response_s(pDiagModuleIndex: c_int64, AReqDataArray: bytearray, AReqDataSize: c_int32,
                                  AResponseDataArray: bytearray, AResponseDataSize: c_int32, ATimeOutMs: c_int32):
    AReqdata = POINTER(c_ubyte * len(AReqDataArray))((c_ubyte * len(AReqDataArray))(*AReqDataArray))
    AResdata = POINTER(c_ubyte * len(AResponseDataArray))((c_ubyte * len(AResponseDataArray))(*AResponseDataArray))
    r = dll.tstp_can_request_and_get_response(pDiagModuleIndex, AReqdata, AReqDataSize, AResdata, byref(AResponseDataSize),
                                          ATimeOutMs)
    if r == 0:
        for i in range(AResponseDataSize.value):
            AResponseDataArray[i] = AResdata.contents[i]
    return r

# 诊断服务

def tsdiag_can_session_control(pDiagModuleIndex: c_int32, ASubSession: c_byte, ATimeoutMs: c_int32):
    r = dll.tsdiag_can_session_control(pDiagModuleIndex, ASubSession, c_int32(ATimeoutMs))
    return r


def tsdiag_can_routine_control(pDiagModuleIndex: c_int32, ARoutineControlType: c_byte, ARoutintID: c_uint16,
                               ATimeoutMs: c_int32):
    r = dll.tsdiag_can_routine_control(pDiagModuleIndex, ARoutineControlType, ARoutintID, c_int32(ATimeoutMs))
    return r


def tsdiag_can_communication_control(pDiagModuleIndex: c_int32, AControlType: c_byte, ATimeoutMs: c_int32):
    r = dll.tsdiag_can_communication_control(pDiagModuleIndex, AControlType, c_int32(ATimeoutMs))
    return r


def tsdiag_can_security_access_request_seed(pDiagModuleIndex: c_int32, ALevel: c_int32, ARecSeed: bytearray,
                                            ARecSeedSize: c_int32, ATimeoutMs: c_int32):
    AReqdata = POINTER(c_ubyte * len(ARecSeed))((c_ubyte * len(ARecSeed))(*ARecSeed))
    r = dll.tsdiag_can_security_access_request_seed(pDiagModuleIndex, ALevel, AReqdata, byref(ARecSeedSize),
                                                    c_int32(ATimeoutMs))
    return r


def tsdiag_can_security_access_send_key(pDiagModuleIndex: c_int32, ALevel: c_int32, AKeyValue: bytearray,
                                        AKeySize: c_int32, ATimeoutMs: c_int32):
    AReqdata = POINTER(c_ubyte * len(AKeyValue))((c_ubyte * len(AKeyValue))(*AKeyValue))
    r = dll.tsdiag_can_security_access_send_key(pDiagModuleIndex, ALevel, AReqdata, AKeySize, c_int32(ATimeoutMs))
    return r


def tsdiag_can_request_download(pDiagModuleIndex: c_int32, AMemAddr: c_uint32, AMemSize: c_uint32, ATimeoutMs: c_int32):
    r = dll.tsdiag_can_request_download(pDiagModuleIndex, AMemAddr, AMemSize, c_int32(ATimeoutMs))
    return r


def tsdiag_can_request_upload(pDiagModuleIndex: c_int32, AMemAddr: c_uint32, AMemSize: c_uint32, ATimeoutMs: c_int32):
    r = dll.tsdiag_can_request_upload(pDiagModuleIndex, AMemAddr, AMemSize, c_int32(ATimeoutMs))
    return r


def tsdiag_can_transfer_data(pDiagModuleIndex: c_int32, ASourceDatas: bytearray, ADataSize: c_int32, AReqCase: c_int32,
                             ATimeoutMs: c_int32):
    AReqdata = POINTER(c_ubyte * len(ASourceDatas))((c_ubyte * len(ASourceDatas))(*ASourceDatas))
    r = dll.tsdiag_can_transfer_data(pDiagModuleIndex, AReqdata, ADataSize, AReqCase, c_int32(ATimeoutMs))


def tsdiag_can_request_transfer_exit(pDiagModuleIndex: c_int32, ATimeoutMs: c_int32):
    r = dll.tsdiag_can_request_transfer_exit(pDiagModuleIndex, c_int32(ATimeoutMs))
    return r


def tsdiag_can_write_data_by_identifier(pDiagModuleIndex: c_int32, ADataIdentifier: c_uint16, AWriteData: bytearray,
                                        AWriteDataSize: c_int32, ATimeOutMs: c_int32):
    AReqdata = POINTER(c_ubyte * len(AWriteData))((c_ubyte * len(AWriteData))(*AWriteData))
    r = dll.tsdiag_can_write_data_by_identifier(pDiagModuleIndex, ADataIdentifier, AReqdata, AWriteDataSize,
                                                c_int32(ATimeOutMs))
    return r


def tsdiag_can_read_data_by_identifier(pDiagModuleIndex: c_int32, ADataIdentifier: c_uint16, AReturnArray: bytearray,
                                       AReturnArraySize: c_int32, ATimeOutMs: c_int32):
    AReqdata = POINTER(c_ubyte * len(AReturnArray))((c_ubyte * len(AReturnArray))(*AReturnArray))
    r = dll.tsdiag_can_read_data_by_identifier(pDiagModuleIndex, ADataIdentifier, AReqdata, byref(AReturnArraySize),
                                               c_int32(ATimeOutMs))
    return r

#LIN诊断
def tstp_lin_master_request(AChnIdx: CHANNEL_INDEX, ANAD: c_int8, AData: bytearray, ADataNum: c_int,
                            ATimeoutMs: c_int32):
    AReqdata = POINTER(c_ubyte * len(AData))((c_ubyte * len(AData))(*AData))
    r = dll.tstp_lin_master_request(AChnIdx, ANAD,byref(AReqdata) , c_int32(ADataNum), c_int32(ATimeoutMs))
    return r

def tstp_lin_master_request_intervalms(AChnIdx:CHANNEL_INDEX,AData:c_int8):
    r = dll.tstp_lin_master_request_intervalms(AChnIdx,AData)
    return r

def tstp_lin_reset(AChnIdx:CHANNEL_INDEX):
    r = dll.tstp_lin_reset(AChnIdx)
    return r

def tstp_lin_slave_response_intervalms(AChnIdx:CHANNEL_INDEX,AData:c_int8):
    r = dll.tstp_lin_slave_response_intervalms(AChnIdx,AData)
    return r


def tsdiag_lin_read_data_by_identifier(AChnIdx: CHANNEL_INDEX, ANAD: c_int8, AId: c_ushort, AResNAD: c_byte,
                                       AResData: bytearray, AResDataNum: c_int32, ATimeoutMS: c_int32):
    Resdata = POINTER(c_ubyte * len(AResData))((c_ubyte * len(AResData))(*AResData))
    r = dll.tsdiag_lin_read_data_by_identifier(AChnIdx, c_int8(ANAD), c_ushort(AId), byref(AResNAD), Resdata,
                                               byref(AResDataNum), ATimeoutMS)
    return r


def tsdiag_lin_write_data_by_identifier(AChnIdx: CHANNEL_INDEX, ANAD: c_int8, AId: c_ushort, AReqData: bytearray,
                                        AReqDataNum: c_int32,
                                        AResNAD: c_byte, AResData: bytearray, AResDataNum: c_int32,
                                        ATimeoutMS: c_int32):
    Reqdata = POINTER(c_ubyte * len(AReqData))((c_ubyte * len(AReqData))(*AReqData))
    Resdata = POINTER(c_ubyte * len(AResData))((c_ubyte * len(AResData))(*AResData))

    r = dll.tsdiag_lin_write_data_by_identifier(AChnIdx, c_int8(ANAD), c_ushort(AId), Reqdata, c_int32(AReqDataNum),
                                                byref(AResNAD), Resdata, byref(AResDataNum), ATimeoutMS)
    return r

def tsdiag_lin_session_control(AChnIdx: CHANNEL_INDEX, ANAD: c_int8, ANewSession: c_byte, ATimeoutMS:c_int32):
    r = dll.tsdiag_lin_session_control(AChnIdx,c_int8(ANAD),c_byte(ANewSession),c_int32(ATimeoutMS))
    return r

def tsdiag_lin_fault_memory_read(AChnIdx: CHANNEL_INDEX, ANAD: c_int8, ANewSession: c_byte, ATimeoutMS:c_int32):
    r = dll.tsdiag_lin_fault_memory_read(AChnIdx,c_int8(ANAD),c_byte(ANewSession),c_int32(ATimeoutMS))
    return r

def tsdiag_lin_fault_memory_clear(AChnIdx: CHANNEL_INDEX, ANAD: c_int8, ANewSession: c_byte, ATimeoutMS:c_int32):
    r = dll.tsdiag_lin_fault_memory_clear(AChnIdx,c_int8(ANAD),c_byte(ANewSession),c_int32(ATimeoutMS))
    return r


# def uds_create_can(udsHandle: c_int32, channel: CHANNEL_INDEX, ASupportCANFD: bool, AMaxDLC: c_byte, reqID: c_int32,
#                    reqisExtended: bool, resID: c_int32, resisExtended: bool):
#     r = dll_uds.s_create_can_diag(byref(udsHandle), channel, ASupportCANFD, c_int8(AMaxDLC), c_int32(reqID),
#                                   reqisExtended, c_int32(resID), resisExtended)
#     return r
#
#
# def tx_diag_req_and_get_res(udsHandle: c_int32, dataIn: bytearray, ReqSize: c_int32, dataOut: bytearray,
#                             resSize: c_int32, TimeOut: c_int32):
#     AReqdata = POINTER(c_ubyte * len(dataIn))((c_ubyte * len(dataIn))(*dataIn))
#     AResdata = POINTER(c_ubyte * len(dataOut))((c_ubyte * len(dataOut))(*dataOut))
#     r = dll_uds.s_tx_diag_req_and_get_res(udsHandle, AReqdata, c_int32(ReqSize), AResdata, byref(resSize),
#                                           c_int32(TimeOut))
#     if r:
#         for i in range(len(dataOut)):
#             dataOut[i] = AResdata.contents[i]
#     return r
