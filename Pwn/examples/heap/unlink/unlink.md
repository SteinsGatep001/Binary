## struct bins

```C
struct malloc_chunk {
    INTERNAL_SIZE_T prev_size;
    INTERNAL_SIZE_T size;
    struct malloc_chunk * fd;
    struct malloc_chunk * bk;
};
```

## unlink

```C
/* Take a chunk off a bin list */
#define unlink(P, BK, FD) { \
    FD = P->fd; \
    BK = P->bk; \
    if (__builtin_expect (FD->bk != P || BK->fd != P, 0)) \
        malloc_printerr (check_action, "corrupted double-linked list", P); \
    else { \
        FD->bk = BK; \
        BK->fd = FD; \
        if (!in_smallbin_range (P->size) \
        && __builtin_expect (P->fd_nextsize != NULL, 0)) { \
            assert (P->fd_nextsize->bk_nextsize == P); \
            assert (P->bk_nextsize->fd_nextsize == P); \
            if (FD->fd_nextsize == NULL)
            {
                if (P->fd_nextsize == P) \
                    FD->fd_nextsize = FD->bk_nextsize = FD; \
                else { \
                    FD->fd_nextsize = P->fd_nextsize; \
                    FD->bk_nextsize = P->bk_nextsize; \
                    P->fd_nextsize->bk_nextsize = FD; \
                    P->bk_nextsize->fd_nextsize = FD; \
                } \
            } else { \
                P->fd_nextsize->bk_nextsize = P->bk_nextsize; \
                P->bk_nextsize->fd_nextsize = P->fd_nextsize; \
            } \
        } \
    } \
}
```

## result

64bit
```C
FD = fake_fd = target_addr - 0x18
BK = fake_bk = target_addr - 0x10
//then
FD + 0x18 = BK = target_addr - 0x10
BK + 0x10 = FD = target_addr - 0x18
// thus
*target_addr = target_addr - 0x18
```

32bit
```C
FD = fake_fd = target_addr - 0x0c
BK = fake_bk = target_addr - 0x08
//then
FD + 0x18 = BK = target_addr - 0x08
BK + 0x10 = FD = target_addr - 0x0c
// thus
*target_addr = target_addr - 0x0c
```
