from django.shortcuts import render
from django.http import HttpResponse
from agora.models import Decision
from datetime import datetime

def index(request,
          template_name="index.html"):
    in_progress = Decision.objects.filter(closed_at__gt = datetime.now())
    closed = Decision.objects.filter(closed_at__lt = datetime.now())
    return render(request, template_name,
        {
            'in_progress' : in_progress,
            'closed' : closed,
        })

def about(request,
		  template_name="about.html"):
	return render(request, template_name)

def rdf_2(request, format="xml"):
    from rdflib.graph import Graph
    from rdflib import Literal, BNode, Namespace, URIRef
    from rdflib import RDF
    from django.contrib.auth.models import User

    g = Graph()
    data = """@prefix lt: 
<http://ns.lateral-thoughts.com/lt/0.1/> .

<http://data.lateral-thoughts.com/members/person#f.biville> a lt:Person;
    lt:email "f.biville@gmail.com" ."""

    # Bind a few prefix, namespace pairs.
    g.bind("lt", "http://ns.lateral-thoughts.com/lt/0.1/")

    # Create a namespace object for the Friend of a friend namespace.
    LT = Namespace("http://ns.lateral-thoughts.com/lt/0.1/")

    # Add triples using store's add method.
    for user in User.objects.all():
        person = URIRef("http://data.lateral-thoughts.com/members/person#%s" % (user.username))
        g.add((person, RDF.type, LT["Person"]))
        g.add((person, LT["nick"], Literal(user.username)))
        g.add((person, LT["firstname"], Literal(user.first_name)))
        g.add((person, LT["lastname"], Literal(user.last_name)))
        g.add((person, LT["name"], Literal("%s %s" % (user.first_name, user.last_name))))

    g.parse(data=data, format="n3")
    return HttpResponse(g.serialize(format=format))

def rdf(request, format="json-ld"):
    from rdflib.graph import Graph
    from rdflib import Literal, BNode, Namespace, URIRef
    from rdflib import RDF
    from django.contrib.auth.models import User

    g = Graph()
    data = """@prefix lt: 
<urn:lt:onto:> .

<urn:lt:members:f.biville> a lt:Person;
    lt:email "f.biville@gmail.com" ."""

    # Bind a few prefix, namespace pairs.
    g.bind("lt", "urn:lt:onto:")

    # Create a namespace object for the Friend of a friend namespace.
    LT = Namespace("urn:lt:onto:")

    # Add triples using store's add method.
    """for user in User.objects.all():
        person = URIRef("urn:lt:members:%s" % (user.username))
        g.add((person, RDF.type, LT["Person"]))
        g.add((person, LT["nick"], Literal(user.username)))
        g.add((person, LT["firstname"], Literal(user.first_name)))
        g.add((person, LT["lastname"], Literal(user.last_name)))
        g.add((person, LT["name"], Literal("%s %s" % (user.first_name, user.last_name))))
    """
    g.parse(data=data, format="n3")
    return HttpResponse(g.serialize(format=format))
