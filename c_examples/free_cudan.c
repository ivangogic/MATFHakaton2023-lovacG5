int main() {
    int ***mat = malloc(1);
    *mat = malloc(3);
    *(*mat) = malloc(3);
    *(*mat+1) = malloc(3);
    *(*mat+2) = malloc(3);
}