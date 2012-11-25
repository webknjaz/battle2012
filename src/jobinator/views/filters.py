from pyramid.view import view_config
from jobinator.schemas import UserFilterSchema, UserFilterDelSchema
from horus.forms import SubmitForm
from horus.resources import RootFactory
import deform
from pyramid.httpexceptions import HTTPFound
from jobinator.models import DBSession, UserFilter, _, FACT_LIST, FactData, ScrapedData
from pyramid.i18n import get_locale_name
from pyramid_rpc.jsonrpc import jsonrpc_method

from pkg_resources import resource_filename
from deform.template import ZPTRendererFactory

import webhelpers.paginate as paginate
from sqlalchemy.orm import joinedload


dir = resource_filename('jobinator', 'templates/')
renderer = ZPTRendererFactory((dir,))


def i18n_aware(func):

    def wrapper(request, *kv, **kw):
        get_locale_name(request)
        return func(request, *kv, **kw)

    return wrapper

@view_config(route_name='filter_add',
             #permission='filter_add',
             renderer='jobinator:templates/filter_add.mako')
@view_config(route_name='filter_edit',
             #permission='filter_edit',
             renderer='jobinator:templates/filter_edit.mako')
@i18n_aware
def filter_add(request):
    """ UserFilter add/edit view """

    schema = UserFilterSchema()
    schema = schema.bind(request=request)
    form = SubmitForm(schema)
    form.children[-1].renderer = renderer

    success_message = isinstance(request.context, RootFactory) \
        and _(u'The filter was created') \
        or _(u'The filter was updated')

    if request.method == 'GET':
        if isinstance(request.context, RootFactory):
            return dict(form=form)
        else:
            return dict(form=form,
                        appstruct=request.context.__json__())
    else:
        try:
            controls = request.POST.items()
            captured = form.validate(controls)
        except deform.ValidationFailure, e:
            return dict(form=e, errors=e.error.children)

        if isinstance(request.context, RootFactory):
            filter = UserFilter(user=request.user, name=captured['name'], filter_details=captured['filter_details'])
        else:
            filter = request.context
            filter.name = captured['name']
            filter.filter_details = captured['filter_details']

        DBSession.add(filter)

        request.session.flash(success_message, 'success')

        return HTTPFound(
            location=request.route_url('filter_list')
        )


@view_config(route_name='filter_list',
             #permission='filter_list',
             renderer='jobinator:templates/filter_list.mako')
def filter_list(request):
    """ Userilter list view """

    return dict(items=UserFilter.get_all(request).filter(UserFilter.user == request.user))


@view_config(route_name='filter_del',
             #permission='filter_del',
             renderer='jobinator:templates/filter_del.mako')
def filter_del(request):
    """ UserFilter del view """

    schema = UserFilterDelSchema()
    schema = schema.bind(request=request)
    form = SubmitForm(schema)

    success_message = isinstance(request.context, RootFactory) \
        and _(u'The filter has been removed')

    if request.method == 'GET':
        return dict(form=form,
                        appstruct=request.context.__json__())
    else:
        try:
            controls = request.POST.items()
            captured = form.validate(controls)
        except deform.ValidationFailure, e:
            return dict(form=e, errors=e.error.children)

        filter = request.context

        DBSession.delete(filter)

        request.session.flash(success_message, 'success')

        return HTTPFound(
            location=request.route_url('filter_list')
        )


@view_config(route_name='filter_view',
             #permission='filter_view',
             renderer='jobinator:templates/filter_view.mako')
def filter_view(request):
    """ List of jobs """

    current_page = int(request.params.get('page', 0))
    q = (FactData.get_all(request).filter(UserFilter.get_by_pk(request, request.context.pk).build_query())
                                                .join(ScrapedData))
    page_url = paginate.PageURL_WebOb(request)
    records = paginate.Page(q, current_page, url=page_url)
    return dict(filter=request.context.name, page = records)


def operators_by_type(type):

    OPERATORS_BY_TYPE = {'Boolean':     ['IsNull',
                                         'NotNull'],

                         'Integer':     [#'Equal',
                                         #  'NotEqual',
                                         #  'LessThan',
                                           'LessOrEqual',
                                          # 'GreaterThan',
                                           'GreaterOrEqual',
                                           'IsNull',
                                           'NotNull',
                                           #'InList',
                                           #'NotInList',
                                           #'Between',
                                           #'NotBetween',
                                           #'InSubQuery'
                                           ]

                         }
    return OPERATORS_BY_TYPE.get(type.__name__, OPERATORS_BY_TYPE.values()[0])


