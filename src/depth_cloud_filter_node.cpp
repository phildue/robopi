//
// Created by phil on 27.12.20.
//

#include <ros/time.h>
#include <sensor_msgs/PointCloud2.h>
#include <ros/publisher.h>
#include <ros/node_handle.h>
#include <tf/tf.h>
#include <pcl_ros/transforms.h>
class Filter{
public:
    Filter(std::shared_ptr<ros::NodeHandle> n,const tf::StampedTransform transform& transform):
    _n(n),
    _transform(transform)
    {
        _pub = n->advertise<sensor_msgs::PointCloud2>("/robopi/cam_stereo/depth_cloud_filter", 10);

    }
    void callback(sensor_msgs::PointCloud2::ConstPtr pcl)
    {
        sensor_msgs::PointCloud2::Ptr pclBody;
        sensor_msgs::PointCloud2::Ptr pclOut;
        pclOut->data.reserve(pcl->data.size());
        pclBody->data.reserve(pcl->data.size());

        pcl_ros::transformPointCloud(_transform.child_frame_id_, _transform, *pcl, *pclBody);

        for(int idx = 0; idx < pcl->data.size(); ++idx)
        {

            const auto pBody = pclBody->data[idx];
        }

    }

private:
    std::shared_ptr<ros::NodeHandle> _n;
    ros::Publisher _pub;
    const tf::StampedTransform _transform;
};


int main(int argc, char **argv)
{
    std::shared_ptr<ros::NodeHandle> n = std::make_shared<ros::NodeHandle>("~");

    ros::init(argc, argv, "depth_cloud_filter");
    ros::Rate loop_rate(n->param("/robopi/depth_cloud_filter/publish_rate",50));
    tf::Transformer listener;
    tf::StampedTransform transform;

    try {
        ros::Time now = ros::Time::now();
        listener.waitForTransform("/camera_left_optical", "/chassis",
                                  now, ros::Duration(3.0));
        listener.lookupTransform("/camera_left_optical", "/chassis",
                                 now, transform);

        Filter filter(n,transform);

        while (ros::ok())
        {
            ros::spinOnce();
            loop_rate.sleep();

        }
    }catch(const tf::TransformException& e)
    {
        std::cerr << e.what() << std::endl;
    }

}




