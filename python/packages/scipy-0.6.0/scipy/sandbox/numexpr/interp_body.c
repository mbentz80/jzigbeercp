{
#define VEC_LOOP(expr) for(j = 0; j < VECTOR_SIZE; j++) {       \
        expr;                                       \
    }
#define VEC_ARG1(expr)                          \
    BOUNDS_CHECK(store_in);                     \
    BOUNDS_CHECK(arg1);                         \
    {                                           \
        char *dest = params.mem[store_in];      \
        char *x1 = params.mem[arg1];            \
        intp sb1 = params.memsteps[arg1];       \
        intp si1 = sb1 / sizeof(long);          \
        intp sf1 = sb1 / sizeof(double);        \
        VEC_LOOP(expr);                         \
    } break
#define VEC_ARG2(expr)                          \
    BOUNDS_CHECK(store_in);                     \
    BOUNDS_CHECK(arg1);                         \
    BOUNDS_CHECK(arg2);                         \
    {                                           \
        char *dest = params.mem[store_in];      \
        char *x1 = params.mem[arg1];            \
        intp sb1 = params.memsteps[arg1];       \
        intp si1 = sb1 / sizeof(long);          \
        intp sf1 = sb1 / sizeof(double);        \
        char *x2 = params.mem[arg2];            \
        intp sb2 = params.memsteps[arg2];       \
        intp si2 = sb2 / sizeof(long);          \
        intp sf2 = sb2 / sizeof(double);        \
        intp s2 = params.memsteps[arg2];        \
        VEC_LOOP(expr);                         \
    } break