@jsonrpc_method(endpoint='filter')
def get_model(request):
    res = {'operators': [{'caption': 'is equal to',
   'displayFormat': '{expr1} [[is equal to]] {expr2}',
   'exprType': 'Unknown',
   'id': 'Equal',
   'paramCount': 2,
   'valueKind': 'Scalar'},
  {'caption': 'is not equal to',
   'displayFormat': '{expr1} [[is not equal to]] {expr2}',
   'exprType': 'Unknown',
   'id': 'NotEqual',
   'paramCount': 2,
   'valueKind': 'Scalar'},
  {'caption': 'is less than',
   'displayFormat': '{expr1} [[is less than]] {expr2}',
   'exprType': 'Unknown',
   'id': 'LessThan',
   'paramCount': 2,
   'valueKind': 'Scalar'},
  {'caption': 'is less than or equal to',
   'displayFormat': '{expr1} [[is less than or equal to]] {expr2}',
   'exprType': 'Unknown',
   'id': 'LessOrEqual',
   'paramCount': 2,
   'valueKind': 'Scalar'},
  {'caption': 'is greater than',
   'displayFormat': '{expr1} [[is greater than]] {expr2}',
   'exprType': 'Unknown',
   'id': 'GreaterThan',
   'paramCount': 2,
   'valueKind': 'Scalar'},
  {'caption': 'is greater than or equal to',
   'displayFormat': '{expr1} [[is greater than or equal to]] {expr2}',
   'exprType': 'Unknown',
   'id': 'GreaterOrEqual',
   'paramCount': 2,
   'valueKind': 'Scalar'},
  {'caption': 'not present',
   'displayFormat': '{expr1} [[not present]] ',
   'exprType': 'Unknown',
   'id': 'IsNull',
   'paramCount': 1,
   'valueKind': 'Scalar'},
  {'caption': 'present',
   'displayFormat': '{expr1} [[present]] ',
   'exprType': 'Unknown',
   'id': 'NotNull',
   'paramCount': 1,
   'valueKind': 'Scalar'},
  {'caption': 'is in list',
   'displayFormat': '{expr1} [[is in list]] {expr2}',
   'exprType': 'Unknown',
   'id': 'InList',
   'paramCount': 2,
   'valueKind': 'List'},
  {'caption': 'is not in list',
   'displayFormat': '{expr1} [[is not in list]] {expr2}',
   'exprType': 'Unknown',
   'id': 'NotInList',
   'paramCount': 2,
   'valueKind': 'List'},
  {'caption': 'contains',
   'defaultEditor': {'id': 'Text value editor',
    'restype': 'String',
    'type': 'EDIT',
    'value': {'text': ''}},
   'displayFormat': '{expr1} [[contains]] {expr2}',
   'exprType': 'Unknown',
   'id': 'Contains',
   'paramCount': 2,
   'valueKind': 'Scalar'},
  {'caption': 'does not contain',
   'defaultEditor': {'id': 'Text value editor',
    'restype': 'String',
    'type': 'EDIT',
    'value': {'text': ''}},
   'displayFormat': '{expr1} [[does not contain]] {expr2}',
   'exprType': 'Unknown',
   'id': 'NotContains',
   'paramCount': 2,
   'valueKind': 'Scalar'},
  {'caption': 'is between',
   'displayFormat': '{expr1} [[is between]] {expr2} and {expr3}',
   'exprType': 'Unknown',
   'id': 'Between',
   'paramCount': 3,
   'valueKind': 'Scalar'},
  {'caption': 'is not between',
   'displayFormat': '{expr1} [[is not between]] {expr2} and {expr3}',
   'exprType': 'Unknown',
   'id': 'NotBetween',
   'paramCount': 3,
   'valueKind': 'Scalar'}],
 'rootEntity': {'UIC': True,
  'UIR': True,
  'UIS': True,
  'caption': None,
  'name': None,
  'subEntities': [
   {'UIC': True,
    'UIR': True,
    'UIS': True,
    'attributes': [
      {'UIC': True,
      'UIR': True,
      'UIS': True,
      'caption': fact,
      'dataType': factType.__name__,
      'description': '',
       'id': id,
      'operators': operators_by_type(factType),
      'size': 0} for (id, (fact, factType, default)) in enumerate(FACT_LIST)
     ],
    'caption': 'Facts',
    'name': 'Facts'},
                  ]}}
    return res
