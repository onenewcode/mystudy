#include<stdio.h>

int main(){

int a=59,b;

printf("猜猜这个数是几？\n");

while(a!=b){

scanf("%d",&b);

if(b>a){

printf("猜大了\n");

}else if(b<a){

printf("猜小了\n");

}else{

printf("猜对了\n"); 

break;

}

}

return 0;

}