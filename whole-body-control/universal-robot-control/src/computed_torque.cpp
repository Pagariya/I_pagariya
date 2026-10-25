#include "urc/computed_torque.hpp"
#include <stdexcept>
namespace urc {
ComputedTorqueController::ComputedTorqueController(RobotModel& robot, Eigen::VectorXd kp, Eigen::VectorXd kd)
    : robot_(robot), kp_(std::move(kp)), kd_(std::move(kd)) {
  if (robot.floatingBase() || robot.nq() != robot.nv() || robot.na() != robot.nv())
    throw std::invalid_argument("Computed torque controller requires a fixed-base, fully actuated robot");
  if (kp_.size() != robot.nv() || kd_.size() != robot.nv() || !kp_.allFinite() || !kd_.allFinite() ||
      (kp_.array() < 0).any() || (kd_.array() < 0).any())
    throw std::invalid_argument("Invalid controller gains");
}
Eigen::VectorXd ComputedTorqueController::update(const Eigen::VectorXd& q, const Eigen::VectorXd& v,
                                                  const Eigen::VectorXd& q_des, const Eigen::VectorXd& v_des,
                                                  const Eigen::VectorXd& a_des) {
  if (q.size() != robot_.nq() || v.size() != robot_.nv() || q_des.size() != robot_.nq() ||
      v_des.size() != robot_.nv() || a_des.size() != robot_.nv() ||
      !q.allFinite() || !v.allFinite() || !q_des.allFinite() || !v_des.allFinite() || !a_des.allFinite())
    throw std::invalid_argument("Invalid controller state or target");
  const Eigen::VectorXd commanded_acc = a_des + kp_.cwiseProduct(q_des-q) + kd_.cwiseProduct(v_des-v);
  return robot_.inverseDynamics(q, v, commanded_acc);
}
}
