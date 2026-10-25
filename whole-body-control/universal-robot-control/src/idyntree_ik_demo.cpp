#include <iDynTree/InverseKinematics.h>
#include <iDynTree/Core/VectorDynSize.h>
#include <iDynTree/Core/Transform.h>
#include <iDynTree/Core/Position.h>

#include <iostream>
#include <stdexcept>

int main()
{
    const std::string urdf = "models/arm6/arm6.urdf";

    iDynTree::InverseKinematics ik;

    // 1. Load robot model
    if (!ik.loadModelFromFile(urdf)) {
        std::cerr << "Failed to load URDF\n";
        return 1;
    }

    // 2. Initial joint configuration
    // Our current example robot has six 1-DoF joints.
    iDynTree::VectorDynSize q0(6);
    q0.zero();

    const iDynTree::Transform world_H_base =
        iDynTree::Transform::Identity();

    if (!ik.setCurrentRobotConfiguration(world_H_base, q0)) {
        std::cerr << "Failed to set initial configuration\n";
        return 1;
    }

    // 3. Desired end-effector position (meters)
    iDynTree::Position desired;
    desired(0) = 0.10;
    desired(1) = 0.05;
    desired(2) = 1.55;

    // 4. Add position-only IK target
    if (!ik.addPositionTarget("tool0", desired)) {
        std::cerr << "Failed to add tool0 target\n";
        return 1;
    }

    // 5. Use soft target optimization
    ik.setTargetResolutionMode(
        "tool0",
        iDynTree::InverseKinematicsTreatTargetAsConstraintNone
    );

    ik.setMaxIterations(300);

    // 6. Solve
    if (!ik.solve()) {
        std::cerr << "IK failed\n";
        return 1;
    }

    // 7. Read optimized configuration
    iDynTree::Transform solvedBase;
    iDynTree::VectorDynSize q_solution(6);

    if (!ik.getFullJointsSolution(solvedBase, q_solution)) {
        std::cerr << "Failed to retrieve solution\n";
        return 1;
    }

    std::cout << "IK joint angles (rad):\n";
    for (unsigned int i = 0; i < q_solution.size(); ++i) {
        std::cout << "q[" << i << "] = "
                  << q_solution(i) << "\n";
    }

    return 0;
}