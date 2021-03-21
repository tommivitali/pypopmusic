#include "LKH.h"

void CandidatePrint()
{
    Node *N;
    Candidate *NN;

    N = FirstNode;
    do {
        if (N->CandidateSet)
            printf("Node %d: ", N->Id);
            for (NN = N->CandidateSet; NN->To; NN++)
                printf("%d ", NN->To->Id);
            printf("\n");
    }
    while ((N = N->Suc) != FirstNode);
}
