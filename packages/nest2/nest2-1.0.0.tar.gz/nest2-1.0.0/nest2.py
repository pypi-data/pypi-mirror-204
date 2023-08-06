def print_htq(the_list, indent=False, level=0, fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_htq(each_item, indent, level+1, fh)
        else:
            if indent:
                for tab_num in range(level):
                    print("\t", end='', file=fh)
            print(each_item, file=fh)
