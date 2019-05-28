import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')

    # give numeric weight to the disks and pegs, so that it is easier to check conditions
    disks_dict = {weight: name for (weight, name) in enumerate(disks)}
    disks_star_dict = {weight: name for (weight, name) in enumerate(disks + pegs)}

    domain_str = 'Propositions:\n'

    ## indicates if disk is empty
    for i in disks_star_dict:
        domain_str += 'clear({}) '.format(disks_star_dict[i])

    ## indicates if disk d can be on disk b
    for d_id, d_str in disks_dict.items():
        for b_id, b_str in disks_star_dict.items():
            if d_id < b_id:
                domain_str += 'smaller({0},{1}) on({0},{1}) '.format(d_str, b_str)

    domain_str += '\nActions:\n'
    for x_id, x_str in disks_dict.items():  # all real disks
        for y_id, y_str in disks_star_dict.items():  # can lay on other real disk, or on peg (virtual disk)
            for z_id, z_str in disks_star_dict.items():  # can be moved to other real disk, or to peg (virtual disk)
                if x_id < y_id and x_id < z_id and y_id != z_id:  # disk x needs to be smaller than disks y and z, and y and z different
                    domain_str += 'Name: move-{0}-from-{1}-to-{2}\n' \
                                  'pre: clear({0}) clear({2}) on({0},{1}) smaller({0},{2})\n' \
                                  'add: on({0},{2}) clear({1})\n' \
                                  'delete: clear({2}) on({0},{1})\n'.format(x_str, y_str, z_str)

    domain_file.write(domain_str)
    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file

    disks_dict = {weight: name for (weight, name) in enumerate(disks)}
    disks_star_dict = {weight: name for (weight, name) in enumerate(disks + pegs)}

    init_state = 'Initial state: '
    goal_state = 'Goal state: '
    for d_id, d_str in disks_dict.items():
        for b_id, b_str in disks_star_dict.items():
            if d_id < b_id:
                init_state += 'smaller({0},{1}) '.format(d_str, b_str)

    for i in range(len(disks)-1):
        init_state += 'on({},{}) '.format(disks[i], disks[i+1])
        goal_state += 'on({},{}) '.format(disks[i], disks[i+1])

    init_state += 'on(d_{}, p_{}) clear(d_0) '.format(n_ - 1, 0)
    goal_state += 'on(d_{}, p_{}) '.format(n_ - 1, m_ - 1)

    for i in range(1, len(pegs)):
        init_state += 'clear({}) '.format(pegs[i])

    problem_file.write(init_state + '\n' + goal_state)
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
