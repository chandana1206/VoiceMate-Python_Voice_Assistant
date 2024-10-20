#include <stdio.h>
#define max 5
int queue[max];
int front=0, rear=-1;

int isFull(){
    if(rear==max-1){
        return 1;
    }
    else{
        return 0;
    }
}

int isEmpty(){
    if(front>rear){
        return 1;
    }
    else{
        return 0;
    }
}

void append(int element){
    if(isFull()){
        printf("Queue if full");
    }
    else{
        rear++;
        queue[rear]=element;
    }
}

int serve(){
    int delElement;
    if(isEmpty()){
        printf("Queue if empty");
    }
    else{
        delElement=queue[front];
        front++;
        return(delElement);
    }
}

void display(){
    int i;
    if(isEmpty()){
        printf("Queue if empty");
    }
    else{
        for(i=front; i<=rear;i++){
            printf("%d\t",queue[i]);
        }
    }
}

int main(){
    int choice, item;

    while(1){
        printf("1.Append, 2.Serve, 3.Display, 4.Exit");
        scanf("%d", &choice);
        switch(choice){
            case1:printf("Enter data iten:");
            scanf("%d", &item);
            append(item);
            break;
            case2:item=serve();
            printf("Deleted element is %d",item);
            break;
            case3:display();
            break;
        }
    }
}