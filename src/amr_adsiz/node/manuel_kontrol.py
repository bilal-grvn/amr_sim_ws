#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import keyboard
import rospy

from geometry_msgs.msg import Twist

class keyboard_controller:
    def __init__(self) -> None:
        rospy.init_node('keyboard_kontrol_node',anonymous= True)

        self.pub_cmd_vel = rospy.Publisher('cmd_vel',Twist, queue_size=1)

        self.rate = rospy.Rate(40)

        self.hiz_verisi = Twist()

        self.hiz_x = 0.2
        self.hiz_wx = 0.2
        self.azami_x = 2.0
        self.azami_wx = 2.0
        self.asgari_x = 0.0
        self.asgari_wx = 0.0
    
    def loop(self):
        try:
            while(not rospy.is_shutdown()):
                # emir.emir = " "
                if keyboard.is_pressed("w"):    self.hiz_verisi.linear.x = self.hiz_x
                if keyboard.is_pressed("w+d"):    
                    self.hiz_verisi.linear.x = self.hiz_x   
                    self.hiz_verisi.angular.z = -self.hiz_wx
                if keyboard.is_pressed("w+a"):
                    self.hiz_verisi.linear.x = self.hiz_x   
                    self.hiz_verisi.angular.z = self.hiz_wx
                if keyboard.is_pressed("s"):    self.hiz_verisi.linear.x = -self.hiz_x
                if keyboard.is_pressed("s+a"):
                    self.hiz_verisi.linear.x = -self.hiz_x   
                    self.hiz_verisi.angular.z = -self.hiz_wx
                if keyboard.is_pressed("s+d"):    
                    self.hiz_verisi.linear.x = -self.hiz_x   
                    self.hiz_verisi.angular.z = self.hiz_wx
                if keyboard.is_pressed("d"):    self.hiz_verisi.angular.z = -self.hiz_wx
                if keyboard.is_pressed("a"):    self.hiz_verisi.angular.z = self.hiz_wx
                if keyboard.is_pressed("up"):    

                    if (self.hiz_x < self.azami_x):    self.hiz_x = self.hiz_x + 0.1
                    else:   self.hiz_x = self.azami_x
                    if (self.hiz_wx < self.azami_wx):    self.hiz_wx = self.hiz_wx + 0.1
                    else:   self.hiz_wx = self.azami_wx

                if keyboard.is_pressed("down"):
                    if (self.hiz_x > self.asgari_x):    self.hiz_x = self.hiz_x - 0.1
                    else:   self.hiz_x = self.asgari_x
                    if (self.hiz_x > self.asgari_wx):    self.hiz_wx = self.hiz_wx - 0.1
                    else:   self.hiz_wx = self.asgari_wx
                if keyboard.is_pressed("esc"):
                    self.hiz_verisi.linear.x = 0.0   
                    self.hiz_verisi.angular.z = 0.0    
                    self.pub_cmd_vel.publish(self.hiz_verisi)
                    print("durduruldu")
                    break



                rospy.loginfo(self.hiz_verisi)
                self.pub_cmd_vel.publish(self.hiz_verisi)

                self.hiz_verisi.linear.x = 0.0
                self.hiz_verisi.angular.z = 0.0

                self.rate.sleep()

        except KeyboardInterrupt:
            print("Kapatiliyor.")

if __name__ == "__main__":
    kumanda = keyboard_controller()
    kumanda.loop()

