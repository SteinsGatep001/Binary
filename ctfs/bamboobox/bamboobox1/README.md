## func
1. show

2. add
```C
box_t[i].name = malloc(size);
read(0, box_t[i].name, size);
num++;
```
3. change
```C
size = input;
rd_bytes = read(0, box_t[i].name, size);
box_t[i].name[rd_bytes] = 0;
```
4. remove
```C
free(box_t[i].name);
box_t[i].name = 0;
box_t[i].size = 0;
```

## struct

```C
struct box_t
{
    int size;
    int ?;
    char* name_ptr;
};
```

## exp

用unlink修改指针，覆盖函数指针到magic函数即可得到falg
