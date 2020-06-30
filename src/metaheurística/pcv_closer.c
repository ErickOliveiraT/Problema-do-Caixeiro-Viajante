#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define TRUE 1
#define FALSE 0

// Matriz de adjacência
typedef struct Matriz {
    int qnt;
    int** elementos;
} matriz;

// Nodo
typedef struct Nodo {
    int indice;
    int valor;
} nodo;

void carregaArquivo(matriz*, char*); // Lê um arquivo para carregar uma matriz de adjacência
int calcCusto(matriz, int*); // Calcula o custo de um caminho
void resolver(matriz, int*); // Calcula o caminho
void imprimeCaminho(int, int*); // Imprime um caminho
void imprimeMatriz(matriz); // Imprime uma matriz

int main(int argc, char *argv[]) {
    int i;
    matriz m;

    carregaArquivo(&m, "../../instances/10_01_25.txt");
    //imprimeMatriz(m);

    int *caminho = malloc((m.qnt + 1) * sizeof(int)); // Inicializando um caminho
    resolver(m, caminho);

    //Mostrando resultados
    printf("Resultado:\n\n");
    printf("Metaheuristica: Vizinho mais proximo\n\n");
    printf("Caminho: ");
    imprimeCaminho(m.qnt + 1, caminho);
    int custo = calcCusto(m, caminho);
    printf("Custo total: %d", custo);
}

void resolver(matriz m, int* caminho) {
    int *inserido = malloc(m.qnt * sizeof(int)); // Vetor de flags para indicar se um elemento foi inserido no caminho
    int i, j;

    // Marca todos os elementos como não inseridos
    for(i = 0; i < m.qnt; i++)  inserido[i] = FALSE; 
    //Insere a primeira cidade
    caminho[0] = 0;
    inserido[0] = TRUE;

    // Construindo o caminho
    for(i = 0; i < m.qnt; i++) {
        int aux = INT_MAX; // Armazena o menor custo atual ao comparar com os vizinhos
        int selected = 0;
        for(j = 0; j < m.qnt; j++) {
            //Marca elemento como possível selecionado caso seu custo seja menor que dos outros vizinhos e ainda não faça parte do caminho
            if(!inserido[j] && aux > m.elementos[i][j]) {
                selected = j;
                aux = m.elementos[i][j];
            }
        }
        // Insere o vizinho não selecionado mais próximo ao caminho
        caminho[i + 1] = selected;
        inserido[selected] = TRUE;
    }
    caminho[m.qnt] = 0; // Volta para a cidade inicial
    free(inserido);
}

void carregaArquivo(matriz* m, char* arq) {
    FILE* pto_arq = fopen(arq, "r");
    int i, j;

    fscanf(pto_arq, "%d\n", &m->qnt);
    m->elementos = malloc(m->qnt * sizeof(int*));
    
    for(i = 0; i < m->qnt; i++) {
        m->elementos[i] = malloc(m->qnt * sizeof(int));
        for(j = 0; j < m->qnt; j++) {
            fscanf(pto_arq, "%d ", &m->elementos[i][j]);
        }
    }
    fclose(pto_arq);
}

int calcCusto(matriz m, int* caminho) {
    int i, custo = 0;
    for(i = 0; i < m.qnt; i++) custo += m.elementos[caminho[i]][caminho[i + 1]];
    return custo;
}

void imprimeMatriz(matriz m) {
    int i, j;
    for(i = 0; i < m.qnt; i++) {
        for(j = 0; j < m.qnt; j++) printf("%d ", m.elementos[i][j]);
        printf("\n");
    }
}

void imprimeCaminho(int n, int* caminho) {
    int i;  
    for(i = 0; i < n; i++) printf("%d ", caminho[i]);
    printf("\n");
}