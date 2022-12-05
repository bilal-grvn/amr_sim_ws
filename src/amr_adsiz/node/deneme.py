#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import rospy

# from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import pygame

class keyboard_kontroller:
    def __init__(self) -> None:
        rospy.init_node('keyboard_kontrol_node',anonymous= True)

        self.yayin = rospy.Publisher('cmd_vel',Twist, queue_size=1)

        self.rate = rospy.Rate(40)

        self.hiz_verisi = Twist()        
        self.hiz_verisi.linear.x = self.hiz_verisi.angular.z = 0.0
        self.vx = 0.5
        self.wz = 0.5
        pygame.init()
        pass


    def ana_kod(self):
        try:
            while(not rospy.is_shutdown()):
                for event in pygame.event.get():
                    # if event.type == pygame.QUIT:
                    #     pygame.quit(); sys.exit()
                    #     main = False
                    print(event.type)
                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == ord('w'):
                    #         self.hiz_verisi.linear.x = self.vx
                    #     if event.key == ord('s'):
                    #         self.hiz_verisi.linear.x = -self.vx
                    #     if event.key == ord('a'):
                    #         if self.hiz_verisi.linear.x >= 0.0: self.hiz_verisi.angular.z = self.wz
                    #         else:                               self.hiz_verisi.angular.z = -self.wx
                    #     if event.key == ord('d'):
                    #         if self.hiz_verisi.linear.x >= 0.0: self.hiz_verisi.angular.z = -self.wz
                    #         else:                               self.hiz_verisi.angular.z = self.wx
                    #     if event.key == ord('up') and self.vx < 1.1:
                    #         self.vx += 0.1
                    #     if event.key == ord('down') and self.vx >= 0.0:
                    #         self.vx -= 0.1
                    #     if event.key == ord('left') and self.vx < 1.1:
                    #         self.wx += 0.1
                    #     if event.key == ord('right') and self.vx >= 0.0:
                    #         self.wx -= 0.1
                        
                    # if event.type == pygame.KEYUP:
                    #     if event.key == ord('w') or event.key == ord('s'):
                    #         self.hiz_verisi.linear.x = 0.0
                    #     if event.key == ord('a') or event.key == ord('d'):
                    #         self.hiz_verisi.angular.z = 0.0
                        # if event.key == ord('q'):
                        #     pygame.quit()
                        #     sys.exit()
                        #     main = False 


                    rospy.loginfo(self.hiz_verisi)
                    self.yayin.publish(self.hiz_verisi)

                    self.rate.sleep()

        except KeyboardInterrupt:
            print("Kapatiliyor.")

if __name__ == "__main__":
    kontrolcu = keyboard_kontroller()
    kontrolcu.ana_kod()
