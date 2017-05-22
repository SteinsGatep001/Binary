/**
0804B0C0  661BD75C 24825227 3F93B950 5BDD9E48  \..f'R.$P..?H..[
0804B0D0  4A61C1F8 71648B65 77359095 1A9C9C67  ..aJe.dq..5wg...
0804B0E0  016F8369 646571FD 5F74463D 0F865C51  i.o..qed=Ft_Q\..
0804B0F0  29EB1D0B 74DC6DBA 4F2C3858 735AC140  ...).m.tX8,O@.Zs
**/

int rand_numb[16];
int tmp_off = 0x0B;
v1 = mrand_n[tmp_off];
v2 = (tmp_off+15)&0x0F;
v3 = mrand_n[(tmp_off+13)&0x0F];
v4 = mrand_n[v2];	// v4 = mrand_n[(tmp_off+15)&0x0F]
v5 = mrand_n[tmp_off]<<16;
tmp_off = (tmp_off+15)&0x0F;
v6 = v3^v5^v1^(v3<<15); // mrand_n[(tmp_off+13)&0x0F] ^ mrand_n[tmp_off]<<16 ^ mrand_n[tmp_off]


