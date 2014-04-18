#include <stdio.h>

double min(double x, double y) { return x > y ? y : x; }

int main(int argc, char **argv) {
  
  int T;
  scanf("%d", &T);
  
  for (int t=0; t<T; t++) {
    double C, F, X;
    scanf("%lf %lf %lf", &C, &F, &X);
    
    printf("Case #%d: ", t+1);
    
    double S = 0;  // Score, i.e. number of cookies
    double R = 2;  // Rate of production, cookies per second
    double T = 0;  // Elapsed time
						       
    double eps = 1e-6;

    while (S + eps < X) {
      
      double dt = 0;
      
      if ((S + eps >=C) && ((X-S)/R > (X-S+C)/(R+F))) {
	S -= C;
	R += F;
	
	// Advance to the next possible factory buying time or win
	dt = min((X-S)/R, C/R);
      } else {
	if (S + eps >= C) {
	  // If we didn't buy a factory this time, we won't but any more
	  dt = (X-S)/R;
	} else {
	  dt = min((X-S)/R, C/R);
	} 
      }
      
      T += dt;        // Total elapsed time
      S += dt * R;    // Total number of cookies we'll have
    }

    printf("%lf\n", T);
  }
  return 0;
}
