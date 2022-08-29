#include <stdio.h>
#include <stdlib.h>
typedef char* string;
const string helpstring="gene FILENAME [-h] -l LENGTH=10 -w WIDTH=10\nUsage : Generate an empty level of any size";
int main(int argc, char *argv[]){
    int length=10,width=10;
    int clength,cwidth;
    int total;
    int i;
    const int charsize=sizeof(char);
    string result,filename,arg;
    /*Parse argv*/
    for (i=0;i<argc;i++){
        arg=argv[i];
        switch (arg[0]){
            case '-':
                switch (arg[1]){
                    case 'h':
                        printf(helpstring);
                        return 0;
                    case 'l':
                        length = atoi(argv[i+1]);
                        break;
                    case 'w':
                        width = atoi(argv[i+1]);
                        break;
                }
                break;
        }
    }
    /*Init result string*/
    filename=argv[1];
    clength = length*3;
    cwidth = width;
    total = clength*cwidth-1;
    result = (string)calloc(total+1,charsize);
    result[total]='\0';
    if (result == NULL){
        printf("calloc failed");
        return 0;
    }
    /*Add objects to string*/
    for (i=0;i<total;i++){
        if ((i%3)!=2){
            result[i] = '-';
        }else if ((i%clength)==(clength-1)){
            result[i] = '\n';
        }else{
            result[i] = ' ';
        }
    }
    /*Output to file*/
    FILE *file = fopen(filename,"w");
    if (file == NULL){
        printf("file write failed");
        return 0;
    }
    fprintf(file,result);
    fclose(file);
    free(result);
    printf("generation complete");
    return total;
}