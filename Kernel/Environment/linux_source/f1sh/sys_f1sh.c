#include <linux/kernel.h>
#define F1SH_DEBUG 1
asmlinkage long sys_f1sh(int arg0)
{
#if F1SH_DEBUG
    printk("syscall arg %d",arg0);
    printk("\n23333333\n");
#endif
    return ((long)arg0);
}
