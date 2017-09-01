

## Reference

[Freebuf](http://bobao.360.cn/ctf/detail/178.html)

## checksec

```js
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
```

## struct

```C
struct orange
{
    int price;
    int color;
};

struct house
{
    struct *orange;
    char *name;
};
//*
```

## Vuln
