<%inherit file="jobinator:templates/app_layout.mako" />

<%def name="body()">
      <div class="row-fluid">
        <div class="span3">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Actions</li>
              % if request.user:
                <li><a href="${request.route_url('filter_add')}">Create a filter</a></li>
                <li><a href="${request.route_url('filter_list')}">Filters</a></li>
              % endif
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span9">
            ${next.content()}
        </div><!--/span-->
      </div><!--/row-->

</%def>

<%def name="layout()">-fluid</%def>

<%def name="content()"></%def>
