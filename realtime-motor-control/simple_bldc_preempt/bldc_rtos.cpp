
#include <algorithm>   // std::clamp(), std::max()
#include <cerrno>      // EINTR, errno
#include <cmath>       // std::abs()
#include <cstring>     // strerror()
#include <fstream>     // CSV file writing
#include <iostream>    // std::cout, std::cerr
#include <sched.h>     // SCHED_FIFO, sched_setscheduler()
#include <string>      // std::string, stoi(), stod()
#include <time.h>      // timespec, clock_gettime(), clock_nanosleep()
#include <vector>      // std::vector

// ============================================================
// 1. CONSTANTS
// ============================================================

// constexpr: compile-time constant.
// Unlike a normal variable, this value cannot change at runtime.
constexpr long NS_PER_SECOND = 1'000'000'000L;

constexpr double MAX_RAMP = 90.0;  // rad/s^2
constexpr double KP = 0.018;       // Proportional gain
constexpr double KI = 0.10;        // Integral gain

constexpr double MAX_COMMAND = 1.0;
constexpr double MIN_COMMAND = -1.0;

// ============================================================
// 2. TELEMETRY DATA STRUCTURE
// ============================================================

// struct groups related variables into one data type.
// Each Sample represents one control-loop iteration.
struct Sample {
    double t;            // Simulation time (seconds)
    double target;       // Desired motor speed (rad/s)
    double ramp;         // Rate-limited target (rad/s)
    double speed;        // Simulated motor speed (rad/s)
    double command;      // Controller output [-1, +1]

    double lateness_us;  // Wake-up delay (microseconds)
    double jitter_us;    // Difference from expected period
    double exec_us;      // Execution time of control calculations

    int missed;          // 1 = deadline missed, 0 = met
};

// ============================================================
// 3. TIME UTILITY FUNCTIONS
// ============================================================

// static at file scope: function has internal linkage.
// It is intended to be used only inside this source file.

// timespec stores time as:
// tv_sec  = seconds
// tv_nsec = nanoseconds

// Pass by reference (&) because we want to MODIFY t.
static void advance(timespec& t, long ns)
{
    t.tv_nsec += ns;

    // Carry complete seconds into tv_sec.
    t.tv_sec += t.tv_nsec / NS_PER_SECOND;

    // Keep nanoseconds in the range [0, 1 billion).
    t.tv_nsec %= NS_PER_SECOND;
}

// Calculate difference between two timestamps in nanoseconds.
//
// const: guarantees that a and b are not modified
// through these references.
// &: avoids copying the timespec objects.
static long long delta(
    const timespec& a,
    const timespec& b)
{
    return
        (a.tv_sec - b.tv_sec) * 1'000'000'000LL
        + (a.tv_nsec - b.tv_nsec);
}

// Return current monotonic time.
//
// CLOCK_MONOTONIC is suitable for measuring elapsed time.
// Unlike wall-clock time, it is not affected by manual
// system-clock changes.
static timespec now()
{
    timespec t{};  // Zero-initialize all members.

    clock_gettime(CLOCK_MONOTONIC, &t);

    return t;
}

// ============================================================
// 4. PROGRAM ENTRY POINT
// ============================================================

