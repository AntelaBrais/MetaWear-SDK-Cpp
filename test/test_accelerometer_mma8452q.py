from common import TestMetaWearBase
from mbientlab.metawear.cbindings import *
from ctypes import create_string_buffer

class TestMma8452qConfiguration(TestMetaWearBase):
    def test_set_odr(self):
        expected= [0x03, 0x03, 0x00, 0x00, 0x20, 0x00, 0x00]

        self.libmetawear.mbl_mw_acc_mma8452q_set_odr(self.board, AccMma8452qOdr._50Hz)
        self.libmetawear.mbl_mw_acc_mma8452q_write_acceleration_config(self.board)
        self.assertListEqual(self.command, expected)

    def test_set_range(self):
        expected= [0x03, 0x03, 0x02, 0x00, 0x18, 0x00, 0x00]

        self.libmetawear.mbl_mw_acc_mma8452q_set_range(self.board, AccMma8452qRange._8G)
        self.libmetawear.mbl_mw_acc_mma8452q_write_acceleration_config(self.board)
        self.assertListEqual(self.command, expected)

    def test_set_odr_and_range(self):
        expected= [0x03, 0x03, 0x01, 0x00, 0x10, 0x00, 0x00]

        self.libmetawear.mbl_mw_acc_mma8452q_set_odr(self.board, AccMma8452qOdr._200Hz)
        self.libmetawear.mbl_mw_acc_mma8452q_set_range(self.board, AccMma8452qRange._4G)
        self.libmetawear.mbl_mw_acc_mma8452q_write_acceleration_config(self.board)
        self.assertListEqual(self.command, expected)

    def test_enable_acceleration_sampling(self):
        expected= [0x03, 0x02, 0x01]

        self.libmetawear.mbl_mw_acc_mma8452q_enable_acceleration_sampling(self.board)
        self.assertListEqual(self.command, expected)

    def test_disable_acceleration_sampling(self):
        expected= [0x03, 0x02, 0x00]

        self.libmetawear.mbl_mw_acc_mma8452q_disable_acceleration_sampling(self.board)
        self.assertListEqual(self.command, expected)

class TestAccMma8452qAccelerationData(TestMetaWearBase):
    def setUp(self):
        super().setUp()

        self.accel_data_signal= self.libmetawear.mbl_mw_acc_mma8452q_get_acceleration_data_signal(self.board)

    def test_get_acceleration_data_g(self):
        response= create_string_buffer(b'\x03\x04\x56\xfa\x05\xf6\x18\x03', 8)
        expected= CartesianFloat(x= -1.450, y= -2.555, z= 0.792)

        self.libmetawear.mbl_mw_datasignal_subscribe(self.accel_data_signal, self.sensor_data_handler)
        self.notify_mw_char(response)

        self.assertEqual(self.data_cartesian_float, expected)

    def test_handle_data_component(self):
        response= create_string_buffer(b'\x03\x04\x56\xfa\x05\xf6\x18\x03', 8)
        tests= [
            {
                'expected': -1.450,
                'index': Const.ACC_ACCEL_X_AXIS_INDEX,
                'name': 'x-axis'
            },
            {
                'expected': -2.555,
                'index': Const.ACC_ACCEL_Y_AXIS_INDEX,
                'name': 'y-axis'
            },
            {
                'expected': 0.792,
                'index': Const.ACC_ACCEL_Z_AXIS_INDEX,
                'name': 'z-axis'
            }
        ]

        for test in tests:
            with self.subTest(odr= test['name']):
                acc_component = self.libmetawear.mbl_mw_datasignal_get_component(self.accel_data_signal, test['index'])
                self.libmetawear.mbl_mw_datasignal_subscribe(acc_component, self.sensor_data_handler)
                self.notify_mw_char(response)
                
                self.assertAlmostEqual(self.data_float.value, test['expected'], delta = 0.001)

    def test_stream_acceleration_data(self):
        expected= [0x03, 0x04, 0x01]

        self.libmetawear.mbl_mw_datasignal_subscribe(self.accel_data_signal, self.sensor_data_handler)
        self.assertListEqual(self.command, expected)

    def test_end_stream_acceleration_data(self):
        expected= [0x03, 0x04, 0x00]

        self.libmetawear.mbl_mw_datasignal_unsubscribe(self.accel_data_signal)
        self.assertListEqual(self.command, expected)

class TestAccMma8452qHighFreqAccData(TestMetaWearBase):
    def setUp(self):
        super().setUp()

        self.accel_data_signal= self.libmetawear.mbl_mw_acc_mma8452q_get_packed_acceleration_data_signal(self.board)

    def sensorDataHandler(self, data):
        super().sensorDataHandler(data)

        self.cartesian_float_values.append(self.data_cartesian_float)

    def test_get_acceleration_data_g(self):
        response= create_string_buffer(b'\x03\x12\xdf\xed\x2b\x16\x15\xff\x7d\xfa\xed\x04\xc5\x0a\x31\xfb\xdb\xf8\x7b\xf2', 20)
        expected_values= [CartesianFloat(x= -4.641, y= 5.675, z= -0.235), CartesianFloat(x= -1.411, y= 1.261, z= 2.757), CartesianFloat(x= -1.231, y= -1.829, z= -3.461)]

        self.cartesian_float_values= []
        self.libmetawear.mbl_mw_datasignal_subscribe(self.accel_data_signal, self.sensor_data_handler)
        self.notify_mw_char(response)

        self.assertEqual(self.cartesian_float_values, expected_values)

    def test_stream_acceleration_data(self):
        expected= [0x03, 0x12, 0x01]

        self.libmetawear.mbl_mw_datasignal_subscribe(self.accel_data_signal, self.sensor_data_handler)
        self.assertListEqual(self.command, expected)

    def test_end_stream_acceleration_data(self):
        expected= [0x03, 0x12, 0x00]

        self.libmetawear.mbl_mw_datasignal_unsubscribe(self.accel_data_signal)
        self.assertListEqual(self.command, expected)

