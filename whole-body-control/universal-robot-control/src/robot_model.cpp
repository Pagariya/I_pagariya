#include "urc/robot_model.hpp"
#include <pinocchio/parsers/urdf.hpp>
#include <pinocchio/algorithm/joint-configuration.hpp>
#include <pinocchio/algorithm/kinematics.hpp>
#include <pinocchio/algorithm/frames.hpp>
#include <pinocchio/algorithm/jacobian.hpp>
#include <pinocchio/algorithm/crba.hpp>
#include <pinocchio/algorithm/rnea.hpp>
#include <pinocchio/algorithm/aba.hpp>
#include <stdexcept>

namespace urc {
RobotModel::RobotModel(const std::string& path, bool floating_base)
    : model_(), data_(model_), floating_base_(floating_base) {
  if (floating_base) {
    pinocchio::urdf::buildModel(path, pinocchio::JointModelFreeFlyer(), model_);
  } else {
    pinocchio::urdf::buildModel(path, model_);
  }
  data_ = pinocchio::Data(model_);
}
void RobotModel::checkState(const Eigen::VectorXd& q, const Eigen::VectorXd& v) const {
  if (q.size() != nq() || v.size() != nv() || !q.allFinite() || !v.allFinite())
    throw std::invalid_argument("Invalid generalized configuration or velocity");
}
Eigen::VectorXd RobotModel::neutral() const { return pinocchio::neutral(model_); }
Eigen::MatrixXd RobotModel::massMatrix(const Eigen::VectorXd& q) {
  if (q.size() != nq() || !q.allFinite()) throw std::invalid_argument("Invalid q");
  pinocchio::crba(model_, data_, q);
  data_.M.triangularView<Eigen::StrictlyLower>() = data_.M.transpose().triangularView<Eigen::StrictlyLower>();
  return data_.M;
}
Eigen::VectorXd RobotModel::nonlinearEffects(const Eigen::VectorXd& q, const Eigen::VectorXd& v) {
  checkState(q,v);
  return pinocchio::nonLinearEffects(model_, data_, q, v);
}
Eigen::VectorXd RobotModel::inverseDynamics(const Eigen::VectorXd& q, const Eigen::VectorXd& v, const Eigen::VectorXd& a) {
  checkState(q,v);
  if (a.size() != nv() || !a.allFinite()) throw std::invalid_argument("Invalid a");
  return pinocchio::rnea(model_, data_, q, v, a);
}
Eigen::VectorXd RobotModel::forwardDynamics(const Eigen::VectorXd& q, const Eigen::VectorXd& v, const Eigen::VectorXd& generalized_forces) {
  checkState(q,v);
  if (generalized_forces.size() != nv() || !generalized_forces.allFinite()) throw std::invalid_argument("Invalid forces");
  // For floating-base robots this is generalized-force dynamics, not an actuator-only interface.
  // Contact forces must be incorporated explicitly by a higher-level constrained dynamics solver.
  return pinocchio::aba(model_, data_, q, v, generalized_forces);
}
Eigen::MatrixXd RobotModel::frameJacobian(const Eigen::VectorXd& q, const std::string& frame_name) {
  if (q.size() != nq() || !q.allFinite()) throw std::invalid_argument("Invalid q");
  if (!model_.existFrame(frame_name)) throw std::invalid_argument("Unknown frame: " + frame_name);
  pinocchio::computeJointJacobians(model_, data_, q);
  pinocchio::updateFramePlacements(model_, data_);
  Eigen::MatrixXd J(6,nv());
  pinocchio::getFrameJacobian(model_, data_, model_.getFrameId(frame_name), pinocchio::LOCAL_WORLD_ALIGNED, J);
  return J;
}
Eigen::Vector3d RobotModel::framePosition(const Eigen::VectorXd& q, const std::string& frame_name) {
  if (q.size() != nq() || !q.allFinite()) throw std::invalid_argument("Invalid q");
  if (!model_.existFrame(frame_name)) throw std::invalid_argument("Unknown frame: " + frame_name);
  pinocchio::forwardKinematics(model_, data_, q);
  pinocchio::updateFramePlacements(model_, data_);
  return data_.oMf[model_.getFrameId(frame_name)].translation();
}
}
