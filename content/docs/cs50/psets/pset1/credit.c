#include <stdio.h>
#include <cs50.h>

int cardLen(long creditcard);

int main(void)
{
    printf("Number: ");
    long creditcard = get_long_long();
    
    // Mastercard start with 51, 52, 53, 54, or 55, length: 16
    // American Express start with 34 or 37, length: 15
    // Visa numbers start with 4, length: 13 or 16
    // printf will be AMEX\n or MASTERCARD\n or VISA\n or INVALID\n

    int length = cardLen(creditcard);
    
    int index = 1;
    int first = 0;
    int second = 0;
    int current = 0;
    
    int amount = 0;
    long leftout = creditcard;

    do{
        int tempTens = 10;
        
        current = (int) (leftout % tempTens);
        leftout = (leftout - current) / tempTens;
        
        if(index == length) {
            first = current;
        } else if(index == length - 1) {
            second = current;
        }
        if(index % 2 != 0) {
            amount += current;
        } else {
            int tempMulti = current * 2;
            if(tempMulti >= 10) {
                tempMulti = tempMulti % 10 + (tempMulti - tempMulti % 10) / 10;
            }
            amount += tempMulti;    
        }
        // printf("index: %i, current: %i, amount: %i\n", index, current, amount);
        index ++;
    } while (index <= length);
    
    if(amount % 10 != 0) {
        printf("INVALID\n");
    } else {
        if(first == 5 && (second == 1 || second == 2 || second == 3 || second == 4 || second == 5) && length == 16) {
            printf("MASTERCARD\n");
        } else if(first == 3 && (second == 4 || second == 7) && length == 15) {
            printf("AMEX\n");
        } else if(first == 4 && (length == 13 || length == 16)) {    
            printf("VISA\n");
        } else {
            printf("INVALID\n");
        }
    }
    
}

int cardLen(long creditcard)
{
    int length = 0;
    do {
        length ++;
        creditcard /= 10;
    } while(creditcard >= 1);
    return length;
}