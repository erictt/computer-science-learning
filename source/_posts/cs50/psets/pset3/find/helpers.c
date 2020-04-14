/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if(value > values[n-1] || value < values[0]) {
        return false;
    }
    
    int low = 0;
    int high = n - 1;
    while(low <= high)
    {
        int middle = (int) (high + low)/2;
        if(value == values[middle]) {
            return true;
        } else if(value < values[middle]) {
            high = middle - 1;
        } else if(value > values[middle]) {
            low = middle + 1;
        }
    }
    
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // Bubble Sort
    // for(int i = 0; i < n - 1; i++) 
    // {
    //     int swapFlag = 0;
    //     for(int j = 1; j < n; j++)
    //     {
    //         if(values[j-1] > values[j]) {
    //             int temp = values[j-1];
    //             values[j-1] = values[j];
    //             values[j] = temp;
    //             swapFlag = 1;
    //         }
    //     }
    //     if(swapFlag == 0) return;
    // }
    
    // Selection Sort
    // for(int i = 0; i < n - 1; i++)
    // {
    //     for(int j = i+1; j < n; j++)
    //     {
    //         if(values[i] > values[j]) {
    //             int temp = values[i];
    //             values[i] = values[j];
    //             values[j] = temp;
    //         }
    //     }
    // }

    // Insert Sort
    for(int i = 0; i < n - 1; i++)
    {
        for(int j = i+1; j < n; j++)
        {
            if(values[i] > values[j]) {
                int temp = values[i];
                values[i] = values[j];
                values[j] = temp;
            }
        }
    }

    return;
}
