#include "urc/cartesian_impedance.hpp"
#include <stdexcept>

namespace urc {

CartesianImpedanceController::CartesianImpedanceController(
    RobotModel& robot,
    const std::string& tool_frame
)
    : robot_(robot),
      tool_frame_(tool_frame),
      kp_(Eigen::Vector3d::Constant(300.0)),
      kd_(Eigen::Vector3d::Constant(30.0))
{
}

void CartesianImpedanceController::setGains(
    const Eigen::Vector3d& stiffness,
    const Eigen::Vector3d& damping
)
{
    if (!stiffness.allFinite() || !damping.allFinite() ||
        (stiffness.array() < 0).any() ||
        (damping.array() < 0).any()) {
        throw std::invalid_argument("Invalid impedance gains");
    }

    kp_ = stiffness;
    kd_ = damping;
}

Eigen::VectorXd CartesianImpedanceController::update(
    const Eigen::VectorXd& q,
    const Eigen::VectorXd& v,
    const Eigen::Vector3d& x_des,
    const Eigen::Vector3d& dx_des
)
{
    if (q.size() != robot_.nq() ||
        v.size() != robot_.nv() ||
        !q.allFinite() || !v.allFinite() ||
        !x_des.allFinite() || !dx_des.allFinite()) {
        throw std::invalid_argument("Invalid controller input");
    }

    // 1. Current Cartesian position
    const Eigen::Vector3d x =
        robot_.framePosition(q, tool_frame_);

    // 2. Cartesian Jacobian (6 x nv)
    const Eigen::MatrixXd J =
        robot_.frameJacobian(q, tool_frame_);

    // Pinocchio: linear velocity is in the first 3 rows.
    const Eigen::MatrixXd Jv = J.topRows(3);

    // 3. Current Cartesian velocity
    const Eigen::Vector3d dx = Jv * v;

    // 4. Cartesian virtual spring-damper force
    const Eigen::Vector3d force =
        kp_.cwiseProduct(x_des - x) +
        kd_.cwiseProduct(dx_des - dx);

    // 5. Gravity compensation
    const Eigen::VectorXd zero_v =
        Eigen::VectorXd::Zero(robot_.nv());

    const Eigen::VectorXd zero_a =
        Eigen::VectorXd::Zero(robot_.nv());

    const Eigen::VectorXd gravity =
        robot_.inverseDynamics(q, zero_v, zero_a);

    // 6. Convert Cartesian force to joint torques
    return Jv.transpose() * force + gravity;
}

}