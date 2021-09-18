from boxbox.utils import Registrar

def BaseName1_a1_b1():
    pass

def BaseName1_a2_b1():
    pass

def BaseName1_a1_b2():
    pass

def BaseName1_a2_b2():
    pass

def BaseName1_a3_b2():
    pass

def BaseName1_a3():
    pass

def test_empty_options():
    test = Registrar('test')
    print('name: ', test.name)
    print('pattern: ', test._pattern)
    print('options: ', test._options)
    print('start uid: ', test.uid)

    test.register_module(module=BaseName1_a1_b1)
    print('registering uid: ', test.uid)
    test.register_module(module=BaseName1_a2_b1)
    print('registering uid: ', test.uid)
    test.register_module(module=BaseName1_a1_b2)
    print('registering uid: ', test.uid)
    test.register_module(module=BaseName1_a2_b2)
    print('registering uid: ', test.uid)

    print('module_infos:')
    print(test._module_infos)
    print('len: ', len(test))
    print('key contain: ', 'BaseName1_a1_b1' in test)
    print('module contain: ', BaseName1_a1_b1 in test)
    print('not contain: ', 'BaseName1_a3_b2' in test, BaseName1_a3_b2 in test)

    item, infos = test['BaseName1_a1_b1']
    print('getitem item: ', item)
    print('getitem infos: ', infos)

    query = test.query(base_name='BaseName1_a1_b1')
    print('query str: ', query)
    query = test.query(base_name=['BaseName1_a1_b1', 'BaseName1_a1_b2'])
    print('query str: ', query)


def test_options():
    test = Registrar('test', options=dict(a=['a1', 'a2'], b=['b1', 'b2']))
    print('name: ', test.name)
    print('pattern: ', test._pattern)
    print('options: ', test._options)
    print('start uid: ', test.uid)

    test.register_module(module=BaseName1_a1_b1)
    print('registering uid: ', test.uid)
    test.register_module(module=BaseName1_a2_b1)
    print('registering uid: ', test.uid)
    test.register_module(module=BaseName1_a1_b2)
    print('registering uid: ', test.uid)
    test.register_module(module=BaseName1_a2_b2)
    print('registering uid: ', test.uid)
    # wrong pattern register
    # invlid options
    # test.register_module(module=BaseName1_a3_b2)
    # invlid options
    test.register_module(module=BaseName1_a3)

    print('module_infos:')
    print(test._module_infos)
    print('len: ', len(test))
    print('key contain: ', 'BaseName1_a1_b1' in test)
    print('module contain: ', BaseName1_a1_b1 in test)
    print('not contain: ', 'BaseName1_a3_b2' in test, BaseName1_a3_b2 in test)

    item, infos = test['BaseName1_a1_b1']
    print('getitem item: ', item)
    print('getitem infos: ', infos)

    query = test.query(base_name='BaseName1_a1_b1')
    print('query str: ', query)
    query = test.query(base_name=['BaseName1_a1_b1', 'BaseName1_a1_b2'])
    print('query str: ', query)


if __name__ == '__main__':
    test_options()
