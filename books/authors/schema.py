import graphene
from django.db.models import Q
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from authors.models import Author, Book


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class Query(graphene.ObjectType):
    books = graphene.List(BookType, search=graphene.String(), limit=graphene.Int())
    book = graphene.Field(BookType, id=graphene.Int())
    authors = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, id=graphene.Int())

    def resolve_books(self, info, **kwargs):
        search = kwargs.get('search')
        limit = kwargs.get('limit')
        qs = Book.objects.all()
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        if limit:
            qs = qs[:limit]
        return qs

    def resolve_book(self, info, id):
        return get_object_or_404(Book, pk=id)

    def resolve_authors(self, info, **kwargs):
        return Author.objects.all()

    def resolve_author(self, info, **kwargs):
        id = kwargs.get('id')
        if id:
            return Author.objects.get(pk=id)
        return None


class CreateAuthor(graphene.Mutation):
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    bio = graphene.String()

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        bio = graphene.String()

    def mutate(self, info, first_name, last_name, bio=None):
        author = Author(first_name=first_name, last_name=last_name, bio=bio)
        author.save()

        return CreateAuthor(
            id=author.id,
            first_name=author.first_name,
            last_name=author.last_name,
            bio=author.bio
        )


class CreateBook(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    author = graphene.Field(AuthorType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        author_id = graphene.Int()

    def mutate(self, info, title, description, author_id=None):
        book = Book(title=title, description=description)
        if author_id:
            book.author_id = author_id
        book.save()
        # raise Exception('something')

        return CreateBook(
            id=book.id,
            title=book.title,
            description=book.description,
            author=book.author
        )


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()
