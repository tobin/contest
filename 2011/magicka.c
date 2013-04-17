#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define DEBUG if (0) 
int main(int argc, char **argv) {

  int T;
  scanf("%d", &T);
  for (int r=0; r<T; r++) {
    printf("Case #%d: ", r+1);
    int C, D, N;
    char map[26][26];
    char opp[26][26];
    // initialize the map
    for (int i=0; i<26; i++)
      for (int j=0; j<26; j++) {
	map[i][j] = 0;
	opp[i][j] = 0;
      }
    // read the triplets of combining characters
    scanf("%d", &C);
    for (int i=0; i<C; i++) {
      char s[4];
      scanf("%s", s);
      assert(strlen(s)==3);
      map[s[0]-'A'][s[1]-'A']=s[2];
      map[s[1]-'A'][s[0]-'A']=s[2];
      DEBUG printf(" %c %c --> %c \n", s[0], s[1], s[2]);
    }
    // read the pairs of annihilating characters
    scanf("%d", &D);
    for (int i=0; i<D; i++) {
      char s[4];
      scanf("%s", s);
      assert(strlen(s)==2);
      opp[s[0]-'A'][s[1]-'A']=1;
      opp[s[1]-'A'][s[0]-'A']=1;
      DEBUG printf(" %c %c --> annihilate! \n", s[0], s[1]);
    }
    scanf("%d", &N);
    char s[N+1]; // sequence of invocations
    char p[N+1]; // resulting string    
    int jj = 0;  // current index into p
    p[jj]=0;
    scanf("%s", s);
    for (int i=0; i<N; i++) {
      DEBUG printf("current stack: '%s'\n", p);
      char c = s[i];
      DEBUG printf("push char %c\n", c);
      char m = 0;
      if (jj > 0)
	m = map[p[jj-1]-'A'][c-'A'];
      if (m == 0) {
	// just add this character
	p[jj] = c;
	jj ++;
	p[jj] = 0;
      } else {
	DEBUG printf(" %c %c --> %c \n", p[jj-1], c, m);
	p[jj - 1] = m;
      }
      
      for (int ii=0; ii<jj; ii++) {
	if (opp[p[ii]-'A'][p[jj-1]-'A']) {
	  DEBUG printf("%c and %c are opposed!\n",p[ii],p[jj-1]);
	  jj = 0;
	  p[jj] = 0;
	  break;
	}
      }
      
    }
    printf("[");
    for (int k=0; k<jj; k++) {
      printf("%c", p[k]);
      if (k<(jj-1)) 
	printf(", ");
    }
    printf("]\n");
  }
  return 0;
}
