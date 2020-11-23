#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/rbtree.h>
#include <linux/slab.h> // for kmalloc
#include <linux/ktime.h>
#include <linux/time.h>

struct my_node {
    struct rb_node node;
    int key;
    int value;
};
void my_insert(struct rb_root *root, struct my_node *data){
    
    struct rb_node **new = &(root->rb_node), *parent = NULL;
    /* Figure out where to put new node */
    while (*new) {
        struct my_node *this = container_of(*new, struct my_node, node);

        parent = *new;
        if ((data->key < 0))
            new = &((*new)->rb_left);
        else
            new = &((*new)->rb_right);
    }

    /* Add new node and rebalance tree. */
    rb_link_node(&data->node, parent, new);
    rb_insert_color(&data->node, root);

    return;
}

void RB_example(int num)
{
    ktime_t start, end, delta;
    struct rb_root root_node = RB_ROOT;
    struct my_node *new_node;

    int i;
    /* rb_node create and insert */
    printk("---- %d items in linux Red-Black Tree ---- \n", num);
    // Add nodes
    start = ktime_get();
    for(i=-(num/2);i<(num/2);i++){
        new_node = kmalloc(sizeof(struct my_node),GFP_KERNEL);
        new_node->value = i*10;
        new_node->key = i;
        my_insert(&root_node, new_node);
    }
    end = ktime_get();
    delta = ktime_sub(end, start);
    printk("ADD %d elements into red-black tree, %lld nano-seconds\n", num, delta);

    /* rb_tree traversal using iterator */
    // Search nodes
    struct rb_node *iter_node;
    
    start = ktime_get();
    for (iter_node = rb_first(&root_node); iter_node; iter_node = rb_next(iter_node)){
        // printk("(key,value)=(%d.%d)\n", rb_entry(iter_node, struct my_node, node)->key, rb_entry(iter_node, struct my_node, node)->value);
    }
    end = ktime_get();
    delta = ktime_sub(end, start);
    printk("Search %d elements into red-black tree, %lld nano-seconds\n", num, delta);

    // Delete nodes
    /* rb_tree delete node */
    start = ktime_get();
    for (iter_node = rb_first(&root_node); iter_node; iter_node = rb_next(iter_node)){
        rb_erase(iter_node, &root_node);
        // kfree(iter_node);
    }
    end = ktime_get();
    delta = ktime_sub(end, start);
    printk("Delete %d elements into red-black tree, %lld nano-seconds\n\n", num, delta); 
    
    /* check whether all nodes are erased */
    for (iter_node = rb_first(&root_node); iter_node; iter_node = rb_next(iter_node)){
        printk("(key,value)=(%d.%d)\n", rb_entry(iter_node, struct my_node, node)->key, rb_entry(iter_node, struct my_node, node)->value);
    }
}

int __init hello_module_init(void)
{
    
    printk("module init\n");
    int j;
    for(j = 1000; j<1000000; j*=10){
        RB_example(j);
    }
    
    return 0;
}
void __exit hello_module_cleanup(void)
{
    printk("Bye Module\n");
}


module_init(hello_module_init);
module_exit(hello_module_cleanup);
MODULE_LICENSE("GPL");