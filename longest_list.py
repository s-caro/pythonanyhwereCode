
def longest_list(prof_t, prof_m, prof_all):

    n_prof_t = len(prof_t)
    n_prof_m = len(prof_m)

    n_prof_all = 0
    for i in prof_all:
        if i not in prof_t and i not in prof_m:
            n_prof_all = n_prof_all + 1
    return max(n_prof_m, n_prof_t, n_prof_all) + 1
