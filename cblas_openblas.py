import os

pardir = os.path.normpath(os.getcwd() + os.sep + os.pardir)

with open(pardir+"/data/"+'map.dat') as f:
    map_lines = f.readlines()

blas_dict = {}
for map_line in map_lines:
    if (map_line.__contains__('=')):
        lhs,rhs = map_line.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()
        # rhs = rhs.rstrip('\n')
        blas_dict[lhs] = rhs


with open(pardir+"/data/"+'cuda.cpp') as f:
    src_lines = f.readlines()

copy_src_lines = src_lines

header_inc_flag = 0
for i in range(len(src_lines)):
    src_lines[i] = src_lines[i].strip()
    src_line = src_lines[i]
    index_src = i

    # case 1
    if (src_line.find("#include") != -1):
        print "=================yes"
        for key in blas_dict.keys():
            if src_line.find(key) != -1:
                src_lines[i] = ""
                if header_inc_flag == 0:
                    src_lines[i] = blas_dict[key]
                    header_inc_flag = 1
    # src_lines[i] = src_lines[i].rstrip('\n')

    # case 2
    # elif (src_line.find("findCudaDevice") != -1) or src_line.find("cudagetvector") != -1) :
    else:
        for key in blas_dict.keys():
            if src_line.find(key) != -1 and blas_dict[key]=="Delete" :
                src_lines[i] = ""
            elif src_line.find(key) != -1 and blas_dict[key]=="add_map_h_d" :
                splt_line = src_line.split(",")
                if len(splt_line) > 4:
                    rhs = splt_line[2].strip()
                    lhs = splt_line[4].strip()
                    blas_dict[lhs] = rhs
                    src_lines[i] = ""
            elif src_line.find(key) != -1 and blas_dict[key].find("gemm") != -1 :
                print "======================Found Gemm"
                pos = src_line.find(key)
                splt_line = src_line.split(",")
                params = []
                if len(splt_line) == 14:
                    for j in range(len(splt_line)):
                        if j == 0:
                            tmp,splt_line[j] = splt_line[j].split("(",1)
                            splt_line[j] = splt_line[j].strip()
                        if j == 13:
                            splt_line[j],tmp = splt_line[j].split(")",1)
                            splt_line[j] = splt_line[j].strip()
                        params.append(splt_line[j].strip())
                    for k in range(len(params)):
                        if blas_dict.has_key(params[k]):
                            params[k] = blas_dict[params[k]]

                tmp = blas_dict[key]+str("(")

                for j in range(len(params)):
                    if j == 13:
                        tmp+=params[j]+");"
                    else:
                        tmp+=params[j]+", "

                src_lines[i] = tmp

    print src_lines[i]
print blas_dict
print src_lines

fl = open(pardir+"/data/openblas_output.cpp",'w')
# for src in src_lines:
fl.writelines("%s\n" % l for l in src_lines)
# fl.writelines(src_lines)
fl.close()


# cublasSgemm(   handle     , CUBLAS_OP_N   , CUBLAS_OP_N  , N , N , N , &alpha, d_A , N , d_B, N , &beta , d_C, N);
# cblas_dgemm ( CblasRowMajor, CblasNoTrans , CblasNoTrans , m , n , k , 1.0   , A   , k , B  , n , 0.0   , C  , n );

# TODO
# remove handle keyword, or for gemm param 0 --> directly use rowmajor