# importing all the required modules
import boto
import boto.ec2.cloudwatch
import boto.ec2.autoscale
from boto.ec2.cloudwatch import MetricAlarm
from boto.ec2.elb import HealthCheck
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import ScalingPolicy

# setting connection variable conn
conn=boto.ec2.autoscale.connect_to_region("us-east-1",profile_name='selectcloud')

# setting launch configuration for creating AutoScaling Group
lc=LaunchConfiguration(name="new-asg",image_id='ami-04328208f4f0cf1fe',key_name='key',security_groups=[security_grpid-1,security-grpid-2],instance_type=’t2.micro’)

conn.create_launch_configuration(lc)

# create AutoScaling Group
ag=AutoScalingGroup(group_name='boto_group',load_balancers=['myelb1'],availability_zones=['us-east-1c','us-east-1b'],launch_config=lc,min_size=1,max_size=3,connection=conn,desired_capacity=1)

conn.create_auto_scaling_group(ag)

# setting the up and down scaling policy
scale_up_policy=ScalingPolicy(name='scale_up',adjustment_type='PercentChangeInCapacity',as_name='boto_group',scaling_adjustment=1,cooldown=180)
scale_down_policy=ScalingPolicy(name='scale_down', adjustment_type='PercentChangeInCapacity',as_name='boto_group',scaling_adjustment=-1, cooldown=180)

conn.create_scaling_policy(scale_down_policy)
conn.create_scaling_policy(scale_up_policy)

cloudwatch=boto.ec2.cloudwatch.connect_to_region('us-east-1',profile_name='selectcloud')
alarm_dimensions={"AutoScalingGroupName":"boto_group"}

# setting alarm in cloudwatch to trigger the autoscaling group
scale_down_alarm=MetricAlarm(name='scale_down_cpu',namespace='AWS/EC2',metric='CPUUtilization',statistic='Average',comparison='<',threshold='40',period='60', evaluation_periods=2,alarm_actions=[scale_down_policy_arn.policy_arn],dimensions=alarm_dimensions)

scale_up_alarm=MetricAlarm(name='scale_up_cpu', namespace='AWS/EC2',metric='CPUUtilization', statistic='Average',comparison='>', threshold='80',period='60', evaluation_periods=2,alarm_actions=[scale_up_policy_arn.policy_arn],dimensions=alarm_dimensions)

cloudwatch.create_alarm(scale_up_alarm)
cloudwatch.create_alarm(scale_down_alarm)