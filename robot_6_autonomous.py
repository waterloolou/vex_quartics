#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT6, 1.5, False)
right_drive_smart = Motor(Ports.PORT1, 1.5, True)
drivetrain_gyro = Gyro(Ports.PORT3)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_gyro, 200)
Intake_motor_a = Motor(Ports.PORT2, True)
Intake_motor_b = Motor(Ports.PORT5, False)
Intake = MotorGroup(Intake_motor_a, Intake_motor_b)
Tray_motor_a = Motor(Ports.PORT12, True)
Tray_motor_b = Motor(Ports.PORT7, False)
Tray = MotorGroup(Tray_motor_a, Tray_motor_b)
bumper_10 = Bumper(Ports.PORT10)
touchled_8 = Touchled(Ports.PORT8)
touchled_11 = Touchled(Ports.PORT11)



# Make random actually random
def setRandomSeedUsingAccel():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    urandom.seed(int(xaxis + yaxis + zaxis))
    
# Set random seed 
setRandomSeedUsingAccel()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Gyro
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Gyro")
    drivetrain_gyro.calibrate(GyroCalibrationType.NORMAL)
    while drivetrain_gyro.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      Full Volume VEXcode Project
# 	Author:       Quartics Team
# 	Created:      01/02/2024
# 	Description:  Autonomous Full volume game play code

'''
 predicted red blocks knocked down: 3

 predicted green blocks scored: 9 - 15

 predicted uniform bonus's: 3

 predicted park: partial

 predicted time: 45-1:00
'''





# ------------------------------------------

# Library imports
from vex import *

# Begin project code
# Method to rotate the robot in both clockwise (right turn) and anti-clockwise direction
# (left turn). This method is used instead of VEX library method as the VEX methods 
# rotation is not close to the rotation angle provided. 
# This method is using gyro sensor for rotation
# Input:  angle to rotate in Degrees. +ve value for left turn and -ve value for right turn
# This code supports turns of less than 180 Degrees
'''
def turn_robot(turn_angle_degrees):  
    print("\n++++++") 
    # reset gyro rotation    
    gyro_3.set_rotation(0, DEGREES)  
    left_drive_smart.set_max_torque(100, PERCENT)
    right_drive_smart.set_max_torque(100, PERCENT)
    left_drive_smart.set_velocity(50, PERCENT)  
    right_drive_smart.set_velocity(50, PERCENT)
    wait(20, MSEC)  

    # based on gyro sensor reading calculate how much the robot needs to turn
    error = turn_angle_degrees - gyro_3.rotation()        

    # stop rotation when error is within 1 Degree of the input value
    # this code was added as we saw that a high number of iterations were taken
    # when error was less than 1 and robot would appear to be not doing anything 
    while math.fabs(error) > 1:  
        print("\ngyro rotation: ", str(gyro_3.rotation()))  
        print("\nerror: ", str(error))  

        # for precise rotation reduce the velocity as the error starts to reduce
        # if the error is a low value velocity becomes very small and so checking
        # if the velocity is below a threshold value of 10. In that case set it to
        # the threshold
        velocity = math.fabs(error) * (50 / 180)
        print("\nvelocity: ", str(velocity))
        if velocity < 15:  
            velocity = 15 
            print("\nset velocity to: ", str(velocity))  
    
        # set velocity for both left and right motors to the calculated velocity
        left_drive_smart.set_velocity(velocity, PERCENT) 
        right_drive_smart.set_velocity(velocity, PERCENT) 

        # error is positive in case of left turn
        # in this case right motor should spin forward and left motor should spin reverse
        # error is negative in case of right turn
        # in this case left motor should spin forward and right motor should spin reverse
        if error > 0:  
            print("\nPositive")  
            left_drive_smart.spin(REVERSE)  
            right_drive_smart.spin(FORWARD)   
        else:  
            print("\nNegative")  
            left_drive_smart.spin(FORWARD)  
            right_drive_smart.spin(REVERSE)  
 
        wait(50, MSEC)  
        # re-calculate error to determine remaining rotation angle
        error = turn_angle_degrees - gyro_3.rotation()  

    print("\ngyro rotation: " + str(gyro_3.rotation()))  
    print("\nerror: " + str(error))   
    print("\ndone")
    # reset drive train velocities in case they were reduced earlier
    drivetrain.set_drive_velocity(25, PERCENT)
    drivetrain.set_turn_velocity(25, PERCENT)

    left_drive_smart.stop()
    right_drive_smart.stop()  

#this is our score function, the purpose of this function is
#so that when we want to score, the code will reverse until the bumper sensor
#is pressed. when the bumper sensor is pressed, the tray will raise up and come down
#hopefully scoring all the blocks in the tray
'''
def score():
    # if the bumper sensor is not pressed, this line of code will run
    if not bumper_10.pressing():
        # this while loop is so while the bumper is not pressed, the robot will reverse
        #until the bumper is pressing
        while not bumper_10.pressing():
            drivetrain.drive(REVERSE)
    #this line of code says that if the bumper sensor is pressed, the lift will move up the tray wait for the blocks 
    #and then put the tray down to get scored 
    if bumper_10.pressing():
        Tray.spin_for(FORWARD, 800, DEGREES)
        wait(1, SECONDS)
        Tray.spin_for(REVERSE, 800, DEGREES)
