#include <inttypes.h>
#include <stdio.h>

const uint64_t BASE = UINT64_MAX;
extern "C" {
    void prArr(uint64_t* num, int size) {
        for (int i = 0; i<size;i++){
            printf("%lu ",num[i]);
        }
        printf("\n");
    }
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
        printf("In sub\n");
        prArr(result,size);
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
        for (int i = size-sT; i >= 0; i--){
            number[i+sT] = number[i];
        }
        for (int i = 0; i < sT; i++) {
            number[i] = 0;
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
    uint64_t* bn_kMul(uint64_t* num1, uint64_t* num2, int size){
        if (size == 1) {
            uint64_t* result = new uint64_t[size*2]();
            mul(result,num1,num2,size);
            return result;
        } else {
            int m = size/2;
            int n = size - m;
            uint64_t* a_l = new uint64_t[n+1]();
            uint64_t* b_l = new uint64_t[n+1]();
            uint64_t* a_h = new uint64_t[n+1]();
            uint64_t* b_h = new uint64_t[n+1]();

            for (int i = 0; i < m; i++){
                a_l[i] = num1[i];
                b_l[i] = num2[i];
            }
            for (int i = m; i < size; i++) {
                a_h[i-m] = num1[i];
                b_h[i-m] = num2[i];
            }
            printf("ablh,m=%i, n=%i\n",m,n);
            prArr(a_l,n+1);
            prArr(b_l,n+1);
            prArr(a_h,n+1);
            prArr(b_h,n+1);
            // uint64_t* z2 = new uint64_t[m*2]();
            // uint64_t* z0 = new uint64_t[n*2]();
            uint64_t* z0 = bn_kMul(a_h,b_h,n);
            uint64_t* z2 = bn_kMul(a_l,b_l,m);
            uint64_t* sum_a = new uint64_t[n+1]();
            uint64_t* sum_b = new uint64_t[n+1]();
            bn_add(sum_a,a_l,a_h,n+1);
            bn_add(sum_b,b_l,b_h,n+1);
            printf("suma,b,m=%i, n=%i\n",m,n);
            prArr(sum_a,n+1);
            prArr(sum_b,n+1);
            int sT = n+1;
            if (sum_a[n] == 0 && sum_b[n] == 0) sT = n;
            printf("sT: %i, n: %i\n",sT,n);
            //uint64_t* tmp = new uint64_t[(sT)*2]();
            uint64_t* sub = new uint64_t[(sT)*2]();
            uint64_t* z1 = new uint64_t[(sT)*2]();
            uint64_t* z0_s = new uint64_t[(sT)*2]();
            uint64_t* z2_s = new uint64_t[(sT)*2]();
            uint64_t* tmp = bn_kMul(sum_a,sum_b,sT);
            prArr(tmp,sT*2);
            for (int i = 0; i < sT*2; i++){
                if (i < m*2)
                    z2_s[i] = z2[i];
                else z2_s[i] = 0;
                printf("%lu ",z2_s[i]);
            }
            printf("\n");
            for (int i = 0; i < sT*2; i++){
                if (i < n*2)
                    z0_s[i] = z0[i];
                else z0_s[i] = 0;
                printf("%i:%i:%i:%lu ",n*2,sT*2,i,z0_s[i]);
            }
            printf("\n");

            printf("z0\n");
            prArr(z0,sT*2);
            printf("z2\n");
            prArr(z2,sT*2);
            printf("tmp\n");
            prArr(tmp,sT*2);
            bn_sub(sub,tmp,z0_s,sT*2);
            printf("sub\n");
            prArr(sub,sT*2);
            bn_sub(z1,sub,z2_s,sT*2);
            printf("z1\n");
            prArr(z1,sT*2);
            uint64_t* f2 = new uint64_t[size*2]();
            uint64_t* f1 = new uint64_t[size*2]();
            uint64_t* f0 = new uint64_t[size*2]();
            for (int i = 0; i < sT*2; i++){
                f2[i] = z2_s[i];
                f1[i] = z1[i];
                f0[i] = z0_s[i];
            }
            printf("Before shifting\n");
            prArr(f0,size*2);
            prArr(f1,size*2);
            prArr(f2,size*2);
            printf("Shifting\n");
            shiftLeft(f0,m*2,size*2);
            shiftLeft(f1,m,size*2);
            prArr(f0,size*2);
            prArr(f1,size*2);
            prArr(f2,size*2);
            uint64_t* res = new uint64_t[size*2]();
            uint64_t* sum = new uint64_t[size*2]();
            bn_add(sum,f0,f1,size*2);
            bn_add(res,sum,f2,size*2);
            return res;
        }
    }

    void bn_mul(uint64_t* result, uint64_t* num1, uint64_t* num2, int size){
        //printf("Cycle bn_mul\n");
        uint64_t* tmp = new uint64_t[size*2]();
        tmp = bn_kMul(num1,num2,size);
        for(int i = 0;i<size*2;i++){
            result[i] = tmp[i];
        }
        printf("res, final\n");
        for (int i = 0;i<size*2;i++) {
            printf("%lu ",result[i]);
        }
        printf("\n");
    }
}
