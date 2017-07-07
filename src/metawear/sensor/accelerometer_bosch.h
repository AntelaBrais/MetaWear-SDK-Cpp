/**
 * @copyright MbientLab License 
 * @file accelerometer_bosch.h
 * @brief Interacts with the supported Bosch accelerometers, currenly BMI160 and BMA255
 * @details The BMI160 and BMA255 sensors are identical except for the output data rates.  Functions that are generic for 
 * both accelerometers have "bosch" in the name whereas functions specific to either accelerometer are contain their model 
 * i.e. "bmi160" or "bma255".
 */
#pragma once

#include "sensor_common.h"

#ifdef	__cplusplus
extern "C" {
#endif

const uint8_t MBL_MW_MODULE_ACC_TYPE_BMI160 = 1;            ///< Constant identifying the BMI160 accelerometer module type
const uint8_t MBL_MW_MODULE_ACC_TYPE_BMA255 = 3;            ///< Constant identifying the BMA255 accelerometer module type

/**
 * Available g-ranges on the Bosch accelerometers
 */
typedef enum {
    MBL_MW_ACC_BOSCH_RANGE_2G= 0,    ///< +/- 2g
    MBL_MW_ACC_BOSCH_RANGE_4G,       ///< +/- 4g
    MBL_MW_ACC_BOSCH_RANGE_8G,       ///< +/- 8g
    MBL_MW_ACC_BOSCH_RANGE_16G       ///< +/- 16g
} MblMwAccBoschRange;

/**
 * Available ouput data rates on the BMI160 accelerometer
 */
typedef enum {
    MBL_MW_ACC_BMI160_ODR_0_78125Hz= 0,
    MBL_MW_ACC_BMI160_ODR_1_5625Hz,
    MBL_MW_ACC_BMI160_ODR_3_125Hz,
    MBL_MW_ACC_BMI160_ODR_6_25Hz,
    MBL_MW_ACC_BMI160_ODR_12_5Hz,
    MBL_MW_ACC_BMI160_ODR_25Hz,
    MBL_MW_ACC_BMI160_ODR_50Hz,
    MBL_MW_ACC_BMI160_ODR_100Hz,
    MBL_MW_ACC_BMI160_ODR_200Hz,
    MBL_MW_ACC_BMI160_ODR_400Hz,
    MBL_MW_ACC_BMI160_ODR_800Hz,
    MBL_MW_ACC_BMI160_ODR_1600Hz
} MblMwAccBmi160Odr;

/**
 * Available ouput data rates on the BMA255 accelerometer
 */
typedef enum {
    MBL_MW_ACC_BMA255_ODR_15_62Hz= 0,
    MBL_MW_ACC_BMA255_ODR_31_26Hz,
    MBL_MW_ACC_BMA255_ODR_62_5Hz,
    MBL_MW_ACC_BMA255_ODR_125Hz,
    MBL_MW_ACC_BMA255_ODR_250Hz,
    MBL_MW_ACC_BMA255_ODR_500Hz,
    MBL_MW_ACC_BMA255_ODR_1000Hz,
    MBL_MW_ACC_BMA255_ODR_2000Hz
} MblMwAccBma255Odr;

/**
 * Operation modes for the step counter algorithm
 */
typedef enum {
    /** Recommended for most applications, well balanced between false positives and false negatives */
    MBL_MW_ACC_BMI160_STEP_COUNTER_MODE_NORMAL= 0,
    /** Recommended for light weighted persons, gives few false negatives but eventually more false positives */
    MBL_MW_ACC_BMI160_STEP_COUNTER_MODE_SENSITIVE,
    /** Gives few false positives but eventually more false negatives */
    MBL_MW_ACC_BMI160_STEP_COUNTER_MODE_ROBUST
} MblMwAccBmi160StepCounterMode;

/**
 * Retrieves the data signal representing acceleration data from a Bosch accelerometer
 * @param board     Pointer to the board to retrieve the signal from
 * @return Pointer to the board's BMI160 acceleration data signal
 */
METAWEAR_API MblMwDataSignal* mbl_mw_acc_bosch_get_acceleration_data_signal(const MblMwMetaWearBoard* board);
/**
 * @deprecated As of v0.8.0 and will be removed in v1.0.0.  Use mbl_mw_acc_bosch_get_packed_acceleration_data_signal instead.
 */
METAWEAR_API MblMwDataSignal* mbl_mw_acc_bosch_get_high_freq_acceleration_data_signal(const MblMwMetaWearBoard* board);
/**
 * Variant of acceleration data that packs multiple data samples into 1 BLE packet to increase the
 * data throughput.  This data signal cannot be used with data processing or logging, only with streaming.
 * @return Pointer to the data singal
 */
METAWEAR_API MblMwDataSignal* mbl_mw_acc_bosch_get_packed_acceleration_data_signal(const MblMwMetaWearBoard *board);
/**
 * Retrieves the data signal representing data from the BMI160 step counter
 * @param board     Pointer to the board to retrieve the signal from
 * @return Pointer to the board's BMI160 step counter data signal
 */
METAWEAR_API MblMwDataSignal* mbl_mw_acc_bmi160_get_step_counter_data_signal(const MblMwMetaWearBoard* board);
/**
 * Retrieves the data signal representing data from the BMI160 step detector
 * @param board     Pointer to the board to retrieve the signal from
 * @return Pointer to the board's BMI160 step detector data signal
 */
METAWEAR_API MblMwDataSignal* mbl_mw_acc_bmi160_get_step_detector_data_signal(const MblMwMetaWearBoard* board);

/**
 * Sets the output data rate for the BMI160 accelerometer
 * @param board     Pointer to the board to modify
 * @param odr       Output data rate value to assign
 */
METAWEAR_API void mbl_mw_acc_bmi160_set_odr(MblMwMetaWearBoard *board, MblMwAccBmi160Odr odr);
/**
 * Sets the output data rate for the BMA255 accelerometer
 * @param board     Pointer to the board to modify
 * @param odr       Output data rate value to assign
 */
METAWEAR_API void mbl_mw_acc_bma255_set_odr(MblMwMetaWearBoard *board, MblMwAccBma255Odr odr);
/**
 * Sets the acceleration range
 * @param board     Pointer to the board to modify
 * @param range     Acceleration range to assign
 */
METAWEAR_API void mbl_mw_acc_bosch_set_range(MblMwMetaWearBoard *board, MblMwAccBoschRange range);
/**
 * Writes the acceleration settings to the sensor
 * @param board     Pointer to the board to send the command to
 */
METAWEAR_API void mbl_mw_acc_bosch_write_acceleration_config(const MblMwMetaWearBoard *board);

/**
 * Sets the operational mode of the step counter
 * @param board     Board to modify
 * @param mode      New operation mode
 */
METAWEAR_API void mbl_mw_acc_bmi160_set_step_counter_mode(MblMwMetaWearBoard* board, MblMwAccBmi160StepCounterMode mode);
/**
 * Enables the BMI160 step counter
 * @param board     Board to modify
 */
METAWEAR_API void mbl_mw_acc_bmi160_enable_step_counter(MblMwMetaWearBoard* board);
/**
 * Disables the BMI160 step counter
 * @param board     Board to modify
 */
METAWEAR_API void mbl_mw_acc_bmi160_disable_step_counter(MblMwMetaWearBoard* board);
/**
 * Writes the step counter configuration to the sensor
 * @param board     Board to write to
 */
METAWEAR_API void mbl_mw_acc_bmi160_write_step_counter_config(const MblMwMetaWearBoard* board);
/**
 * Resets the BMI160 step counter
 * @param board     Board to reset
 */
METAWEAR_API void mbl_mw_acc_bmi160_reset_step_counter(const MblMwMetaWearBoard* board);

/**
 * Enables the BMI160 step detector 
 * @param board     Pointer to the board to send the command to
 */
METAWEAR_API void mbl_mw_acc_bmi160_enable_step_detector(const MblMwMetaWearBoard *board);
/**
 * Disables the BMI160 step detector
 * @param board     Pointer to the board to send the command to
 */
METAWEAR_API void mbl_mw_acc_bmi160_disable_step_detector(const MblMwMetaWearBoard *board);

/**
 * Switches the accelerometer to active mode.  When in active mode, the accelerometer cannot be configured
 * @param board     Pointer to the board to send the command to
 */
METAWEAR_API void mbl_mw_acc_bosch_start(const MblMwMetaWearBoard *board);
/**
 * Switches the accelerometer to standby mode
 * @param board     Pointer to the board to send the command to
 */
METAWEAR_API void mbl_mw_acc_bosch_stop(const MblMwMetaWearBoard *board);

/**
 * Enables acceleration sampling
 * @param board     Pointer to the board to send the command to
 */
METAWEAR_API void mbl_mw_acc_bosch_enable_acceleration_sampling(const MblMwMetaWearBoard *board);
/**
 * Disables acceleration sampling
 * @param board     Pointer to the board to send the command to
 */
METAWEAR_API void mbl_mw_acc_bosch_disable_acceleration_sampling(const MblMwMetaWearBoard *board);

#ifdef	__cplusplus
}
#endif
