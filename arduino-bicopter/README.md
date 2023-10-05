# Generic Arduino Based Flightcontroller

## Code
There are two versions:

## MultiWii based FC code
(see https://github.com/multiwii/multiwii-firmware.git for more details). 

### Compass module
Some modifications of the original code were necessary for the compass module (QMC5883L) and are described here:
https://forum.arduino.cc/index.php?topic=556590.0

0.) Navigate to config.h add the line somewhere behind /* I2C magnetometer */:

        #define QMC5883
        
1.) Navigate to sensors.cpp add following somewhere behind the last #endif statement at the magnetometer section:

        // ************************************************************************************************************
        // I2C Compass QMC5883L
        // ************************************************************************************************************
        // I2C adress: 0x0D (7bit)
        // ************************************************************************************************************
        #if defined(QMC5883)

        #define MAG_ADDRESS 0x0D
        #define MAG_DATA_REGISTER 0x00

        //REG CONTROL

        #define MAG_CTRL_REG1 0x09
        #define QMC_MODE 0xC1 // 11 00 00 01OSR=64(11); Range=2G(00); ODR=10Hz(00); MODE=Cont(01)
        #define MAG_CTRL_REG2 0x0A

        void Mag_init() {
          i2c_writeReg(MAG_ADDRESS,0x0B,0x01);
          i2c_writeReg(MAG_ADDRESS,MAG_CTRL_REG1,QMC_MODE);
        }


        static void getADC() {
          i2c_getSixRawADC(MAG_ADDRESS,MAG_DATA_REGISTER);
          MAG_ORIENTATION( ((rawADC[1]<<8) | rawADC[0]) ,
                           ((rawADC[3]<<8) | rawADC[2]) ,
                           ((rawADC[5]<<8) | rawADC[4]) );
        }

        #if !defined(MPU6050_I2C_AUX_MASTER)
        static void Device_Mag_getADC() {
          getADC();
        }
        #endif
        #endif


Now we need to add the QMC to the MPU6050 I2C Master & Slave functionality:

Search for this comment in sensors.cpp:

        //The MAG acquisition function must be replaced because we now talk to the MPU device

Add following lines inside static void Device_Mag_getADC(){} after i2c_getSixRawADC(MPU6050_ADDRESS, 0x49);:


        #if defined(QMC5883)
                MAG_ORIENTATION( ((rawADC[1]<<8) | rawADC[0]) ,
                                 ((rawADC[3]<<8) | rawADC[2]) ,
                                 ((rawADC[5]<<8) | rawADC[4]) );
              #endif
              
Navigate to def.h search for the MAG 1 definition "#if" clause - add "|| defined(QMC5883)" - like this:

        #if defined(HMC5883) || defined(HMC5843) || defined(AK8975) || defined(MAG3110) || defined(QMC5883)
          #define MAG 1
        #else
          #define MAG 0
        #endif
              
The original HMC5883 Code has lots of more lines because of some ominous bias and gain settings - the QMC5883 lacks those registers - Unfortunately I don't have any knowledge about this and its benefits and no time to get into it. The data provided by the sensor seems to be reliable.

### Setup
Due to the construction of the flight controller the following settings were necessary:
            
          MINTHROTTLE = 1150
          # ==============================================
          # MPU Setup 
          # ==============================================
          # Roll and Yaw inverted
          #define ACC_ORIENTATION(X, Y, Z) {imu.accADC[ROLL] =  -X; imu.accADC[PITCH] =  -Y; imu.accADC[YAW] = Z;}
          #define GYRO_ORIENTATION(X, Y, Z) {imu.gyroADC[ROLL] = -X; imu.gyroADC[PITCH] = -Y; imu.gyroADC[YAW] = Z;}
          
          # ==============================================
          # Inverted Pitch ... let's see ===> Not a good idea ... Create oscillations!
          #define ACC_ORIENTATION(X, Y, Z) {imu.accADC[ROLL] =  X; imu.accADC[PITCH] =  Y; imu.accADC[YAW] = -Z;}
          #define GYRO_ORIENTATION(X, Y, Z) {imu.gyroADC[ROLL] = -X; imu.gyroADC[PITCH] = Y; imu.gyroADC[YAW] = -Z;}
          
          
          # ==============================================
          WORKING!!!!
          # Roll and Yaw inverted ==> Stabilize around roll axis! Roll appears inverted in MultiwiiConf!!!
          #define ACC_ORIENTATION(X, Y, Z) {imu.accADC[ROLL] =  X; imu.accADC[PITCH] =  -Y; imu.accADC[YAW] = -Z;}
          #define GYRO_ORIENTATION(X, Y, Z) {imu.gyroADC[ROLL] = -X; imu.gyroADC[PITCH] = -Y; imu.gyroADC[YAW] = -Z;}
          # PID Coeff; Roll; 4.1, 0.004,9 Pitch:1.6, 0.003,4 Yaw: 1.6, 0.003, 2
          
          # ==============================================
          # MPU + Compass
          # ==============================================
          WORKING!!!! Works perfectly with 
          #define YAW_DIRECTION -1
          #define ACC_ORIENTATION(X, Y, Z) {imu.accADC[ROLL] =  X; imu.accADC[PITCH] =  -Y; imu.accADC[YAW] = -Z;}
          #define GYRO_ORIENTATION(X, Y, Z) {imu.gyroADC[ROLL] = -X; imu.gyroADC[PITCH] = -Y; imu.gyroADC[YAW] = -Z;}
          #define FORCE_MAG_ORIENTATION(X, Y, Z)  {imu.magADC[ROLL]  =   -X; imu.magADC[PITCH]  =  -Y; imu.magADC[YAW]  = -Z;}

### ESC Calibration
Dont forget the ESC calibration in config.h!


### Custom Arduino based FC code
Inspired by http://www.electronoobs.com

## PCB
Created with Fritzing and Flatcam.

# Issues
Some issues encountered during the construction phase.

## Vibrations
Has a very intensive impact on PID controller resulting in twitches and an in general "nervous" behaviour of the quad. In order to mitigate there are three ways:

    1.) Reduce vibrations by accurately balancing propellers
    2.) Increase damping of the flight controller module
    3.) In MultiWii: Reduce low pass filter to e.g. 42hz for gyro and activate moving average filter (with default settings). Search for LPF in config.h