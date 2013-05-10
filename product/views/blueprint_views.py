from flask import Blueprint, request, render_template, redirect, url_for

from product.models import *


# blueprint experiments:
bookmarks = Blueprint('bookmarks', __name__, template_folder='templates')

@bookmarks.route('/bookmark/')
def list():
    bm = Bookmark.objects()
    return render_template('bookmarks/index.html', bm=bm)

@bookmarks.route('/bookmark/add/')
def add():
    url = request.args.get('url')
    if url:
        try:
            b = Bookmark.objects.get(url=url)
        except DoesNotExist, e:
            b = Bookmark(url=url, desc='a description')
            b.save()
    return redirect(url or url_for('bookmarks.list'))

@bookmarks.route('/bookmark/<pk>/delete/')
def delete(pk):
    try:
        bookmark = Bookmark.objects.get(id=pk)
        bookmark.delete()
    except DoesNotExist:
        pass
    return redirect(url_for('bookmarks.list'))

# end blueprint experiments