Intake.set_velocity(100,PERCENT)
drivetrain.set_drive_velocity(25,PERCENT)
drivetrain.set_turn_velocity(25,PERCENT)
# here we are setting identification colors so we know which sensor is what
touchled_8.set_color(Color.GREEN)
touchled_11.set_color(Color.BLUE)
#here we are letting the gyro callibrate, we use the gyro for our turning so this is very important
drivetrain_gyro.calibrate(GyroCalibrationType.NORMAL)
#here we are setting timeout. if the drivetrain stops for more than 3 secounds the code will move to the next line.
#drivetrain.set_timeout(3, SECONDS)
#here we are setting up the intake.
Intake.spin(FORWARD)
# this while loop stops the intake from getting jammed
#its saying that if the drivetrain velocity throughout the code becomes zero or stop's
# the intake will reverse, or try to get the block out, and then spin forward again to pick up the block
#we have just released
while Intake.velocity == 0:
    Intake.set_timeout(2, SECONDS)
    Intake.spin_for(REVERSE, 90, DEGREES)
    Intake.set_velocity(100,PERCENT)
drivetrain.set_heading(0, DEGREES)
brain_inertial.calibrate()


#start path part 1
#here we are setting our driving velocity. we want our driving to be accurate so we are setting velocity to 25%
drivetrain.set_drive_velocity(50, PERCENT)
drivetrain.set_turn_velocity(25, PERCENT)
drivetrain.drive_for(FORWARD, 900, MM)
drivetrain.turn_to_rotation(81 ,DEGREES)
wait(75, MSEC)
drivetrain.drive_for(FORWARD, 1524, MM)
wait(1,SECONDS)
drivetrain.turn_to_rotation(90,DEGREES)
wait(1,SECONDS)
drivetrain.drive_for(REVERSE, 266.7, MM)
wait(75, MSEC)
left_drive_smart.spin_for(REVERSE, 15, DEGREES)
wait(1,SECONDS)
drivetrain.drive_for(REVERSE, 241.3, MM)
wait(75, MSEC)
right_drive_smart.spin_for(REVERSE, 15, DEGREES)

#calls the score function
score()

#this peice of code says that after part 1, if the touchled_8 is not pressing, turn red
# the red signals to us that we have to pick up the robot and move it to a new destination
#when the touchled_8 is pressed,  the next line of code will start
while not touchled_8.pressing():
    touchled_8.set_color(Color.RED)
    print("touchled_8 not pressing")
    
#path pART 2
wait(75, MSEC)
drivetrain.drive_for(FORWARD, 965.2, MM)
wait(75, MSEC)
drivetrain.turn_to_rotation(-45, DEGREES)
wait(75, MSEC)
drivetrain.drive_for(FORWARD, 193.2, MM)
wait(75, MSEC)
drivetrain.drive_for(REVERSE, 193.2, MM)
wait(75, MSEC)
drivetrain.turn_to_rotation(45,DEGREES)
wait(75, MSEC)
drivetrain.drive_for(REVERSE, 635, MM)
wait(75, MSEC)
drivetrain.turn_to_rotation(-115,DEGREES)
wait(75, MSEC)
drivetrain.drive_for(FORWARD, 300, MM)
wait(75, MSEC)
drivetrain.turn_to_rotation(45,DEGREES)
wait(75, MSEC)
drivetrain.drive_for(REVERSE, 300, MM)
#calls the score function
score()

#this peice of code says that after part 1, if the touchled_10 is not pressing, turn red
# the red signals to us that we have to pick up the robot and move it to a new destination
#when the touchled_10 is pressed,  the next line of code will start
while not touchled_11.pressing():
    touchled_11.set_color(Color.RED)
    print("touchled_10 not pressing")

#path part 3
drivetrain.drive_for(FORWARD, 762, MM)
drivetrain.turn_to_rotation(-115,DEGREES)
drivetrain.drive_for(FORWARD, 381, MM)
wait(1,SECONDS)
drivetrain.turn_to_rotation(75,DEGREES)
wait(1,SECONDS)
drivetrain.drive_for(FORWARD, 127, MM)
wait(1,SECONDS)
drivetrain.turn_to_rotation(45,DEGREES)
wait(1,SECONDS)
drivetrain.drive_for(REVERSE, 381, MM)
wait(1,SECONDS)
#calls the score function
score()
wait(1,SECONDS)
#after this, we are just trying to speed up and get to partial park before the time is up
drivetrain.set_drive_velocity(100, PERCENT)
drivetrain.drive(FORWARD)
'''
total red blocks knocked down:

total green blocks scored:

total fill level bonus's:

total uniform bonus's: 

parking status: 

total time:

total points:

'''


