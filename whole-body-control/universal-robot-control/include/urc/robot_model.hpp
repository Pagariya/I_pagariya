#pragma once
#include <Eigen/Core>
#include <pinocchio/multibody/model.hpp>
#include <pinocchio/multibody/data.hpp>
#include <string>

namespace urc {
class RobotModel {
public:
  explicit RobotModel(const std::string& urdf_path, bool floating_base = false);
  int nq() const { return model_.nq; }
  int nv() const { return model_.nv; }
  int na() const { return model_.nv - (floating_base_ ? 6 : 0); }
  bool floatingBase() const { return floating_base_; }
  Eigen::VectorXd neutral() const;
  Eigen::MatrixXd massMatrix(const Eigen::VectorXd& q);
  Eigen::VectorXd nonlinearEffects(const Eigen::VectorXd& q, const Eigen::VectorXd& v);
  Eigen::VectorXd inverseDynamics(const Eigen::VectorXd& q, const Eigen::VectorXd& v, const Eigen::VectorXd& a);
  Eigen::VectorXd forwardDynamics(const Eigen::VectorXd& q, const Eigen::VectorXd& v, const Eigen::VectorXd& generalized_forces);
  Eigen::MatrixXd frameJacobian(const Eigen::VectorXd& q, const std::string& frame_name);
  Eigen::Vector3d framePosition(const Eigen::VectorXd& q, const std::string& frame_name);
  const pinocchio::Model& model() const { return model_; }
private:
  void checkState(const Eigen::VectorXd& q, const Eigen::VectorXd& v) const;
  pinocchio::Model model_;
  pinocchio::Data data_;
  bool floating_base_;
};
}
