#include<iostream>
#include <cstring>
#include <cstdio>
#include <climits>
using namespace std;

#define r 5
#define c 7

int max1=-1;
int wasMax = 1;
int final[r][c];

int lastWrite = INT_MAX;     

bool safe(int x, int y){
   if (x < r && y < c && x >= 0 && y >= 0)
		return true;
  return false;
}

bool valid(int arr[r][c], int v[r][c], int x, int y){

    if(arr[x][y]=='#' || v[x][y])
         return false;
    return true;
}

int path(int arr[r][c],int v[r][c],int i, int j,int count){

   
    if( max1 < count ){                          // For limiting the recursion and finding largest path                       
    max1 = count;
    wasMax = 1;
    lastWrite = INT_MAX;
    for(int k=0;k<r;k++){
        for(int l=0;l<c;l++){
                final[k][l] = 0;              
        } 
    }
    }

 
    v[i][j]=1;                                    // Recursion for finding path

    if(safe(i+1,j) && valid(arr,v,i+1,j)){
    path(arr,v,i+1,j,count+1); 
    v[i+1][j] = 0;
    }

    if(safe(i,j+1) && valid(arr,v,i,j+1)){
    path(arr,v,i,j+1,count+1);
    v[i][j+1] = 0;
    }

    if(safe(i-1,j) && valid(arr,v,i-1,j)){
    path(arr,v,i-1,j,count+1);
    v[i-1][j] = 0;
    }

    if(safe(i,j-1) && valid(arr,v,i,j-1)){
        path(arr,v,i,j-1,count+1);  
        v[i][j-1] = 0;
    }
    

    if(wasMax && lastWrite > count){
         lastWrite = count;
         final[i][j]=count;
       }

    if(count == 1){
      wasMax = 0;
      lastWrite = INT_MAX;
    }

}


int main(){

freopen("Input.txt","r",stdin);  // Input File

freopen("Output.txt","w",stdout);  // Output File


int arr[r][c];                      // Input Array
int visit[r][c];                    // Visited Array

memset(visit,0,sizeof visit);
for(int i=0;i<r;i++){
	    for(int j=0;j<c;j++){
	        char ch;
	        cin>>ch;
	        arr[i][j] = ch;
	    }
}
     
for(int i=0;i<r;i++){
    for(int j=0;j<c;j++){

        if(arr[i][j]=='.'){
            path(arr,visit,i,j,1);
                visit[i][j] = 0;
        }        
    }     

}

        
for(int i=0;i<r;i++){
    for(int j=0;j<c;j++){
        if(final[i][j]==0 && arr[i][j]=='#')
            cout<<"#"<<" ";
        else if(final[i][j]==0 && arr[i][j=='.'])
            cout<<"."<<" ";
        else
            cout<<final[i][j]-1<<" ";
    }
    cout<<"\n";
}

}



// ##.##.#
// #..##.#
// #.#####
// #..####
// #######

// ##.##.#
// ##.#..#
// ####..#
// ##....#
// #######