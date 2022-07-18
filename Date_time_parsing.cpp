// Program take number of data points do the user want to input and later asks time (HH.MM) and date (in format DD.MM.YYYY)


// Program to check parsable date and time and displays it later:
   //  1. It checks that teh input is not null 
   //  2. It also checks if the data entered is number or not
   //  3. In case of failure it asks you to enter the data
   
   
//Creator - Anshul Pagariya
 

#include <iostream>
#include <string>
#include <sstream>
#include <cstdlib>
#include <stdexcept>
#include<map>

using namespace std;




struct Date {
    int day;
    int month;
    int year;
};


struct Time {
    int hour;
    int minute;
    
};


bool is_number(string str)
{
    for (size_t i = 0; i < str.length(); i++)
    {
        if (!isdigit(str[i]))
        {
            return false;   
        }
    }
    return true;
}



Time parse_time(string str)
{
    istringstream iss(str);
    
    string hour_str;
    getline(iss, hour_str, '.');
    
    string minute_str;
    getline(iss, minute_str,'.');
    
    if (!is_number(hour_str)){
        throw exception();
        }
        
    int hour = atoi(hour_str.c_str());
    
    
    if (!hour)
    {
        throw exception();
        }
    if (!is_number(minute_str)){
        throw exception();
        }
    int minute = atoi(minute_str.c_str());
    if (!minute){
        throw exception();
        }
    return Time{hour, minute};
    
    
} 





Date parse(string str)
{
    istringstream iss(str);
    
    string day_str;
    getline(iss, day_str, '.');
    
    string month_str;
    getline(iss, month_str, '.');
    
    string year_str; 
    getline(iss, year_str);
    
    if (!is_number(day_str))
    {
        throw exception();   
    }
    int day = atoi(day_str.c_str());
    if (!day)
    {
        throw exception();
    }
    
    if (!is_number(month_str))
    {
        throw exception();   
    }
    int month = atoi(month_str.c_str());
    if (!month)
    {
        throw exception();
    }
    
    if (!is_number(year_str))
    {
        throw exception();   
    }
    int year = atoi(year_str.c_str());
    if (!year)
    {
        throw exception();
    }
     
    return Date{day, month, year};
}

int main()
{  int t;
   map<string, string>  time_date_data;
   cout << "How much data do you want to enter?";  //how many date and time do you want to save
   cin >> t;
   for(int i= 1; i <= t; i++){
        bool right_input = true;
        while (right_input == true) {
                string f,g;
                cout << "Please enter a data in format DD.MM.YYYY :";
                cin >> f;
                cout << "Please enter a data in format HH.MM :";
                cin >> g;
                try
                {
                    Date date = parse(f);
                    Time time = parse_time(g);
                    time_date_data[f] = g;
                    right_input = false;
                }
                catch (...)
                {
                    cout << "Invalid date or time, Please insert date in DD.MM.YYYY and time in HH.MM format.\n";  
                    
                }
                }
   }
   map <string,string> :: iterator iter;
   
   for (iter = time_date_data.begin(); iter != time_date_data.end(); iter++)
   {
     cout<<"You entered: date "<<(*iter).first<<" and time is "<<(*iter).second<<"\n";
   }

}
