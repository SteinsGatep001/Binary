
struct gun_func_list
{
    void shoot();
    void reload();
    void info();
};

struct gun
{
    void *gun_func_list;   //
    char *name;//
    int n_max;  // 弹夹容量
    int n_left;
};

struct biugun
{
    function gun_biu;
    0;
    15;
    15;
};

struct bangun
{
    function gun_bang;
    0;
    30;
    30;
};


56629D1C

5662BFD0
