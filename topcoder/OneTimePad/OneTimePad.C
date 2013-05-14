#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <limits>
#include <cmath>
#include <assert.h>

using namespace std;

class OneTimePad {
public:
  static string decrypt(vector<string> encoded);
  static string bruteforce(int m, vector<string> encoded);
  static string markovchain(string key, vector<string> encoded);
  static string viterbi(vector<string> encoded);
};


#include "frequencies.c"

// try all combinations for the N-graph starting at character M.  Return the one that
// yields the best joint probability distribution
string OneTimePad::bruteforce(int m, vector<string> encoded) {
  float bestscore = 0;
  string bestchars = "EEE";

  int N = encoded.size();      // number of messages

  // loop through all possibilities (A-Z) of this pad position
  for (char c1 = 'A'; c1<='Z'; c1++)
    for (char c2 = 'A'; c2<='Z'; c2++) 
      for (char c3 = 'A'; c3<='Z'; c3++) {
	
	// starting probability for this digraph to appear in the key
	float score = frequencies[c1 - 'A'][c2 - 'A'][c3 - 'A'];

	// compute the joint probability of all the encoded messages	
	for (int n=0; n<N; n++) {
	  int d1 = (encoded[n][m-2]-c1) % 26;
	  int d2 = (encoded[n][m-1]-c2) % 26;
	  int d3 = (encoded[n][m  ]-c3) % 26;
	  
	  if (d1<0) d1 += 26;
	  if (d2<0) d2 += 26;
	  if (d3<0) d3 += 26;

	  score *= frequencies[d1][d2][d3];	  
	}

	// see if we've done any better...
	if (score > bestscore) {
	  bestscore = score;
	  bestchars = c1;
	  bestchars += c2;
	  bestchars += c3;
	}
      }
    // append this character to the result
  return bestchars;
}

// Given the key so far, find the most probable next element of the key
string OneTimePad::markovchain(string key, vector<string> encoded) {
  float bestscore = 0;
  string bestchars = "E";

  int N = encoded.size();      // number of messages

  // Get the tail of the already-determinedkey
  int m = key.length();
  char c1 = key.at(m-2);
  char c2 = key.at(m-1);

  // loop through all possibilities (A-Z) of this pad position
  for (char c3 = 'A'; c3<='Z'; c3++) {
    
    // starting probability for this digraph to appear in the key
    float score = frequencies[c1 - 'A'][c2 - 'A'][c3 - 'A'];
    
    // compute the joint probability of all the encoded messages	
    for (int n=0; n<N; n++) {
      int d1 = (encoded[n][m-2]-c1) % 26;
      int d2 = (encoded[n][m-1]-c2) % 26;
      int d3 = (encoded[n][m  ]-c3) % 26;
      
      if (d1<0) d1 += 26;
      if (d2<0) d2 += 26;
      if (d3<0) d3 += 26;

      float prob = frequencies[d1][d2][d3];	

      if (prob==0) prob=0.1;
      score *= prob;
    }
    
    // see if we've done any better...
    if (score > bestscore) {
      bestscore = score;
      bestchars = c3;
    }
  }
  // append this character to the result
  return bestchars;
}

