int main() {
    int **niz = malloc(8);
    int i = 0;
    while(i <= 10) {
        *(niz+i/2) = i;
        i = i + 2;
    }
}