#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import rospy

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class logitech_f107_kontroller:
    def __init__(self) -> None:
        rospy.init_node('logitech_kontrol_node',anonymous= True)

        rospy.Subscriber('joy', Joy, self.joy_callback)
        self.yayin = rospy.Publisher('cmd_vel',Twist, queue_size=1)

        self.rate = rospy.Rate(40)

        self.hiz_verisi = Twist()        
        self.hiz_verisi.linear.x = self.hiz_verisi.angular.z = 0.0

    def joy_callback(self, veri):
        self.hiz_verisi.linear.x = veri.axes[1]
        self.hiz_verisi.angular.z = veri.axes[3]

    def ana_kod(self):
        try:
            while(not rospy.is_shutdown()):
    
                rospy.loginfo(self.hiz_verisi)
                self.yayin.publish(self.hiz_verisi)

                self.rate.sleep()

        except KeyboardInterrupt:
            print("Kapatiliyor.")

if __name__ == "__main__":
    kontrolcu = logitech_f107_kontroller()
    kontrolcu.ana_kod()
