from DBconnection import DBconnection
import functional_req as fr

def print_help():
    with open('help.txt', 'r') as f:
        print(f.read())

if __name__ == "__main__":
    print()
    print_help()

    dbms = DBconnection()
    while True:
        cmd = input('> ').strip()
        cmd_list = list(map(lambda s: s.strip(), cmd.split(' ')))
        operations = {
            'select': fr.select,
            'project': fr.project,
            'aggregate': fr.aggregate,
            'search': fr.search,
            'analysis': fr.analysis,
            'insert': fr.insert,
            'delete': fr.delete,
            'update': fr.update
        }
        operations_num = {
            1: fr.select, 2: fr.select, 3: fr.select, 4: fr.select,
            5: fr.project, 6: fr.project, 7: fr.project,
            8: fr.aggregate, 9: fr.aggregate, 10: fr.aggregate, 11: fr.aggregate, 12: fr.aggregate,
            13: fr.search, 14: fr.search, 15: fr.search,
            16: fr.analysis, 17: fr.analysis, 18: fr.analysis, 19: fr.analysis, 20: fr.analysis, 21: fr.analysis,
            22: fr.insert, 23: fr.insert, 24: fr.insert,
            25: fr.update, 26: fr.update, 27: fr.update,
            28: fr.delete, 29: fr.delete, 30: fr.delete
        }
        if cmd == 'q':
            break
        if cmd == 'h':
            print_help()
        elif cmd == '':
            continue
        elif cmd.isnumeric():
            if int(cmd) in operations_num:
                operations_num[int(cmd)](cmd_list, dbms, int(cmd))
            else:
                print(f"{cmd} : Invalid Command Number")
        elif len(cmd_list) and cmd_list[0].lower() in operations:
            operations[cmd_list[0].lower()](cmd_list, dbms)
        else:
            print(f"{cmd_list[0]} : Invalid Command")
    dbms.close()
