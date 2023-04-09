int main() {
    int n = 5;

    int **mat = malloc(n);

    int i = 0;
    while(i < n) {
        *(mat+i) = malloc(n);
        i = i + 1;
    }
}