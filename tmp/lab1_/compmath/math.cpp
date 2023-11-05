#include <inttypes.h>
#include <stdio.h>

const uint64_t BASE = UINT64_MAX;
extern "C" {
    void bn_add(uint64_t* result, uint64_t* num1, uint64_t* num2, int size) {
        uint64_t carry = 0;
        //printf("Base is: %lu\n",BASE);
        for (int i=0;i<size;i++) {
            uint64_t tmp = num1[i] + num2[i] + carry;
            if (tmp < num1[i]) carry = 1;
            else carry = 0;
            //printf("Carry is: %lu; Tmp is: %lu\n",carry,tmp);
            result[i] = tmp; 
        } 
        if (carry != 0) result[size] = carry;
    }
    int bn_sub(uint64_t* result, uint64_t* num1, uint64_t* num2, int size){
        int borrow = 0;
        for (int i = 0; i < size; i++){
            //printf("Num1 %lu, num2 %lu, borrow %i\n",num1[i],num2[i],borrow);
            uint64_t tmp = num1[i] - num2[i] - borrow;
            //printf("Tmp is: %lu\n",tmp);
            if (tmp <= num1[i]) {
                result[i] = tmp;
                borrow = 0;
            } else if (tmp >= num1[i]){
                result[i] = (uint64_t)(tmp);
                //printf("I was here, res: %lu\n",(uint64_t)(tmp));
                borrow = 1;
            }
        }
        return borrow;
    }
    uint64_t hi(uint64_t x) {
        return x >> 32;
    }
    uint64_t lo(uint64_t x){
        return ((1ULL << 32) - 1) & x;
    }
    void mulStep(uint64_t a, uint64_t b, uint64_t* carry, uint64_t* result) {
        uint64_t s0, s1, s2, s3, x; 
        x  = lo(a) * lo(b);
        s0 = lo(x);
        x = hi(a) * lo(b) + hi(x);
        s1 = lo(x);
        s2 = hi(x);
        x = s1 + lo(a) * hi(b);
        s1 = lo(x);
        x = s2 + hi(a) * hi(b) + hi(x);
        s2 = lo(x);
        s3 = hi(x);
        uint64_t tmp = s1 << 32 | s0;
        // printf("tmp: %lu\n",tmp);
        *result = tmp + *carry;
        // printf("tmp: %lu\n",*result);
        *carry = s3 << 32 | s2;
        if (*result < tmp) {
            // printf("I waas here. %lu, %lu \n",tmp,*result);
            // printf("Carry %lu\n",*carry);
            *carry = *carry + 1;
        }
        // printf("Carry %lu\n",*carry);
        // printf("res: %lu\n",*result);
    }
    void mulScal(uint64_t* result, uint64_t* num1, uint64_t num2, int size){
        uint64_t carry = 0;
        for (int i = 0; i < size; i++) {
            // printf("carry before %lu\n",carry);
            uint64_t tmp;
            mulStep(num1[i],num2,&carry,&tmp);
            // carry = res[1];
            // uint64_t tmp = res[0];
            // printf("Carry outside: %lu, tmp outside: %lu\n",carry,tmp);
            result[i] = tmp;
            //carry = carry > 64;
        }
        result[size] = carry;
    }    
    void shiftLeft(uint64_t* number, int sT, int size) {
        for (int i = size-sT; i >= 0; i--){
            number[i+sT] = number[i];
        }
        for (int i = 0; i < sT; i++) {
            number[i] = 0;
        }
    }
    void bn_mul(uint64_t* result, uint64_t* num1, uint64_t* num2, int size){
        printf("%i",3/2);
        // printf("Cycle bn_mul\n");
        for (int i = 0;i < size;i++){
            uint64_t* tmp = new uint64_t[size*2]();
            mulScal(tmp,num1,num2[i],size);
            shiftLeft(tmp,i,size*2);
            bn_add(result,result,tmp,size*2);
        }
    }
    uint64_t* kMul(uint64_t* num1, uint64_t* num2, int size){

    }
}
