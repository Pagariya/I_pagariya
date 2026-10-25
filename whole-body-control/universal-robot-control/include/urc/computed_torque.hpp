#pragma once
#include "urc/robot_model.hpp"
namespace urc {
// Fixed-base, fully actuated controller. Not directly valid for floating-base robots.
class ComputedTorqueController {
public:
  ComputedTorqueController(RobotModel& robot, Eigen::VectorXd kp, Eigen::VectorXd kd);
  Eigen::VectorXd update(const Eigen::VectorXd& q, const Eigen::VectorXd& v,
                         const Eigen::VectorXd& q_des, const Eigen::VectorXd& v_des,
                         const Eigen::VectorXd& a_des);
private:
  RobotModel& robot_;
  Eigen::VectorXd kp_, kd_;
};
}
