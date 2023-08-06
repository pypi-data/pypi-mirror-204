# List of eager operators, they execute immediately, e.g.,
# ``db.remove``.
#
# Operators **not** listed here are lazy. They will execute at a later
# time.
#
ops_eager = set((
    # list('operators');
    # ---
    'cancel',

    'consume',
    'create_array',
    'create_array_using',

    'delete',

    'help',

    'insert',

    'load_library',
    'load_module',

    'remove',
    'remove_versions',
    'rename',

    'save',

    'store',

    'sync',

    'unload_library',

    # list('macros');
    # ---
    'load',

    # load_library('accelerated_io_tools');
    # ---
    'aio_save',

    # load_library('bridge');
    # ---
    'xremove',
    'xsave',

    # load_library('dense_linear_algebra');
    # ---
    'mpi_init',

    # load_library('namespaces');
    # ---
    'add_user_to_role',
    'change_user',
    'create_namespace',
    'create_role',
    'create_user',
    'drop_namespace',
    'drop_role',
    'drop_user',
    'drop_user_from_role',
    'move_array_to_namespace',
    'set_namespace',
    'set_role_permissions',

    # load_library('system');
    # ---
    'add_instances',
    'remove_instances',
    'sync',
    'unregister_instances',

    ))

# List of operators with string arguments. The list is grouped by
# argument position. If an operator has multiple string arguments, it
# is listed multiple times. If an argument can be a string or something
# else, it is excluded from this list.
#
string_args = (
    # 1st argument
    set((
        # list('operators');
        # ---
        'cancel',
        'list',
        'load_library',
        'load_module',
        'unload_library',

        # load_library('accelerated_io_tools');
        # ---
        'split',

        # load_library('bridge');
        # ---
        'xremove',
        'xinput',
        'secure_xinput',

        # load_library('namespaces');
        # ---
        'add_user_to_role',
        'change_user',
        'create_namespace',
        'create_role',
        'create_user',
        'drop_namespace',
        'drop_role',
        'drop_user',
        'drop_user_from_role',
        'set_namespace',
        'set_role',
        'set_role_permissions',
        'show_users_in_role',
        'show_role_permissions',
    )),
    # 2nd argument
    set((
        # list('operators');
        # ---
        'input',
        'save',
        'show',

        # list('macros');
        # ---
        'load',

        # load_library('accelerated_io_tools');
        # ---
        'aio_save',
        'parse',
        'split',

        # load_library('bridge');
        # ---
        'xsave',

        # load_library('namespaces');
        # ---
        'add_user_to_role',
        'change_user',
        'create_user',
        'drop_user_from_role',
        'move_array_to_namespace',
    )),
    # 3rd argument
    set((
        # load_library('accelerated_io_tools');
        # ---
        'parse',
        'split',

        # load_library('namespaces');
        # ---
        'change_user',
        'set_role_permissions',
    )),
    # 4thd argument
    set((
        # list('operators');
        # ---
        'input',
        'load',
        'save',

        # load_library('accelerated_io_tools');
        # ---
        'parse',
        'split',

        # load_library('namespaces');
        # ---
        'set_role_permissions',
    )),
    # 5th argument
    set((
        # load_library('accelerated_io_tools');
        # ---
        'parse',
        'split',
    )),
    # 6th argument
    set((
        # load_library('accelerated_io_tools');
        # ---
        'parse',
        'split',
    )),
    # 7th argument
    set((
        # load_library('accelerated_io_tools');
        # ---
        'split',
    )),
    # 8th argument
    set((
    ))
)
