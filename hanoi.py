import sys


def action(x, y, z, disks_dict, disks_star_dict):
    name = 'move-%s-from-%s-to-%s' %(disks_dict[x], disks_star_dict[y], disks_star_dict[z])
    pre = 'clear(%s) clear(%s) on(%s,%s) smaller(%s,%s)' %(disks_dict[x], disks_star_dict[z],
                                                           disks_dict[x], disks_star_dict[y],
                                                           disks_dict[x], disks_star_dict[z])
    add = 'on(%s,%s) clear(%s)' %(disks_dict[x], disks_star_dict[z], disks_star_dict[y])
    delete = 'clear(%s) on(%s,%s)' %(disks_star_dict[z], disks_dict[x], disks_star_dict[y])

    return {'Name' : name,
            'pre' : pre,
            'add' : add,
            'delete' : delete}

def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    "*** YOUR CODE HERE ***"

    # give numeric weight to the disks and pegs, so that it is easier to check conditions
    disks_dict = {weight: name for (weight, name) in enumerate(disks)}
    disks_star_dict = {weight: name for (weight, name) in enumerate(disks + pegs)}

    # propositions
    ## indicates if disk is empty
    clear = ['clear(%s)' % disks_star_dict[i] for i in disks_star_dict]

    ## indicates if disk d can be on disk b
    smaller = []
    on = []
    for d in disks_dict:
        for b in disks_star_dict:
            if d < b:
                smaller.append('smaller(%s,%s)' %(disks_dict[d], disks_star_dict[b]))
                on.append('on(%s,%s)' %(disks_dict[d], disks_star_dict[b]))

    props = clear + smaller + on  # TODO: this has to be written in file
    print(props)

    # actions
    actions = []
    for x in disks_dict:  # all real disks
        for y in disks_star_dict:  # can lay on other real disk, or on peg (virtual disk)
            for z in disks_star_dict:  # can be moved to other real disk, or to peg (virtual disk)
                if x < y and x < z and y!=z:  # disk x needs to be smaller than disks y and z, and y and z different
                    actions.append(action(x, y, z, disks_dict, disks_star_dict))

    print(actions)  # TODO: actions are now a list of dictionaries (see function action) needs to be written in file

    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    "*** YOUR CODE HERE ***"

    # give numeric weight to the disks and pegs, so that it is easier to check conditions
    disks_dict = {weight: name for (weight, name) in enumerate(disks)}
    disks_star_dict = {weight: name for (weight, name) in enumerate(disks + pegs)}

    # initial state
    ## stack the disks
    stack = []
    for d, b in zip(disks[:-1], disks[1:]):
        stack.append('on(%s,%s)' % (d, b))
    ## and locate at first peg
    on_i = stack + ['on(%s,%s)' %(disks[-1], pegs[0])]

    ## what is clear
    clear_i = ['clear(%s)' %disks[0]] + ['clear(%s)' %i for i in pegs[1:]]

    ## indicates if disk d can be on disk b
    smaller = []
    for d in disks_dict:
        for b in disks_star_dict:
            if d < b:
                smaller.append('smaller(%s,%s)' % (disks_dict[d], disks_star_dict[b]))

    initial_state = on_i + clear_i + smaller  # TODO: write this in problem file

    # goal state
    ## and stack at last peg
    on_g = stack + ['on(%s,%s)' % (disks[-1], pegs[-1])]

    ## what is clear, smalles disk and all pegs despite last
    clear_g = ['clear(%s)' % disks[0]] + ['clear(%s)' % i for i in pegs[:-1]]

    goal_state = on_g + clear_g + smaller  # TODO: write this in problem file

    print(initial_state)
    print(goal_state)
    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
