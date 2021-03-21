#include "LKH.h"

void CandidateWriteToFile()
{
    if (CandidateFiles > 0) {
        return;
    }

    FILE *fptr;
    Node *N;
    Candidate *NN;

    fptr = fopen(CandidateOutputFileName, "w");
    if (fptr == NULL) {
        eprintf("Error opening the file!");
        return;
    }

    N = FirstNode;
    do {
        if (N->CandidateSet)
            fprintf(fptr, "%d:", N->Id);
            for (NN = N->CandidateSet; NN->To; NN++)
                fprintf(fptr, "%d;", NN->To->Id);
            fprintf(fptr, "\n");
    }
    while ((N = N->Suc) != FirstNode);

    fclose(fptr);
}
