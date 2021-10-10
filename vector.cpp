#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */   
    int n, q;
    cin>>n>>q;
    vector<int> A[n];
    for(int i =0; i<n; i++){
        int k;
        cin>>k;
        for(int j=0; j<k; j++){
            int val;
            cin>>val;
            A[i].push_back(val);
        }


    }
    for(int i =0; i<q; i++){
    int a,b;
    cin>>a>>b;
    cout<<A[a][b];
    }
    return 0;
}