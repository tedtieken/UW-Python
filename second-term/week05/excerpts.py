# urls.py

    url(r'^seriously-who-puts-something-like-this-on-a-dev-server/thats-a-bad-hack/books/$', 'misc.views.week05', name="week05"),    
    url(r'^seriously-who-puts-something-like-this-on-a-dev-server/thats-a-bad-hack/books/(?P<book_id>\w+)', 'misc.views.week05', name="week05_sub"),
    
    
# misc.views.py 
def week05(request, book_id = None):
    from bookdb import BookDB
    new_db = BookDB()
    if book_id == None:
        book_list = new_db.titles()
        #raise book_list
    else:
        try:
            book = new_db.title_info(book_id)
        except:
            book = None
        
    return render_to_response('week05.html', locals(), context_instance=RequestContext(request))
    
# week05.html
{% extends "base.html" %}

{% block title %}Book Database!{% endblock %}


{% block body %}
<div class="container">
<br />
<div class="span-24">
{% if book_list %}
    <h1> OMFG, A LIST OF BOOKS!</h1>
    <ul>
    {% for book in book_list %}
        <li><a href="{% url week05 %}{{book.id}}/">{{book.title}}</a><br /></li>
    {% empty %}
        <li>No Books, arg</li>
    {% endfor %}
    </ul>
{% else %}
    {% if book %}
    <h1> ZORG, A BOOK!</h1>
    <table>
        <tr>
            <td class="span-3">Title</td>
            <td>{{book.title}}</td>
        </tr>
        <tr>
            <td>Author</td>
            <td>{{book.author}}</td>
        </tr>
        <tr>
            <td>Publisher</td>
            <td>{{book.publisher}}</td>
        </tr>
        <tr>
            <td>ISBN</td>
            <td>{{book.isbn}}</td>
        </tr>
    </table>
    {% else %}
    <h1>NO BOOK FOUND</h1>
    <p>Off color remark also not found</p>
    {% endif %}

{% endif %}
    <hr>
    <a href="{% url week05 %}">Back to book list</a>
</div>
</div>
{% endblock %}