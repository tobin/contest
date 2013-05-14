#include <cstdlib>
#include <iostream>
#include <vector>
#include <utility>

using namespace std;

/* 
   Algorithm:  I test whether M randomly chosen locations are within the
   bounds of the polygon.  The area of the polygon should be proportional
   to the number of tests that succeed.  
 */

class Polygon {
private:
  vector<pair<double,double> > verticies;
public:
  Polygon() {
    verticies.clear();
  }

  Polygon(vector<pair<double,double> > verticies) {
    this->verticies = verticies;

  }

  bool isInside(double x, double y) {
    return (rand() > RAND_MAX/2.0);
  }

};

class PolygonArea {
public:
  static double estimate(int M) {
    int N = 0;
    Polygon p;
    for (int i=0; i<M; i++) 
      if (p.isInside(rand()*10.0/RAND_MAX, rand()*10.0/RAND_MAX))
	N++;
    double result = 100 * (double)N/M;
    cout << "Estimating area = " << result << endl;
    return result;
  }
};

int main(int argc, char **argv) {
  PolygonArea p;
  for (int i=0; i<10; i++)
    cout << p.estimate(17) << endl;
}