#define VEC_ARG3(expr)                          \
    BOUNDS_CHECK(store_in);                     \
    BOUNDS_CHECK(arg1);                         \
    BOUNDS_CHECK(arg2);                         \
    BOUNDS_CHECK(arg3);                         \
    {                                           \
        char *dest = params.mem[store_in];      \
        char *x1 = params.mem[arg1];            \
        intp sb1 = params.memsteps[arg1];       \
        intp si1 = sb1 / sizeof(long);          \
        intp sf1 = sb1 / sizeof(double);        \
        char *x2 = params.mem[arg2];            \
        intp s2 = params.memsteps[arg2];        \
        intp sb2 = params.memsteps[arg2];       \
        intp si2 = sb2 / sizeof(long);          \
        intp sf2 = sb2 / sizeof(double);        \
        char *x3 = params.mem[arg3];            \
        intp s3 = params.memsteps[arg3];        \
        intp sb3 = params.memsteps[arg3];       \
        intp si3 = sb3 / sizeof(long);          \
        intp sf3 = sb3 / sizeof(double);        \
        VEC_LOOP(expr);                         \
    } break


    unsigned int pc, j, k, r;
    /* set up pointers to next block of inputs and outputs */
    params.mem[0] = params.output + index * params.memsteps[0];
    for (r = 0; r < params.n_inputs; r++) {
        struct index_data id = params.index_data[r+1];
        if (id.count) {
            params.mem[1+r] = params.inputs[r];
            for (j = 0; j < VECTOR_SIZE; j++) {
                unsigned int flatindex = 0;
                for (k = 0; k < id.count; k ++)
                    flatindex += id.strides[k] * id.index[k];
                memcpy(params.mem[1+r]+ (j*id.size), id.buffer + flatindex, id.size);
                k = id.count - 1;
                id.index[k] += 1;
                if (id.index[k] >= id.shape[k])
                    while (id.index[k] >= id.shape[k]) {
                        id.index[k] -= id.shape[k];
                        if (k < 1) break;
                        id.index[k-1] += 1;
                        k -= 1;
                    }
            }
        } else {
            params.mem[1+r] = params.inputs[r] + index * params.memsteps[1+r];
        }
    }
    for (pc = 0; pc < params.prog_len; pc += 4) {
        unsigned char op = params.program[pc];
        unsigned int store_in = params.program[pc+1];
        unsigned int arg1 = params.program[pc+2];
        unsigned int arg2 = params.program[pc+3];
        #define      arg3   params.program[pc+5]
        #define store_index params.index_data[store_in]
        
       /* WARNING: From now on, only do references to params.mem[arg[123]]
         & params.memsteps[arg[123]] inside the VEC_ARG[123] macros,
          or you will risk accessing invalid addresses.  */
        
        #define reduce_ptr  (dest + flat_index(&store_index, j))
        #define i_reduce    *(long *)reduce_ptr
        #define f_reduce    *(double *)reduce_ptr
        #define cr_reduce   *(double *)ptr
        #define ci_reduce   *((double *)ptr+1)
        #define b_dest ((char *)dest)[j]
        #define i_dest ((long *)dest)[j]
        #define f_dest ((double *)dest)[j]
        #define cr_dest ((double *)dest)[2*j]
        #define ci_dest ((double *)dest)[2*j+1]
        #define b1    ((char   *)x1)[j*sb1]
        #define i1    ((long   *)x1)[j*si1]
        #define f1    ((double *)x1)[j*sf1]
        #define c1r   ((double *)x1)[j*sf1]
        #define c1i   ((double *)x1)[j*sf1+1]
        #define b2    ((char   *)x2)[j*sb2]
        #define i2    ((long   *)x2)[j*si2]
        #define f2    ((double *)x2)[j*sf2]
        #define c2r   ((double *)x2)[j*sf2]
        #define c2i   ((double *)x2)[j*sf2+1]
        #define b3    ((char   *)x3)[j*sb3]
        #define i3    ((long   *)x3)[j*si3]
        #define f3    ((double *)x3)[j*sf3]
        #define c3r   ((double *)x3)[j*sf3]
        #define c3i   ((double *)x3)[j*sf3+1]

        double fa, fb;
        cdouble ca, cb;
        char *ptr;

        switch (op) {

        case OP_NOOP: break;

        case OP_COPY_BB: VEC_ARG1(b_dest = b1);
        case OP_COPY_II: VEC_ARG1(i_dest = i1);
        case OP_COPY_FF: VEC_ARG1(f_dest = f1);
        case OP_COPY_CC: VEC_ARG1(cr_dest = c1r;
                                  ci_dest = c1i);

        case OP_INVERT_BB: VEC_ARG1(b_dest = !b1);

        case OP_AND_BBB: VEC_ARG2(b_dest = b1 && b2);
        case OP_OR_BBB: VEC_ARG2(b_dest = b1 || b2);

        case OP_GT_BII: VEC_ARG2(b_dest = (i1 > i2) ? 1 : 0);
        case OP_GE_BII: VEC_ARG2(b_dest = (i1 >= i2) ? 1 : 0);
        case OP_EQ_BII: VEC_ARG2(b_dest = (i1 == i2) ? 1 : 0);
        case OP_NE_BII: VEC_ARG2(b_dest = (i1 != i2) ? 1 : 0);

        case OP_GT_BFF: VEC_ARG2(b_dest = (f1 > f2) ? 1 : 0);
        case OP_GE_BFF: VEC_ARG2(b_dest = (f1 >= f2) ? 1 : 0);
        case OP_EQ_BFF: VEC_ARG2(b_dest = (f1 == f2) ? 1 : 0);
        case OP_NE_BFF: VEC_ARG2(b_dest = (f1 != f2) ? 1 : 0);

        case OP_CAST_IB: VEC_ARG1(i_dest = (long)b1);
        case OP_ONES_LIKE_II: VEC_ARG1(i_dest = 1);
        case OP_NEG_II: VEC_ARG1(i_dest = -i1);

        case OP_ADD_III: VEC_ARG2(i_dest = i1 + i2);
        case OP_SUB_III: VEC_ARG2(i_dest = i1 - i2);
        case OP_MUL_III: VEC_ARG2(i_dest = i1 * i2);
        case OP_DIV_III: VEC_ARG2(i_dest = i1 / i2);
        case OP_POW_III: VEC_ARG2(i_dest = (i2 < 0) ? (1 / i1) : (long)pow(i1, i2));
        case OP_MOD_III: VEC_ARG2(i_dest = i1 % i2);

        case OP_WHERE_IFII: VEC_ARG3(i_dest = f1 ? i2 : i3);

        case OP_CAST_FB: VEC_ARG1(f_dest = (long)b1);
        case OP_CAST_FI: VEC_ARG1(f_dest = (double)(i1));
        case OP_ONES_LIKE_FF: VEC_ARG1(f_dest = 1.0);
        case OP_NEG_FF: VEC_ARG1(f_dest = -f1);

        case OP_ADD_FFF: VEC_ARG2(f_dest = f1 + f2);
        case OP_SUB_FFF: VEC_ARG2(f_dest = f1 - f2);
        case OP_MUL_FFF: VEC_ARG2(f_dest = f1 * f2);
        case OP_DIV_FFF: VEC_ARG2(f_dest = f1 / f2);
        case OP_POW_FFF: VEC_ARG2(f_dest = pow(f1, f2));
        case OP_MOD_FFF: VEC_ARG2(f_dest = f1 - floor(f1/f2) * f2);

        case OP_SIN_FF: VEC_ARG1(f_dest = sin(f1));
        case OP_COS_FF: VEC_ARG1(f_dest = cos(f1));
        case OP_TAN_FF: VEC_ARG1(f_dest = tan(f1));
        case OP_SQRT_FF: VEC_ARG1(f_dest = sqrt(f1));
        case OP_ARCTAN2_FFF: VEC_ARG2(f_dest = atan2(f1, f2));

        case OP_WHERE_FFFF: VEC_ARG3(f_dest = f1 ? f2 : f3);

        case OP_FUNC_FF: VEC_ARG1(f_dest = functions_f[arg2](f1));
        case OP_FUNC_FFF: VEC_ARG2(f_dest = functions_ff[arg3](f1, f2));

        case OP_CAST_CB: VEC_ARG1(cr_dest = (double)b1;
                                  ci_dest = 0);
        case OP_CAST_CI: VEC_ARG1(cr_dest = (double)(i1);
                                  ci_dest = 0);
        case OP_CAST_CF: VEC_ARG1(cr_dest = f1;
                                  ci_dest = 0);
        case OP_ONES_LIKE_CC: VEC_ARG1(cr_dest = 1;
                                  ci_dest = 0);
        case OP_NEG_CC: VEC_ARG1(cr_dest = -c1r;
                                 ci_dest = -c1i);

        case OP_ADD_CCC: VEC_ARG2(cr_dest = c1r + c2r;
                                  ci_dest = c1i + c2i);
        case OP_SUB_CCC: VEC_ARG2(cr_dest = c1r - c2r;
                                  ci_dest = c1i - c2i);
        case OP_MUL_CCC: VEC_ARG2(fa = c1r*c2r - c1i*c2i;
                                  ci_dest = c1r*c2i + c1i*c2r;
                                  cr_dest = fa);
        case OP_DIV_CCC: VEC_ARG2(fa = c2r*c2r + c2i*c2i;
                                  fb = (c1r*c2r + c1i*c2i) / fa;
                                  ci_dest = (c1i*c2r - c1r*c2i) / fa;
                                  cr_dest = fb);

        case OP_EQ_BCC: VEC_ARG2(b_dest = (c1r == c2r && c1i == c2i) ? 1 : 0);
        case OP_NE_BCC: VEC_ARG2(b_dest = (c1r != c2r || c1i != c2i) ? 1 : 0);

        case OP_WHERE_CFCC: VEC_ARG3(cr_dest = f1 ? c2r : c3r;
                                     ci_dest = f1 ? c2i : c3i);
        case OP_FUNC_CC: VEC_ARG1(ca.real = c1r;
                                  ca.imag = c1i;
                                  functions_cc[arg2](&ca, &ca);
                                  cr_dest = ca.real;
                                  ci_dest = ca.imag);
        case OP_FUNC_CCC: VEC_ARG2(ca.real = c1r;
                                   ca.imag = c1i;
                                   cb.real = c2r;
                                   cb.imag = c2i;
                                   functions_ccc[arg3](&ca, &cb, &ca);
                                   cr_dest = ca.real;
                                   ci_dest = ca.imag);

        case OP_REAL_FC: VEC_ARG1(f_dest = c1r);
        case OP_IMAG_FC: VEC_ARG1(f_dest = c1i);
        case OP_COMPLEX_CFF: VEC_ARG2(cr_dest = f1;
                                      ci_dest = f2);

        case OP_SUM_IIN: VEC_ARG1(i_reduce += i1);
        case OP_SUM_FFN: VEC_ARG1(f_reduce += f1);
        case OP_SUM_CCN: VEC_ARG1(ptr = reduce_ptr;
                                  cr_reduce += c1r;
                                  ci_reduce += c1i);

        case OP_PROD_IIN: VEC_ARG1(i_reduce *= i1);
        case OP_PROD_FFN: VEC_ARG1(f_reduce *= f1);
        case OP_PROD_CCN: VEC_ARG1(ptr = reduce_ptr;
                                   fa = cr_reduce*c1r - ci_reduce*c1i;
                                   ci_reduce = cr_reduce*c1i + ci_reduce*c1r;
                                   cr_reduce = fa);

        default:
            *pc_error = pc;
            return -3;
            break;
        }
    }

#undef VEC_LOOP
#undef VEC_ARG1
#undef VEC_ARG2
#undef VEC_ARG3

#undef b_dest
#undef i_dest
#undef f_dest
#undef cr_dest
#undef ci_dest
#undef b1
#undef i1
#undef f1
#undef c1r
#undef c1i
#undef b2
#undef i2
#undef f2
#undef c2r
#undef c2i
#undef b3
#undef i3
#undef f3
#undef c3r
#undef c3i
}
