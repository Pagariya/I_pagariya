#include "urc/robot_model.hpp"
#include "urc/computed_torque.hpp"
#include <gtest/gtest.h>
#include <Eigen/Eigenvalues>
#include <pinocchio/algorithm/joint-configuration.hpp>
#include <pinocchio/algorithm/frames.hpp>
#include <pinocchio/algorithm/kinematics.hpp>
#include <pinocchio/algorithm/jacobian.hpp>
#include <stdexcept>
namespace {
const std::string kUrdf = "models/arm6/arm6.urdf";
}
TEST(Model, Dimensions) {
  urc::RobotModel robot(kUrdf);
  EXPECT_EQ(robot.nq(),6);
  EXPECT_EQ(robot.nv(),6);
  EXPECT_EQ(robot.na(),6);
  EXPECT_EQ(robot.frameJacobian(robot.neutral(),"tool0").rows(),6);
}
TEST(Model, FloatingBaseDimensions) {
  urc::RobotModel robot(kUrdf,true);
  EXPECT_EQ(robot.nq(),13);
  EXPECT_EQ(robot.nv(),12);
  EXPECT_EQ(robot.na(),6);
  EXPECT_EQ(robot.neutral().size(),13);
}
TEST(Dynamics, InverseForwardConsistency) {
  urc::RobotModel robot(kUrdf);
  Eigen::VectorXd q = Eigen::VectorXd::LinSpaced(6,-0.3,0.4);
  Eigen::VectorXd v = Eigen::VectorXd::LinSpaced(6,0.1,0.6);
  Eigen::VectorXd a = Eigen::VectorXd::LinSpaced(6,-0.4,0.2);
  auto tau = robot.inverseDynamics(q,v,a);
  auto recovered = robot.forwardDynamics(q,v,tau);
  EXPECT_LT((recovered-a).norm(),1e-8);
}
TEST(Dynamics, MassMatrixPositiveDefinite) {
  urc::RobotModel robot(kUrdf);
  auto M = robot.massMatrix(Eigen::VectorXd::Constant(6,0.2));
  EXPECT_LT((M-M.transpose()).norm(),1e-9);
  Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> solver(M);
  ASSERT_EQ(solver.info(),Eigen::Success);
  EXPECT_GT(solver.eigenvalues().minCoeff(),1e-9);
}
TEST(Dynamics, GravityIsInverseDynamicsAtRest) {
  urc::RobotModel robot(kUrdf);
  auto q = Eigen::VectorXd::Constant(6,0.3);
  auto zero = Eigen::VectorXd::Zero(6);
  EXPECT_LT((robot.inverseDynamics(q,zero,zero)-robot.nonlinearEffects(q,zero)).norm(),1e-9);
}
TEST(Control, ComputedTorqueAtTargetEqualsGravity) {
  urc::RobotModel robot(kUrdf);
  urc::ComputedTorqueController controller(robot,Eigen::VectorXd::Constant(6,100),Eigen::VectorXd::Constant(6,20));
  auto q = Eigen::VectorXd::Constant(6,0.25);
  auto zero = Eigen::VectorXd::Zero(6);
  EXPECT_LT((controller.update(q,zero,q,zero,zero)-robot.nonlinearEffects(q,zero)).norm(),1e-9);
}
TEST(Model, RejectInvalidState) {
  urc::RobotModel robot(kUrdf);
  EXPECT_THROW(robot.massMatrix(Eigen::VectorXd::Zero(5)),std::invalid_argument);
}