int main(int argc, char** argv)
{
    // --------------------------------------------------------
    // 4.1 DEFAULT CONFIGURATION
    // --------------------------------------------------------

    bool fifo = false;      // Use normal Linux scheduler
    int hz = 1000;          // Control frequency: 1000 Hz
    double seconds = 8.0;   // Simulation duration

    // argc = number of command-line arguments
    // argv = array containing the argument strings
    //
    // Example:
    // ./bldc_control --fifo --hz 1000 --seconds 8

    for (int i = 1; i < argc; ++i)
    {
        std::string arg = argv[i];

        if (arg == "--fifo")
        {
            fifo = true;
        }
        else if (arg == "--hz" && i + 1 < argc)
        {
            hz = std::stoi(argv[++i]);
        }
        else if (arg == "--seconds" && i + 1 < argc)
        {
            seconds = std::stod(argv[++i]);
        }
        else
        {
            std::cerr
                << "Usage: " << argv[0]
                << " [--fifo] [--hz 1000] [--seconds 8]\n";

            return 1;
        }
    }

    // Validate user input.
    if (hz < 1 || hz > 10000 ||
        !std::isfinite(seconds) ||
        seconds <= 0 || seconds > 300)
    {
        std::cerr << "Invalid frequency/duration\n";
        return 1;
    }

    // --------------------------------------------------------
    // 4.2 LINUX REAL-TIME SCHEDULING
    // --------------------------------------------------------

    if (fifo)
    {
        // sched_param holds scheduler-specific parameters.
        sched_param p{};

        // Linux real-time priorities typically range 1 to 99.
        // Higher number = higher real-time priority.
        p.sched_priority = 60;

        // pid = 0 means the calling thread.
        //
        // SCHED_FIFO:
        // Fixed-priority real-time scheduling.
        //
        // Important: this does not guarantee zero jitter.
        if (sched_setscheduler(0, SCHED_FIFO, &p) != 0)
        {
            std::cerr
                << "SCHED_FIFO: " << strerror(errno)
                << " (try sudo)\n";

            return 1;
        }
    }

    // --------------------------------------------------------
    // 4.3 CONTROL LOOP TIMING
    // --------------------------------------------------------

    // Period = 1 / frequency
    //
    // At 1000 Hz:
    // period = 1,000,000 ns = 1 ms
    // dt     = 0.001 seconds

    const long period = NS_PER_SECOND / hz;
    const double dt = 1.0 / hz;

    // Number of control iterations.
    //
    // static_cast<size_t> explicitly converts the
    // floating-point result to an unsigned size type.
    const size_t count =
        static_cast<size_t>(seconds * hz);

    // Preallocate memory BEFORE entering the real-time loop.
    //
    // This avoids repeated vector allocations in the loop.
    std::vector<Sample> samples(count);

    // --------------------------------------------------------
    // 4.4 MOTOR AND CONTROLLER STATE
    // --------------------------------------------------------

    double speed = 0.0;      // Current motor speed
    double ramp = 0.0;       // Smoothed speed reference
    double integral = 0.0;   // PI controller integral state
    double command = 0.0;    // Normalized motor drive

    // release = next scheduled wake-up time
    // previous = previous actual loop start time
    timespec release = now();
    timespec previous = release;

    // ========================================================
    // 5. MAIN REAL-TIME CONTROL LOOP
    // ========================================================

    for (size_t i = 0; i < count; ++i)
    {
        // ----------------------------------------------------
        // STEP 1: WAIT FOR NEXT CONTROL PERIOD
        // ----------------------------------------------------

        // Advance the absolute wake-up deadline.
        advance(release, period);

        int rc;

        do
        {
            // TIMER_ABSTIME means sleep until an ABSOLUTE time.
            //
            // This avoids accumulating relative sleep drift.
            rc = clock_nanosleep(
                CLOCK_MONOTONIC,
                TIMER_ABSTIME,
                &release,
                nullptr
            );

        } while (rc == EINTR);

        if (rc != 0)
        {
            std::cerr
                << "clock_nanosleep: "
                << strerror(rc) << '\n';

            return 1;
        }

        // Record actual wake-up time.
        timespec start = now();

        // Nominal simulation time.
        double t = (i + 1) * dt;

        // ----------------------------------------------------
        // STEP 2: GENERATE TARGET SPEED
        // ----------------------------------------------------

        // Desired speed profile:
        //
        // t < 0.5s          -> 0 rad/s
        // t < 55% duration  -> 120 rad/s
        // t < 80% duration  -> 65 rad/s
        // Otherwise         -> 0 rad/s

        double target;

        if (t < 0.5)
        {
            target = 0.0;
        }
        else if (t < seconds * 0.55)
        {
            target = 120.0;
        }
        else if (t < seconds * 0.80)
        {
            target = 65.0;
        }
        else
        {
            target = 0.0;
        }

        // ----------------------------------------------------
        // STEP 3: SPEED RAMP LIMITER
        // ----------------------------------------------------

        // Avoid an instantaneous jump in reference speed.
        //
        // Maximum reference change per iteration:
        //
        // MAX_RAMP * dt
        //
        // At 1 kHz:
        // 90 * 0.001 = 0.09 rad/s per iteration

        const double difference = target - ramp;

        const double max_step = MAX_RAMP * dt;

        const double limited_step = std::clamp(
            difference,
            -max_step,
            max_step
        );

        ramp += limited_step;

        // ----------------------------------------------------
        // STEP 4: PI SPEED CONTROLLER
        // ----------------------------------------------------

        // Error = desired speed - actual speed
        double error = ramp - speed;

        // Integral part accumulates error over time.
        //
        // trial = integral + error * dt
        //
        // Clamp integral to prevent excessive accumulation.
        double trial = std::clamp(
            integral + error * dt,
            -100.0,
            100.0
        );

        // PI control equation:
        //
        // u = Kp * error + Ki * integral
        double unsat =
            KP * error + KI * trial;

        // Saturate motor command to [-1, +1].
        command = std::clamp(
            unsat,
            MIN_COMMAND,
            MAX_COMMAND
        );

        // Anti-windup:
        //
        // Update integral when:
        // 1. Output is not saturated, OR
        // 2. Error drives the output back toward valid range.
        //
        // This prevents integral windup during saturation.

        if (std::abs(unsat - command) < 1e-9 ||
            (unsat > command && error < 0) ||
            (unsat < command && error > 0))
        {
            integral = trial;
        }

        // ----------------------------------------------------
        // STEP 5: SIMULATED BLDC MOTOR DYNAMICS
        // ----------------------------------------------------

        // Apply a simulated external load during part
        // of the experiment.
        //
        // This tests how the controller rejects disturbance.

        double load = 0.0;

        if (t > seconds * 0.35 &&
            t < seconds * 0.65)
        {
            load = 12.0;
        }

        // Simplified first-order motor speed model:
        //
        // acceleration =
        //     drive_gain * command
        //     - drag_coefficient * speed
        //     - external_load
        //
        // This is NOT a full electrical BLDC/FOC model.

        double acceleration =
            180.0 * command
            - 0.65 * speed
            - load;

        // Euler numerical integration:
        //
        // speed_new = speed_old + acceleration * dt
        speed += acceleration * dt;

        // ----------------------------------------------------
        // STEP 6: MEASURE REAL-TIME PERFORMANCE
        // ----------------------------------------------------

        timespec finish = now();

        // Wake-up lateness:
        // Actual wake-up minus scheduled wake-up.
        double lateness =
            delta(start, release) / 1000.0;

        // Period jitter:
        // Actual start-to-start period minus ideal period.
        double jitter =
            (delta(start, previous) - period) / 1000.0;

        // Execution time:
        // Time spent performing control calculations.
        double execution =
            delta(finish, start) / 1000.0;

        // Deadline check:
        //
        // The current iteration should finish before
        // the next scheduled release.
        int missed =
            delta(finish, release) > period;

        // ----------------------------------------------------
        // STEP 7: STORE TELEMETRY
        // ----------------------------------------------------

        // Store data in preallocated memory.
        // No file I/O inside the control loop.
        samples[i] = {
            t,
            target,
            ramp,
            speed,
            command,
            lateness,
            jitter,
            execution,
            missed
        };

        // Save actual start time for next jitter calculation.
        previous = start;
    }

    // ========================================================
    // 6. WRITE TELEMETRY TO CSV
    // ========================================================

    // File operations are performed AFTER the real-time loop.
    std::ofstream out("telemetry.csv");

    if (!out)
    {
        std::cerr << "Cannot open telemetry.csv\n";
        return 1;
    }

    out << "time_s,target_rad_s,ramped_rad_s,"
        << "speed_rad_s,command,wakeup_lateness_us,"
        << "period_jitter_us,execution_us,deadline_miss\n";

    // ========================================================
    // 7. CALCULATE PERFORMANCE STATISTICS
    // ========================================================

    double maxlate = 0.0;
    double maxjitter = 0.0;
    double maxexec = 0.0;

    int misses = 0;

    // const auto&:
    //
    // auto  -> compiler deduces Sample type
    // &     -> reference, avoids copying Sample
    // const -> read-only access
    for (const auto& s : samples)
    {
        out << s.t << ','
            << s.target << ','
            << s.ramp << ','
            << s.speed << ','
            << s.command << ','
            << s.lateness_us << ','
            << s.jitter_us << ','
            << s.exec_us << ','
            << s.missed << '\n';

        maxlate = std::max(
            maxlate, s.lateness_us
        );

        maxjitter = std::max(
            maxjitter, std::abs(s.jitter_us)
        );

        maxexec = std::max(
            maxexec, s.exec_us
        );

        misses += s.missed;
    }

    out.close();

    // ========================================================
    // 8. PRINT FINAL RESULTS
    // ========================================================

    std::cout
        << "Scheduler: "
        << (fifo ? "SCHED_FIFO" : "SCHED_OTHER")
        << '\n'

        << "Samples: " << count << '\n'

        << "Max wake-up lateness (us): "
        << maxlate << '\n'

        << "Max abs period jitter (us): "
        << maxjitter << '\n'

        << "Max execution time (us): "
        << maxexec << '\n'

        << "Deadline misses: "
        << misses << '\n'

        << "Output: telemetry.csv\n";

    return 0;
}
