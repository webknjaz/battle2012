from jobinator.resources import UserFilterFactory


def includeme(config):
    """ Add routes to the config """

    config.add_route('index', '/')
    config.add_route('filter_add', '/filters/add')
    config.add_route('filter_edit', '/filters/{filter_pk}/edit',
                     factory=UserFilterFactory,
                     traverse="/{filter_pk}")
    config.add_route('filter_list', '/filters/')
    
    config.add_route('filter_del', '/filters/{filter_pk}/remove',
                     factory=UserFilterFactory,
                     traverse="/{filter_pk}")
    config.add_route('filter_view', '/filters/{filter_pk}',
                     factory=UserFilterFactory,
                     traverse="/{filter_pk}")
    
    config.add_jsonrpc_endpoint('filter', '/api/filter')
