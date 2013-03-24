from webhelpers import paginate
from kibra.db.models import Entry, Tag
from kibra.db import DBObject, get_db_session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
import transaction
import re
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from wtforms.form import Form
import wtforms.validators as v
import wtforms.fields as f
from string import strip
from sqlalchemy.sql.expression import text, bindparam


class EntryForm (Form):
    url = f.TextField(validators=[], filters=[strip])
    title = f.TextField(validators=[], filters=[strip])
    tags = f.TextField(validators=[], filters=[])
    text = f.TextAreaField(validators=[], filters=[strip])
    

DEFAULT_TAG_NAME = 'totag'

filter_tags_re = re.compile(r'-?\w+', re.UNICODE)
tag_re = re.compile(r'\w+', re.UNICODE)

def _get_all_tags ():
    #TODO replace with trigger to count + delete not linked tags
    dbsession = get_db_session()
    tbl = DBObject.metadata.tables['entries__tags']
    entities_num_map = dict(dbsession.query(tbl.c.tag_id, func.count('*')).group_by(tbl.c.tag_id))
    return [(tag, entities_num_map.get(tag.id, 0)) for tag in Tag.q.order_by(Tag.name.asc())]

def show_list (request):
    current_page = int(request.GET.get('page', '1'))

    include_tags = set()
    exclude_tags = set()
    for cmd in filter_tags_re.findall(request.GET.get('filter', '')):
        if cmd.startswith('-'):
            exclude_tags.add(cmd[1:])
        else:
            include_tags.add(cmd)


    related_tags = {}


    q = Entry.q.order_by(Entry.id.desc())
    
    class ReturnEmpty (Exception):
        pass
    try:    #TODO yeah i know
        if include_tags:
            tags = Tag.q.filter(Tag.name.in_(include_tags)).all()
            if len(tags) != len(include_tags):
                raise ReturnEmpty
            for tag in tags:
                q = q.filter(Entry.tags.contains(tag))

            subq = '''
                SELECT et1.tag_id
                FROM entries__tags AS et
                    INNER JOIN entries__tags AS et1 ON et.entry_id = et1.entry_id AND et.tag_id = :tag_id
                WHERE et1.tag_id != :tag_id'''
            for tag in tags:
                related_tags[tag.name] = (Tag.q
                    .filter(Tag.id.in_(text(subq, bindparams = [bindparam('tag_id', tag.id)])))
                    .order_by(Tag.name)
                    .all())
        if exclude_tags:
            tags = Tag.q.filter(Tag.name.in_(exclude_tags)).all()
            if len(tags) != len(include_tags):
                raise ReturnEmpty
            for tag in Tag.q.filter(Tag.name.in_(exclude_tags)):
                q = q.filter(~ Entry.tags.contains(tag))
    except ReturnEmpty:
        q = []

    entries = paginate.Page(q, current_page, url=paginate.PageURL_WebOb(request), items_per_page=10)


    return {
        'entries': entries,
        'all_tags': _get_all_tags(),
        'related_tags': related_tags,
    }


def edit (request):
    dbsession = get_db_session()
    dbsession.expire_on_commit = False

    #TODO yeah form handling is very ugly. i'll solve it
    if 'id' in request.GET:
        id = int(request.GET['id'])
        if id:
            entry = Entry.q.get(id)
            if not entry:
                return HTTPNotFound()

            entry_url = entry.url
            entry_title = entry.title
            tag_names = '%s ' % ' '.join(tag.name for tag in entry.tags)
            entry_text = entry.text
        else:
            entry = None

            entry_url = ''
            entry_title = ''
            tag_names = ''
            entry_text = ''
    elif 'url' in request.GET:
        entry = Entry.q.filter_by(url = request.GET['url']).first()
        if entry:
            entry_url = entry.url
            entry_title = entry.title
            tag_names = '%s ' % ' '.join(tag.name for tag in entry.tags)
            entry_text = entry.text
        else:
            entry_url = request.GET['url']
            entry_title = request.GET.get('title') or request.GET['url']
            tag_names = ''
            entry_text = ''
    else:
        return HTTPNotFound()


    failed_form = None

    if request.method.lower() == 'post':
        form = EntryForm(request.POST)
        if form.validate():
            if not entry:
                entry = Entry()

            entry.url = form.url.data
            entry.title = form.title.data
            entry.text = form.text.data

            dbsession.add(entry)

#            try:
#                dbsession.flush()
#            except IntegrityError as e:
#                if 'duplicate key value violates unique constraint "entries_url_key"' in e.message:
#                    raise #TODO show error in form
#                else:
#                    raise

            #TODO this may cause unique violation, test it
            new_tags = []
            for tag_name in set(tag_re.findall(form.tags.data)) or [DEFAULT_TAG_NAME]:
                tag = Tag.q.filter_by(name = tag_name).first() or Tag(name = tag_name)
                new_tags.append(tag)
            entry.tags = new_tags
            
            transaction.commit()

            return HTTPFound(location = request.route_url('entries.edit', _query = dict(id = entry.id)))
        else:
            failed_form = form
            
            entry_url = request.POST['url']
            entry_title = request.POST['title']
            tag_names = request.POST['tags']
            entry_text = request.POST['text']
    
    return {
        'entry': entry,

        'entry_url': entry_url,
        'entry_title': entry_title,
        'tag_names': tag_names,
        'entry_text': entry_text,

        'failed_form': failed_form,

        'all_tags': _get_all_tags(),
    }


def delete (request):
    Entry.q.filter_by(id = int(request.matchdict['id'])).delete(synchronize_session = False)
    transaction.commit()

    return HTTPFound(location = request.GET.get('redirect_url') or request.route_url('entries.list'))

	
def rename_tag (request):
    old_name = request.POST['old'].strip()
    new_name = request.POST['new'].strip()

    if old_name and new_name and (old_name != DEFAULT_TAG_NAME) and (old_name != new_name):
        new_tag = Tag.q.filter_by(name = new_name).first()
        if new_tag:
            dbsession = get_db_session()
            tbl = DBObject.metadata.tables['entries__tags']
            
            old_tag = Tag.q.filter_by(name = old_name).one()
            dbsession.execute(tbl.update().where(tbl.c.tag_id == old_tag.id).values(tag_id = new_tag.id))
            dbsession.delete(old_tag)
        else:
            Tag.q.filter_by(name = old_name).update({Tag.name: new_name}, synchronize_session = False)

        transaction.commit()

    return 'ok'
