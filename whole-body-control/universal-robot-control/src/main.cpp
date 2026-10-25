
#include "urc/robot_model.hpp"
#include "urc/computed_torque.hpp"
#include "urc/cartesian_impedance.hpp"

#include <Eigen/Dense>
#include <iostream>
#include <string>
#include <exception>

int main(int argc, char** argv)
{
    try {
        const std::string urdf =
            argc > 1 ? argv[1] : "models/arm6/arm6.urdf";

        urc::RobotModel robot(urdf);

        // Common robot state for both controllers
        Eigen::VectorXd q = robot.neutral();
        q[0] = 0.5;
        q[1] = 0.3;
        q[2] = -0.5;

        Eigen::VectorXd v = Eigen::VectorXd::Zero(robot.nv());
        Eigen::VectorXd a = Eigen::VectorXd::Zero(robot.nv());

        std::cout << "\n========================================\n";
        std::cout << "        ROBOT MODEL INFORMATION\n";
        std::cout << "========================================\n";

        std::cout << "Robot nq = " << robot.nq()
                  << ", nv = " << robot.nv()
                  << ", na = " << robot.na() << "\n";

        std::cout << "Joint positions: "
                  << q.transpose() << "\n";

        std::cout << "Tool position: "
                  << robot.framePosition(q, "tool0").transpose()
                  << "\n";

        std::cout << "Mass matrix:\n"
                  << robot.massMatrix(q) << "\n";


        // ========================================
        // CONTROLLER 1: COMPUTED TORQUE
        // ========================================

        std::cout << "\n========================================\n";
        std::cout << "   CONTROLLER 1: COMPUTED TORQUE\n";
        std::cout << "========================================\n";

        urc::ComputedTorqueController computed_controller(
            robot,
            Eigen::VectorXd::Constant(robot.nv(), 100.0),
            Eigen::VectorXd::Constant(robot.nv(), 20.0)
        );

        Eigen::VectorXd tau_computed =
            computed_controller.update(q, v, q, v, a);

        std::cout << "Kp = 100, Kd = 20\n";
        std::cout << "Desired joint position: "
                  << q.transpose() << "\n";

        std::cout << "Computed torque output [Nm]: "
                  << tau_computed.transpose() << "\n";


        // ========================================
        // CONTROLLER 2: CARTESIAN IMPEDANCE
        // ========================================

        std::cout << "\n========================================\n";
        std::cout << "   CONTROLLER 2: CARTESIAN IMPEDANCE\n";
        std::cout << "========================================\n";

        urc::CartesianImpedanceController impedance_controller(
            robot, "tool0"
        );

        impedance_controller.setGains(
            Eigen::Vector3d(300.0, 300.0, 300.0),
            Eigen::Vector3d(30.0, 30.0, 30.0)
        );

        Eigen::Vector3d x_current =
            robot.framePosition(q, "tool0");

        // Request a 5 mm displacement along world X
        Eigen::Vector3d x_des =
            x_current + Eigen::Vector3d(0.005, 0.0, 0.0);

        Eigen::Vector3d dx_des = Eigen::Vector3d::Zero();

        Eigen::VectorXd tau_impedance =
            impedance_controller.update(q, v, x_des, dx_des);

        std::cout << "Cartesian stiffness Kp [N/m]: "
                  << "300 300 300\n";

        std::cout << "Cartesian damping Kd [Ns/m]: "
                  << "30 30 30\n";

        std::cout << "Current tool position [m]: "
                  << x_current.transpose() << "\n";

        std::cout << "Desired tool position [m]: "
                  << x_des.transpose() << "\n";

        std::cout << "Cartesian position error [m]: "
                  << (x_des - x_current).transpose() << "\n";

        std::cout << "Impedance torque output [Nm]: "
                  << tau_impedance.transpose() << "\n";


        // ========================================
        // COMPARISON
        // ========================================

        std::cout << "\n========================================\n";
        std::cout << "        CONTROLLER COMPARISON\n";
        std::cout << "========================================\n";

        std::cout << "Computed torque [Nm]: "
                  << tau_computed.transpose() << "\n";

        std::cout << "Cartesian impedance [Nm]: "
                  << tau_impedance.transpose() << "\n";

        std::cout << "\nBoth controllers executed successfully.\n";

        return 0;
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
}
