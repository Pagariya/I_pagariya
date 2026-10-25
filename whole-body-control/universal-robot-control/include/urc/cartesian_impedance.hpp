#pragma once

#include "urc/robot_model.hpp"
#include <Eigen/Dense>
#include <string>

namespace urc {

class CartesianImpedanceController {
public:
    CartesianImpedanceController(
        RobotModel& robot,
        const std::string& tool_frame = "tool0"
    );

    Eigen::VectorXd update(
        const Eigen::VectorXd& q,
        const Eigen::VectorXd& v,
        const Eigen::Vector3d& x_des,
        const Eigen::Vector3d& dx_des
    );

    void setGains(
        const Eigen::Vector3d& stiffness,
        const Eigen::Vector3d& damping
    );

private:
    RobotModel& robot_;
    std::string tool_frame_;

    Eigen::Vector3d kp_;
    Eigen::Vector3d kd_;
};

}