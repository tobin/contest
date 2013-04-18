#include <stdio.h>

bool debug = false;

bool global_constraint(int n_chests, int n_keys, int key_count[], int key_req[], int **keys_inside) {
  int keys_available[n_keys];
  int keys_needed[n_keys];

  // add the keys that are in our possession
  for (int k=0; k<n_keys; k++) 
    keys_available[k] += key_count[k];

  // add the keys that are in each chest
  for (int c=0; c<n_chests; c++) 
    for (int k=0; k<n_keys; k++) 
      keys_available[k] += keys_inside[c][k];

  for (int k=0; k<n_keys; k++) {
    if (keys_needed[k] > keys_available[k]) {
      if (debug)
	printf("Need %d of key %d but only have %d.\n", keys_needed[k], k, keys_available[k]);
      return false;
    }
  }

  return true;
}


bool still_possible(int n_chests, bool opened[], int key_count[], int key_req[], int **keys_inside) {
  bool flag = true;

  int keys_available[n_keys];

  // add the keys that are in our possession
  for (int k=0; k<n_keys; k++) 
    keys_available[k] += key_count[k];

  while (flag) {
    flag = false;
    
    for (int c=0; c<n_chests; c++) {
      // check if it's already opened
      if (opened[c]) 
	continue;

      // check whether we can open the chest
      if (!keys_available[key_req[c]])
	continue;
      
      // open it without destroying the key
      for (int k=0; k<n_keys; k++) 
	keys_available[k] += keys_inside[c][k];
      opened[c] = true;
      flag = true; // there is still hope
      break;
    }
  }

  return chests.empty();
}

int solve(int n_chests, vector<int> key_count, int key_req[], multiset<int> keys_inside[]) {

  vector<bool> chest(n_chests);  // true=not yet opened, false=opened
  vector<int> solution;

  int chests_remaining = n_chests;

  if (!global_constraint(chests, keys, key_req, keys_inside) ||
      !still_possible(chests, keys, key_req, keys_inside)) {
    cout << "IMPOSSIBLE" << endl;
    return 0;
  }

  while (chests_remaining) {
    for (set<int>::iterator c=chests.begin(); c != chests.end(); c ++) {

      // Skip this chest if it's already been opened
      if (! *c) 
	continue;

      // Skip this chest if we can't open it
      int key = key_req[*c];
      if (key_count[key] == 0) {
	if (debug) 
	  cout << "Can't open chest " << chest + 1 << " because I don't have key " << key << endl;
	continue;
      }

      // Open the chest
      key_count[key] --;
      *c = false;  // set chest to opened

      // insert keys_inside into keys
      for (multiset<int>::iterator k = keys_inside[chest].begin(); k != keys_inside[chest].end(); *k ++) {
	key_count[*k] ++;
      }

      if (debug) {
	cout << "I have these keys:";
	for (auto k = key_count.begin(); k != key_count.end(); k++) 
	  for (int i=0; i<*k; i++)
	    cout << " " << *k;
	cout << endl;
      }

      // Test
      if (still_possible(chests, keys, key_req, keys_inside)) {
	chests = new_chests;    
	solution.push_back(chest + 1);
	break;
      }
      if (debug)
	cout << "Had to unopen chest " << chest + 1 << endl;
      // Rewind
      keys.insert(key);
      //chests.insert(*c);      
      // remove keys_inside from keys
      for (multiset<int>::iterator k = keys_inside[chest].begin(); k != keys_inside[chest].end(); *k ++) {
	keys.erase(keys.find(*k));
      }
    }
  }

  if (debug) 
    cout << "Solution: ";
  copy(solution.begin(), solution.end(),
       ostream_iterator<int>(cout, " "));
  cout << endl;
}


int main(int argc, char **argv) {
  int T;
  cin >> T;
  for (int t=0; t<T; t++) {
    cout << "Case #" << t+1 << ": ";
    if (debug) cout << endl;

    int K, N;
    cin >> K >> N;
    
    multiset<int> keys;
    for (int k=0; k<K; k++) {
      int temp;
      cin >> temp;
      keys.insert(temp);
    }
    if (debug) {
      cout << "I start with these keys: ";
      copy(keys.begin(), keys.end(),
	   ostream_iterator<int>(cout, " "));
      cout << endl;
    }

    int key_req[N];
    multiset<int> keys_inside[N];
    set<int> chests;

    for (int n=0; n<N; n++) {
      chests.insert(n);

      int Ti, Ki;
      cin >> Ti >> Ki;
      key_req[n] = Ti;
      for (int k=0; k<Ki; k++) {
	int temp;
	cin >> temp;
	keys_inside[n].insert(temp);
      }
      if (debug) {
	cout << "Chest " << n+1 << " needs key " << Ti << 
	  " and contains keys: ";
	copy(keys_inside[n].begin(), keys_inside[n].end(),
	     ostream_iterator<int>(cout, " "));
	cout << endl;
      }
    }
    
    solve(chests, keys, key_req, keys_inside);
  }

  return 0;
}
