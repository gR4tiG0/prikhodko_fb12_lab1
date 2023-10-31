#include <inttypes.h>
#include <stdio.h>
#include <string.h>


extern "C" {
    void prArr(uint64_t* num, int size) {
        for (int i = 0; i<size;i++){
            printf("%lu ",num[i]);
        }
        printf("\n");
    }
    void bn_add(uint64_t* result, uint64_t* num1, uint64_t* num2, int size) {
        uint64_t carry = 0;
        // printf("add input\n");
        // prArr(num1,size);
        // prArr(num2,size);
        //printf("Base is: %lu\n",BASE);
        for (int i=0;i<size;i++) {
            uint64_t tmp = num1[i] + num2[i] + carry;
            if (tmp < num1[i]) carry = 1;
            else carry = 0;
            //printf("Carry is: %lu; Tmp is: %lu\n",carry,tmp);
            result[i] = tmp; 
        } 
        if (carry != 0) result[size] = carry;
        // printf("result from add\n");
        // prArr(result,size);
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
            //printf("Carry outside: %lu, tmp outside: %lu\n",carry,tmp);
            result[i] = tmp;
        }
        result[size] = carry;
    }    
    void shiftLeft(uint64_t* number, int sT, int size) {
        // for (int i = size - sT; i >= 0; i--) {
        //     *(number+i+sT) = *(number+i);
        // }
        memcpy(number+sT, number, (size - sT) * sizeof(uint64_t));
        for (int i = 0; i < sT; i++) {
            *(number+i) = 0;
        }
    }
    void mul(uint64_t* result, uint64_t* num1, uint64_t* num2, int size){
        for (int i = 0;i < size;i++){
            uint64_t* tmp = new uint64_t[size*2]();
            mulScal(tmp,num1,num2[i],size);
            shiftLeft(tmp,i,size*2);
            bn_add(result,result,tmp,size*2);
        }
    }
    void bn_kMul(uint64_t* result, uint64_t* num1, uint64_t* num2, int size){
        // printf("input\n");
        // prArr(num1,size);
        // prArr(num2,size);
        if (size == 1) {
            // mul(result,num1,num2,size);
            mulScal(result,num1,num2[0],size);
            // printf("returning\n");
            // prArr(result,size*2);
        } else {
            int m = size/2;
            int n = size - m;
            int tmpS = 2*(2*size + 2*n + 1);
            uint64_t* space = new uint64_t[tmpS]();
            uint64_t* a_l = space;
            uint64_t* b_l = space+n;
            // for (int i = 0; i<m;i++){
            //     *(a_l+i) = *(num1+i);
            //     *(b_l+i) = *(num2+i);
            // }
            memcpy(a_l, num1, m * sizeof(uint64_t));
            memcpy(b_l, num2, m * sizeof(uint64_t));
            uint64_t* a_h = num1+m;
            uint64_t* b_h = num2+m;
            uint64_t* z0 = space+2*n;
            uint64_t* z2 = result;
            bn_kMul(z0, a_h,b_h, n);
            bn_kMul(z2, a_l,b_l, m);
            // printf("space, n=%i,m=%i,size=%i\n",n,m,size);
            // prArr(space,tmpS);
            // printf("res\n");
            // prArr(result,size*2);
            // printf("z0\n");
            // prArr(z0,2*m);
            // printf("z1\n");
            // prArr(z2,2*n);
            uint64_t* sum_a = space+2*(size)+2*n;
            uint64_t* sum_b = space+2*size+3*n+1;

            bn_add(sum_a,a_l,a_h,n);
            bn_add(sum_b,b_l,b_h,n);

            // printf("ablh,m=%i, n=%i\n",m,n);
            // prArr(a_l,m);
            // prArr(b_l,m);
            // prArr(a_h,n);
            // prArr(b_h,n);
            // printf("space\n");
            // prArr(space,tmpS);
            // printf("suma,b,m=%i, n=%i\n",m,n);
            // prArr(sum_a,n+1);
            // prArr(sum_b,n+1);
            int sT = n+1;
            if (sum_a[n] == 0 && sum_b[n] == 0) sT--;
            // printf("sT: %i, n: %i\n",sT,n);
            //uint64_t* tmp = new uint64_t[(sT)*2]();
            uint64_t* z1 = space+2*(2*n+size+1);
            bn_kMul(z1,sum_a,sum_b,sT);
            
            // printf("space\n");
            // prArr(space,tmpS);

            bn_sub(z1,z1,z0,sT*2);

            // printf("space\n");
            // prArr(space,tmpS);

            bn_sub(z1,z1,z2,sT*2);

            // printf("space, n=%i,m=%i,size=%i\n",n,m,size);
            // prArr(space,tmpS);
            // printf("Before shifting\n");
            // prArr(z0,size*2);
            // prArr(z1,size*2);
            // prArr(z2,size*2);
            // printf("Shifting\n");

            shiftLeft(z1,m,size*2);

            // printf("space\n");
            // prArr(space,tmpS);
            // printf("res\n");
            // prArr(result,size*2);
            // printf("z1\n");
            // prArr(z1,size*2);

            bn_add(result,result,z1,size*2);

            // printf("res\n");
            // prArr(result,size*2);

            shiftLeft(z0,m*2,size*2);

            // printf("space\n");
            // prArr(space,tmpS);
            // printf("res\n");
            // prArr(result,size*2);
            // printf("z0\n");
            // prArr(z0,size*2);

            bn_add(result,z0,result,size*2);

            // printf("returtning res\n");
            // prArr(result,size*2);
            delete space;
        }
    }



    void bn_mul(uint64_t* result, uint64_t* num1, uint64_t* num2, int size){
        //printf("Cycle bn_mul\n");
        //uint64_t* tmp = new uint64_t[size*2]();
        bn_kMul(result, num1,num2,size);
        // for(int i = 0;i<size*2;i++){
        //     result[i] = tmp[i];
        // }
    }
}
