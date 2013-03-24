<%inherit file="/base.mako" />
<%namespace name="util" file="/util.mako" />

<%block name="title">kibra: list</%block>


<style type="text/css">
    a img {border: none;}
    a {
        color: #000;
        text-decoration: none;
        border-bottom: 1px dashed #000;
    }
    a:hover {opacity: 0.7}


    .j-add-filter-exclude {
        color: #777;
    }
    .j-add-filter-exclude:hover {
        text-decoration: line-through;
        cursor: pointer;
    }
</style>

<script type="text/javascript">
    var App = window.App || {};

    App.all_tags = [
        ${','.join("'%s'" % tag.name for tag, count in all_tags) |n}
    ];
    App.url_rename_tag = '${request.route_path('entries.rename_tag')}';

    window.addEvent('domready', function () {
        var el = $('filter');
        if (el) {
            App.filter_autosuggest = new App.Autosuggest(el, {
                    debug: true
            });

            el.focus();
            el.setCaretPosition('end');
        }


        $$('.j-rename-tag').addEvent('click', function () {
            var old = this.get('oldname')
            var ret = prompt('new tag name:', old);
            if (ret) ret = ret.trim();
            if (ret && (old != ret)) {
                new Request({
                    url: App.url_rename_tag,
                    noCache: true,

                    onSuccess: function (responseText) {
                        if (responseText == 'ok') {
                            location.reload(true);
                        } else {
                            alert('failed to rename tag: ' + responseText);
                        }
                    },

                    onFailure: function (xhr) {
                        alert(['server responsed error:', xhr.status, xhr.statusText].join(' '));
                    }
                })
                .post({old: old, 'new': ret})
            }

            return false;
        });

        $$('.j-add-filter-exclude').addEvent('click', function () {
            $('filter').set('value', ($('filter').get('value').trim() + ' -' + this.get('text')).trim());
            $('tags-filter-submit').click();
        });

        $$('.j-confirm-delete').addEvent('click', function () {
            return confirm('are you sure?');
        });
    });
</script>

<div>
    <form action="${request.route_path('entries.list')}" method="get">
        <label>
            tag filter
            <%
                filter_value = request.GET.get('filter', "").strip()
                if filter_value:
                    filter_value += " "
            %>
            <input id="filter" name="filter" type="text" value="${filter_value}" size="50" autocomplete="off" />
        </label>
        <input id="tags-filter-submit" type="submit" value="find entries" />
    </form>
</div>

%if related_tags:
    <div style="margin: 1em 0 1em 0;">
        related tags:
        %for tag_name, tags in related_tags.items():
            <div style="margin-left: 1.5em;">
                %if len(related_tags) > 1:
                    ${tag_name}:
                %endif
                ${', '.join(t.name for t in tags)}
            </div>
        %endfor
    </div>
%endif

<a href="${request.route_path('entries.edit', _query = dict(id = 0))}">create new</a>

<div>
    %if entries:
         <ul>
            %for entry in entries:
                <li>
                    <a href="${request.route_path('entries.edit', _query = dict(id = entry.id))}">
                        <img src="${request.static_url('kibra:static/img/edit.png')}" alt="[edit]" title="edit" />
                    </a>
                    <a class="j-confirm-delete" href="${request.route_path('entries.delete', id = entry.id, _query = dict(redirect_url = request.url))}">
                        <img src="${request.static_url('kibra:static/img/delete.png')}" alt="[delete]" title="delete" />
                    </a>
                    &nbsp;

                    %if entry.url:
                        <a href="${entry.url}">${entry.title or '(untitled)'}</a>
                    %else:
                        ${entry.title or '(untitled)'}
                    %endif

                    %if entry.tags:
                        <span style="margin-left: .5em;">
                            <%util:compact sep=', '>
                                %for tag in entry.tags:
                                    <span class="j-add-filter-exclude">${tag.name}</span>
                                %endfor
                            </%util:compact>
                        </span>
                    %endif
                </li>
            %endfor
         </ul>

        <div>
            %if entries.page_count > 1:
                pages:
                ${entries.pager()}
            %endif
        </div>
    %else:
        nothing found
    %endif
</div>


<div style="margin-top: 1em; font-size: 80%;">
    %if all_tags:
        tags:
        <%util:compact sep=', '>
            %for tag, count in all_tags:
                <a href="#" class="j-rename-tag" oldname="${tag.name}" ><img src="${request.static_url('kibra:static/img/edit.png')}" alt="[rename]" title="rename" /></a>\
                ${tag.name}<span style="color: #bbb;">(${count})</span>
            %endfor
        </%util:compact>
    %else:
        no tags
    %endif
</div>