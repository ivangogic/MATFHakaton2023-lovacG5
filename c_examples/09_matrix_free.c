int main() {
    int n = 5;

    int **mat = malloc(n);

    int i = 0;
    while(i < n) {
        *(mat+i) = malloc(n);
        i = i + 1;
    }

    i = 1;
    while(i <= n) {
        free(*(mat+i));
        i = i + 1;
    }
    free(mat);
}
