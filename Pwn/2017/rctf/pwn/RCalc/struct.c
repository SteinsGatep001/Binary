

_manhea_addr    ->  manhea_addr
_roun_ptr       -> roun_ptr


// 保存res
struct manhea_addr
{
    u64 number;
    void *pt;       // 0x100
};

// 类似栈的方式存值
struct roun_ptr
{
    u64 number;
    void *pt;       // 0x320
}
