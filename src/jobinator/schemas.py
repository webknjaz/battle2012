import colander
import deform
from pyramid_deform import CSRFSchema

from jobinator import widgets


class UserFilterSchema(CSRFSchema):
    """ UserFilter form schema """

    name = colander.SchemaNode(colander.String())
    #description = colander.SchemaNode(colander.String())
    filter_details = colander.SchemaNode(colander.String(),
                                         widget = widgets.FilterDetailsWidget())


class UserFilterDelSchema(CSRFSchema):
    """ UserFilter form schema """
    pass

