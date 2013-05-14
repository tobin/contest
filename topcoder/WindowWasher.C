#include <iostream>
#include <utility>
#include <vector>
#include <map>

using namespace std;

class WindowWasher {
  
  map< pair<int,int>,  pair<int,int> > table;
  
  // wash (columns, workers)  returns (columns to give, best time)
  pair<int,int> wash(int cols, int workers, vector<int> T) {
    if (workers == 0) 
      return table[make_pair(cols,workers)] = make_pair( cols, cols*T[0] );
    
    if (table.find(make_pair(cols,workers)) != table.end())     
      return table[make_pair(cols,workers)];
    
    pair<int,int> result = make_pair(0, infinity);
    
    for (int columns = 0; columns <= cols; columns ++) {
      pair<int,int> subproblem = wash(cols - columns, workers - 1, T);
      unsigned int time = max ( subproblem.second , columns * T[workers] );
      if (time < result.second) 
	result = make_pair(columns, time);
    }  
    return (table[make_pair(cols,workers)] = make_pair(bestcols,besttime));
  }
  
public:

  int fastest(int w, int h, vector<int> T) {
    return wash(w, T.size()-1, T).second * h;
  }
};


int main(void) {

  WindowWasher washer;
  vector<int> T;
  T.push_back(111);
  T.push_back(56);
  T.push_back(931);
  T.push_back(22);
  T.push_back(445);
  T.push_back(90);
  T.push_back(14);
  T.push_back(222);

  cout << washer.fastest(421, 936, T) << endl;
  return 0;
}

