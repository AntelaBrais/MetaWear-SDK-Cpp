import copy
from common import TestMetaWearBase
from ctypes import create_string_buffer
from mbientlab.metawear import GyroBmi160, CartesianFloat

class TestGyroBmi160Config(TestMetaWearBase):
    def test_mbl_mw_gyro_bmi160_set_odr(self):
        expected= [0x13, 0x3, 0x29, 0x0]

        self.libmetawear.mbl_mw_gyro_bmi160_set_odr(self.board, GyroBmi160.ODR_200HZ)
        self.libmetawear.mbl_mw_gyro_bmi160_write_config(self.board)
        self.assertListEqual(self.command, expected)

    def test_mbl_mw_gyro_bmi160_set_fsr(self):
        expected= [0x13, 0x03, 0x28, 0x03]

        self.libmetawear.mbl_mw_gyro_bmi160_set_range(self.board, GyroBmi160.FSR_250DPS)
        self.libmetawear.mbl_mw_gyro_bmi160_write_config(self.board)
        self.assertListEqual(self.command, expected)

    def test_mbl_mw_gyro_bmi160_set_all_config(self):
        expected= [0x13, 0x03, 0x27, 0x04]

        self.libmetawear.mbl_mw_gyro_bmi160_set_odr(self.board, GyroBmi160.ODR_50HZ)
        self.libmetawear.mbl_mw_gyro_bmi160_set_range(self.board, GyroBmi160.FSR_125DPS)
        self.libmetawear.mbl_mw_gyro_bmi160_write_config(self.board)
        self.assertListEqual(self.command, expected)

    def test_gyro_active(self):
        expected= [0x13, 0x01, 0x01]

        self.libmetawear.mbl_mw_gyro_bmi160_start(self.board)
        self.assertListEqual(self.command, expected)

    def test_gyro_standby(self):
        expected= [0x13, 0x01, 0x00]

        self.libmetawear.mbl_mw_gyro_bmi160_stop(self.board)
        self.assertListEqual(self.command, expected)

    def test_enable_rotation_sampling(self):
        expected= [0x13, 0x02, 0x01, 0x00]

        self.libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.board)
        self.assertListEqual(self.command, expected)

    def test_disable_rotation_sampling(self):
        expected= [0x13, 0x02, 0x00, 0x01]

        self.libmetawear.mbl_mw_gyro_bmi160_disable_rotation_sampling(self.board)
        self.assertListEqual(self.command, expected)

class TestGyroBmi160DataHandler(TestMetaWearBase):
    def setUp(self):
        super().setUp()

        self.gyro_rot_data_signal= self.libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.board)

    def test_subscribe_rotation_data(self):
        expected= [0x13, 0x05, 0x01]

        self.libmetawear.mbl_mw_datasignal_subscribe(self.gyro_rot_data_signal)
        self.assertListEqual(self.command, expected)

    def test_unsubscribe_rotation_data(self):
        expected= [0x13, 0x05, 0x00]

        self.libmetawear.mbl_mw_datasignal_unsubscribe(self.gyro_rot_data_signal)
        self.assertListEqual(self.command, expected)

    def test_rotation_data_handler(self):
        response= create_string_buffer(b'\x13\x05\x3e\x43\xff\x7f\x00\x80', 8)
        expected= CartesianFloat(x= 262.409, y= 499.497, z= -499.512)

        self.libmetawear.mbl_mw_datasignal_subscribe(self.gyro_rot_data_signal)
        self.libmetawear.mbl_mw_gyro_bmi160_set_range(self.board, GyroBmi160.FSR_500DPS)
        self.libmetawear.mbl_mw_metawearboard_handle_response(self.board, response.raw, len(response))

        self.assertEqual(self.data_cartesian_float, expected)