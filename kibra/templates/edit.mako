<%inherit file="/base.mako" />

<%block name="title">kibra: edit</%block>


<script type="text/javascript">
    var App = window.App || {};

    App.all_tags = [
        ${','.join("'%s'" % tag.name for tag, count in all_tags) |n}
    ];

    window.addEvent('domready', function () {
        var el = $('tags');

        App.filter_autosuggest = new App.Autosuggest(el, {
                debug: true
        });

        el.focus();
        el.setCaretPosition('end');
        
        $$('.j-confirm-delete').addEvent('click', function () {
            return confirm('are you sure?');
        });
        
        $$('form').addEvent('submit', function() {
            this.getElement('input[type=submit]').set('disabled',true);
        });
    });
</script>

<a href="${request.route_path('entries.list')}">list</a>

<h3>${'edit' if entry else 'create'} entry</h3>

<form action="${request.route_path('entries.edit', _query = dict(id = entry.id if entry else 0))}" method="post">
    %if failed_form:
        <div style="color: red;">errors:</div>
        %for field_name, errors in failed_form.errors:
            <div style="color: red;">${field_name}: ${', '.join(errors)}</div>
        %endfor
    %endif

    
    <label>url <input type="text" name="url" size="100" value="${entry_url}" autocomplete="off" /></label>

    <br />
    <label>title <input type="text" name="title" size="60" value="${entry_title}" /></label>

    <br />
    <label>tags <input type="text" id="tags" name="tags" size="40" value="${tag_names}" autocomplete="off" /></label>

    <br />
    <label>text <textarea name="text" cols="40" rows="10">${entry_text}</textarea></label>

    %if entry:
        <br />
        <a class="j-confirm-delete" href="${request.route_path('entries.delete', id = entry.id)}">
            <img src="${request.static_url('kibra:static/img/delete.png')}" alt="[delete]" title="delete" />
        </a>
    %endif


    <br />
    <input type="submit" value="save" /> <input type="reset" value="reset" />
</form>