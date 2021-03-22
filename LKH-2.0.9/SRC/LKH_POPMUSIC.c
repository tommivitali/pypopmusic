#include "LKH.h"
#include "Genetic.h"

/*
 * This file contains the function to compute the candidate sets and write these to a file.
 */

double LKH_POPMUSIC(char *parameterFile) 
{
    double LastTime = GetTime();

    ParameterFileName = parameterFile;
    ReadParameters();

    int OldTraceLevel = TraceLevel;
    TraceLevel = 0;

    MaxMatrixDimension = 20000;
    MergeWithTour = Recombination == IPT ? MergeWithTourIPT :
        MergeWithTourGPX2;
    ReadProblem();

    AllocateStructures();

    TraceLevel = OldTraceLevel;
    CreateCandidateSet();

    CandidateWriteToFile();

    double TimeSpent = GetTime() - LastTime;
    if (TraceLevel >= 1)
        printff("Total execution time: %0.4f seconds", TimeSpent);
    return TimeSpent;
}