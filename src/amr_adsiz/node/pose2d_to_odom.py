#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# import keyboard
import math
import rospy
import tf
import tf_conversions

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose2D, Point, Pose, Quaternion, Twist



class pose2odom:
    def __init__(self):
        rospy.init_node('pose2dToOdomNode', anonymous=False)
        self.odom_pub = rospy.Publisher("odom", Odometry, queue_size=1)
        rospy.Subscriber('pose2D', Pose2D, self.pose_oku_isle)
        rospy.Subscriber('odom_encoder', Odometry, self.odom_enc_oku_isle)

        self.odom_broadcaster   = tf.TransformBroadcaster()
        self.odom_enc_verisi    = Odometry()
        self.odom_verisi        = Odometry()
        self.eski_pose          = Pose2D()
        
        self.hareket_durum      = False

        self.odom_verisi.header.frame_id    = "odom"
        self.odom_verisi.child_frame_id     = "chassis_link"

        self.rate = rospy.Rate(10)

    def pose_oku_isle(self, konum_okunan):

        if self.hareket_durum == True:
            self.eski_pose = konum_okunan

        acilar_quat                     = tf_conversions.transformations.quaternion_from_euler(0, 0, self.eski_pose.theta)
        self.odom_verisi.header.stamp   = rospy.Time.now()
        self.odom_verisi.pose.pose      = Pose(Point(self.eski_pose.x, self.eski_pose.y, 0), Quaternion(*acilar_quat))

        self.odom_broadcaster.sendTransform((self.eski_pose.x, self.eski_pose.y, 0), acilar_quat, self.odom_verisi.header.stamp, "chassis_link", "odom")


    def odom_enc_oku_isle(self, konum_okunan):
        dtheta      = 0.0
        orientation = self.odom_enc_verisi.pose.pose.orientation
        orient_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        dtheta      = tf_conversions.transformations.euler_from_quaternion(orient_list)[2]

        orientation = konum_okunan.pose.pose.orientation
        orient_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        dtheta      = abs(dtheta - tf_conversions.transformations.euler_from_quaternion(orient_list)[2])

        dx      = self.odom_enc_verisi.pose.pose.position.x - konum_okunan.pose.pose.position.x
        dy      = self.odom_enc_verisi.pose.pose.position.y - konum_okunan.pose.pose.position.y

        dpos = math.sqrt(math.pow(dx,2)+ math.pow(dy,2))
        self.hareket_durum = (dpos > 0.001) or (dtheta > 0.001)
        
        self.odom_enc_verisi = konum_okunan 
        
        # rospy.loginfo(self.hareket_durum )
        if self.hareket_durum == True:
            rospy.loginfo("dpos hareket: " +  str((dpos > 0.001)))
            rospy.loginfo("dtheta hareket: " +  str((dtheta > 0.001)))

        self.odom_enc_verisi.pose.pose.position.x = konum_okunan.pose.pose.position.x
        self.odom_enc_verisi.pose.pose.position.y = konum_okunan.pose.pose.position.y

    def ana_kod(self):
        while not rospy.is_shutdown():
            self.odom_pub.publish(self.odom_verisi)
            # rospy.loginfo(self.odom_verisi)
            self.rate.sleep()

if __name__ == "__main__":

    try:
        poseTodom = pose2odom()
        poseTodom.ana_kod()
    except rospy.ROSInterruptException:
        pass
