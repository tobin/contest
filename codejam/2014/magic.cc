#include <vector>
#include <set>
#include <iostream>
#include <algorithm>

std::vector<std::set<int> > readmatrix() {
  std::vector<std::set<int> > rslt;
  for (int i=0; i<4; i++) {
    std::set<int> items;
    for (int j=0; j<4; j++) {
      int x;
      std::cin >> x;
      items.insert(x);            
    }
    rslt.push_back(items);
  }
  return rslt;
}

int main(int argc, char **argv) {
  int T;  // number of test cases
  std::cin >> T;
  
  for (int t=0; t<T; t++) {    
    std::cout << "Test Case #" << t+1 << ": ";
    int nA, nB;
    
    std::cin >> nA;
    auto A = readmatrix();
    
    std::cin >> nB;
    auto B = readmatrix();
       
    std::set<int> rslt; // = A[nA] & B[nB]
    std::set_intersection(A[nA-1].begin(), A[nA-1].end(), 
			  B[nB-1].begin(), B[nB-1].end(), 
			  inserter(rslt, rslt.begin()));
    
    if (rslt.empty())
      std::cout << "Volunteer cheated!" << std::endl;
    else if (rslt.size() > 1) 
      std::cout << "Bad Magician!" << std::endl;
    else // exactly one element
      std::cout << *rslt.begin() << std::endl;    
  }
  
  return 0;
} 




    
    
