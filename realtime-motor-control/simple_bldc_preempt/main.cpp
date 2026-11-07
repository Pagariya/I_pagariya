#include <algorithm>
#include <cerrno>
#include <cmath>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sched.h>
#include <string>
#include <time.h>
#include <vector>

struct Sample { double t, target, ramp, speed, command, lateness_us, jitter_us, exec_us; int missed; };
static void advance(timespec &t, long ns) { t.tv_nsec += ns; t.tv_sec += t.tv_nsec / 1000000000L; t.tv_nsec %= 1000000000L; }
static long long delta(const timespec &a, const timespec &b) { return (a.tv_sec-b.tv_sec)*1000000000LL + (a.tv_nsec-b.tv_nsec); }
static timespec now() { timespec t{}; clock_gettime(CLOCK_MONOTONIC,&t); return t; }
int main(int argc,char**argv) {
 bool fifo=false; int hz=1000; double seconds=8;
 for(int i=1;i<argc;i++) { std::string a=argv[i]; if(a=="--fifo") fifo=true; else if(a=="--hz"&&i+1<argc) hz=std::stoi(argv[++i]); else if(a=="--seconds"&&i+1<argc) seconds=std::stod(argv[++i]); else { std::cerr<<"Usage: "<<argv[0]<<" [--fifo] [--hz 1000] [--seconds 8]\n"; return 1; } }
 if(hz<1||hz>10000||seconds<=0||seconds>300) {std::cerr<<"Invalid frequency/duration\n";return 1;}
 if(fifo) { sched_param p{};p.sched_priority=60; if(sched_setscheduler(0,SCHED_FIFO,&p)) {std::cerr<<"SCHED_FIFO: "<<strerror(errno)<<" (try sudo)\n";return 1;} }
 const long period=1000000000L/hz; const double dt=1.0/hz; const size_t count=static_cast<size_t>(seconds*hz);
 std::vector<Sample> samples(count); // preallocate before loop
 double speed=0, ramp=0, integral=0, command=0; timespec release=now(), previous=release;
 for(size_t i=0;i<count;i++) {
  advance(release,period); int rc; do {rc=clock_nanosleep(CLOCK_MONOTONIC,TIMER_ABSTIME,&release,nullptr);} while(rc==EINTR);
  if(rc) {std::cerr<<"clock_nanosleep: "<<strerror(rc)<<"\n";return 1;}
  timespec start=now(); double t=(i+1)*dt;
  double target=t<0.5?0:(t<seconds*0.55?120:(t<seconds*0.8?65:0));
  const double max_ramp=90.0; ramp+=std::clamp(target-ramp,-max_ramp*dt,max_ramp*dt);
  double error=ramp-speed;
  double trial=std::clamp(integral+error*dt,-100.0,100.0);
  double unsat=0.018*error+0.10*trial;
  command=std::clamp(unsat,-1.0,1.0);
  if(std::abs(unsat-command)<1e-9 || (unsat>command&&error<0) || (unsat<command&&error>0)) integral=trial;
  // Toy BLDC speed model: normalized drive command, drag and load.
  double load=(t>seconds*0.35&&t<seconds*0.65)?12.0:0.0;
  double acceleration=180.0*command-0.65*speed-load;
  speed+=acceleration*dt;
  timespec finish=now();
  double lateness=delta(start,release)/1000.0;
  double jitter=(delta(start,previous)-period)/1000.0;
  double execution=delta(finish,start)/1000.0;
  int missed=delta(finish,release)>period;
  samples[i]={t,target,ramp,speed,command,lateness,jitter,execution,missed};previous=start;
 }
 std::ofstream out("telemetry.csv");out<<"time_s,target_rad_s,ramped_rad_s,speed_rad_s,command,wakeup_lateness_us,period_jitter_us,execution_us,deadline_miss\n";
 double maxlate=0,maxjitter=0,maxexec=0;int misses=0;
 for(const auto&s:samples) {out<<s.t<<','<<s.target<<','<<s.ramp<<','<<s.speed<<','<<s.command<<','<<s.lateness_us<<','<<s.jitter_us<<','<<s.exec_us<<','<<s.missed<<'\n';maxlate=std::max(maxlate,s.lateness_us);maxjitter=std::max(maxjitter,std::abs(s.jitter_us));maxexec=std::max(maxexec,s.exec_us);misses+=s.missed;}
 std::cout<<"Scheduler: "<<(fifo?"SCHED_FIFO":"SCHED_OTHER")<<"\nSamples: "<<count<<"\nMax wake-up lateness (us): "<<maxlate<<"\nMax abs period jitter (us): "<<maxjitter<<"\nMax execution time (us): "<<maxexec<<"\nDeadline misses: "<<misses<<"\nOutput: telemetry.csv\n";
}
