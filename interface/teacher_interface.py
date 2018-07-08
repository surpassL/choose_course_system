def teacher(adj,teacher_info,choose):
    if hasattr(adj, teacher_info[choose][1]):
        getattr(adj, teacher_info[choose][1])()
    else:
        print('没有该功能')