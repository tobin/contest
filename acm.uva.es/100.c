/*   @JUDGE_ID:   38209AT   100   C   ""   */
#include <stdio.h>

int main(void) {
  int i, j;
  while (2 == scanf("%d %d",&i,&j)) {
    int most = 0;
    printf("%d %d",i,j);
    for (; i<=j; i++) {
      int count = 1;
      int n = i;
      while (n != 1) { 
      	n = (n%2 == 0 ? n/2 : 3*n+1);
	count ++;
      }
      if (count > most) most = count;
    }
    printf(" %d\n",most);
  }
  return 0;
}