string OneTimePad::viterbi(vector<string> encoded) {
  int N = encoded.size();    // number of ciphertexts
  int M = encoded[0].length(); // length of each message

  float Inf = std::numeric_limits<float>::infinity();

  struct state {
    float p;
    int   prev;
  } trellis[M][26][26];

  // initialize the trellis
  for (int m=0; m<M; m++)
    for (int ii=0; ii<26; ii++)
      for (int jj=0; jj<26; jj++) {
	trellis[m][ii][jj].p = Inf; // Infinite cost
	trellis[m][ii][jj].prev = '!' - 26;
      }

  // populate the first column   
  {
    // compute single character probabilities
    float char_costs[26];
    for (int ii=0; ii<26; ii++) 
      char_costs[ii] = 0;
    for (int ii=0; ii<26; ii++) 
      for (int jj=0; jj<26; jj++)
	for (int kk=0; kk<26; kk++)
	  char_costs[ii] += frequencies[ii][jj][kk];
    // convert single character probabilities into cost
    for (int ii=0; ii<26; ii++) 
      char_costs[ii] = -log(char_costs[ii]);

    for (int ii=0; ii<26; ii++) { // try all characters
      // The only reachable states in the first column are [00][00][ii]
      
      trellis[0][0][ii].p = char_costs[ii];   // probability of seeing this character in the key
      
      for (int n=0; n<N; n++) {
	int d1 = (encoded[n][0]-'A'-ii);
	if (d1<0) d1 += 26;
	trellis[0][0][ii].p += char_costs[d1];
      }
            
    }
  }

  // propagate the first column to the second column 
  {
    // compute digram character probabilities
    float digraph_costs[26][26];

    // initialize
    for (int ii=0; ii<26; ii++) 
      for (int jj=0; jj<26; jj++)
	digraph_costs[ii][jj] = 0;

    // count
    for (int ii=0; ii<26; ii++) 
      for (int jj=0; jj<26; jj++)
	for (int kk=0; kk<26; kk++)
	  digraph_costs[ii][jj] += frequencies[ii][jj][kk];
    
    // convert to costs
    for (int ii=0; ii<26; ii++) 
      for (int jj=0; jj<26; jj++)
	digraph_costs[ii][jj] = -log(digraph_costs[ii][jj]);
       
    // loop through all initial states
    for (int ii=0; ii<26; ii++) { 
      float T3 = trellis[0][0][ii].p;  // The cost that we're in this state to begin with
      // loop through all successor states
      for (int jj=0; jj<26; jj++) { 
	float T1 = digraph_costs[ii][jj];  // cost of seeing this pattern in the key       
	float T2 = 0; // cost of seeing the implied pattern in the ciphertext
	for (int n=0; n<N; n++) {

	  int d1 = (encoded[n][0]-'A'-ii); // first character
	  int d2 = (encoded[n][1]-'A'-jj); // second character
	  	  
	  if (d1<0) d1 += 26;
	  if (d2<0) d2 += 26;
	  
	  T2 += digraph_costs[d1][d2];
	  
	}

	float T = T1 + T2 + T3; // total cost
	if (T < trellis[1][ii][jj].p) {
	  // This is the best so far
	  trellis[1][ii][jj].p = T;
	  trellis[1][ii][jj].prev = ii;
	}
      }
    }
  }

  // Convert probabilities into costs 
  for (int ii=0; ii<26; ii++) 
    for (int jj=0; jj<26; jj++)
      for (int kk=0; kk<26; kk++)
	frequencies[ii][jj][kk] = -log(frequencies[ii][jj][kk]);
  
  // propage to all further columns
  for (int m=1; m<(M-1); m++) {
    // Loop through all states [ii][jj]
    for (int ii=0; ii<26; ii++) {
      // decode the first character
      int d1[N];
      for (int n=0; n<N; n++) {
	d1[n] = (encoded[n][m-1]-'A'-ii);
	if (d1[n]<0) d1[n] += 26;
      }

      for (int jj=0; jj<26; jj++) { 
	// decode the second character
	int d2[N];
	for (int n=0; n<N; n++) {
	  d2[n] = (encoded[n][m  ]-'A'-jj);
	  if (d2[n]<0) d2[n] += 26;
	}

	// Loop through all successor states
	float T3 = trellis[m][ii][jj].p;  // The probability that we're in this state to begin with
	for (int kk=0; kk<26; kk++) {
	  // Emitting character kk would put us into state [jj][kk]	  
	  float T1 = 0;//frequencies[ii][jj][kk]; // probability of this transition in the key
	  float T2 = 0;

	  // loop through all ciphertexts
	  
	  for (int n=0; n<N; n++) {
	    int d3 = (encoded[n][m+1]-'A'-kk);
	    if (d3<0) d3 += 26;	    
	    T2 += frequencies[d1[n]][d2[n]][d3];	  
	  }
	  
	  // We have a possible edge of probability T1*T2*T3 from [ii][jj] to [jj][kk]
	  float T = T1+T2+T3; // total cost
	  if (T < trellis[m+1][jj][kk].p) {
	    // This is the best so far
	    trellis[m+1][jj][kk].p = T;
	    trellis[m+1][jj][kk].prev = ii;
	  }
	}
      }
    }
  }

  // Find which final state was best
  float bestp = Inf; // infinite cost
  int bestii = 99, bestjj = 99;
  for (int ii=0; ii<26; ii++)
    for (int jj=0; jj<26; jj++) 
      if (trellis[M-1][ii][jj].p < bestp) {
	bestp  = trellis[M-1][ii][jj].p;
	bestii = ii;
	bestjj = jj;
      }
  assert((bestii != 99) && (bestjj != 99));
  // best final state was [ii, jj], i.e. last character was jj

  // Allocate the string and assemble it from right to left
  string key(M, '!');
  for (int m=(M-1); m>=0; m--) {
    // put this character into the string
    key[m] = bestjj + 'A';
    // advance the state
    int prev = trellis[m][bestii][bestjj].prev;
    bestjj = bestii;   // [ii,jj]' = [prev,ii]
    bestii = prev;
  }

  return key;
  
}

string OneTimePad::decrypt(vector<string> encoded) {
  int M = encoded[0].length(); // length of each message

  string key = "";

  key = viterbi(encoded);
  /*
  // loop through each N-graph position
  for (int m = 2; m<M; m+=3) {
    key += bruteforce(m, encoded);
    // Make sure we don't miss the deadline
    if ((m%10==0) && (clock()>19*CLOCKS_PER_SEC))
      break;
  }
  
  // Solve the first three characters using brute force
  key += bruteforce(0, encoded);
  // Solve the rest using the Markov chain
  for (int m=3; m<M; m++) 
    key += markovchain(key, encoded);
  */
  
  // pad our result out to be the right length
  while (key.length() < M)
    key += 'E';
  cerr << key << endl;

  return key;
}


int main(int argc, char **argv) {

  int N;           // number of encoded messages
  int M;           // length of each message
  cin >> N >> M;
   cerr << "N = " << N << ", M = " << M << endl;


  vector<string> messages(N);

  for(int i = 0; i<N; i++)
    cin >> messages[i];

  cout << OneTimePad::decrypt(messages) << endl;

  return 0;
}
