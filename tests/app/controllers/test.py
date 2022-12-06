from muscles import JsonRequestBody, JsonResponseBody, XmlResponseBody, MultipartRequestBody, HeaderParameter, \
    CookieParameter, PathParameter, QueryParameter, Numeric, List, RestApi
from muscles import Column, String, Enum
from app.models.user import User

api1 = RestApi(name='ApiV1')


@api1.controller('/test',
                 description='Контроллер работы со списком пользователей и пользователями',
                 summary='РО'
                 )
class Test:
    """
    Пользователи
    """

    @api1.action(method='option')
    def option(self, request):
        return {
            "method": request.method,
            "request": {
                "url": request.url,
            }
        }

    @api1.action(method='get',
                 description='1 Контроллер работы со списком пользователей и пользователями',
                 summary='1 РО',
                 response={
                     200: [
                         JsonResponseBody(description='OK', model=User),
                         XmlResponseBody(description='OK'),
                     ],
                     400: JsonResponseBody(description='Error 400'),
                     404: JsonResponseBody(description='Not Found'),
                 })
    def get(self, request):
        return {
            "method": request.method,
            "request": {
                "url": request.url,
            }
        }

    @api1.action(method='post',
                 request=[
                     JsonRequestBody(description='Json', model=User),
                     MultipartRequestBody(description='Form', model=User),
                 ],
                 response={
                     200: JsonResponseBody(description='OK'),
                     400: JsonResponseBody(description='Error 400'),
                     404: JsonResponseBody(description='Not Found'),
                 })
    def post(self, request):
        return {
            "method": request.method,
            "request": {
                "url": request.url,
                "headers": request.headers,
                "query": request.query,
                "content_type": request.content_type,
                "cookies": request.cookies,
                "is_json": request.is_json,
                "forms": request.forms,
                "files": request.files,
                "body": request.body,
            }
        }

    @api1.action(method='delete',
                 request=[
                     JsonRequestBody(description='Json', model=User),
                     MultipartRequestBody(description='Form', model=User),
                 ],
                 response={
                     200: JsonResponseBody(description='OK'),
                     400: JsonResponseBody(description='Error 400'),
                     404: JsonResponseBody(description='Not Found'),
                 })
    def delete(self, request):
        return {
            "method": request.method,
        }

    @api1.action(method='put',
                 request=[
                     JsonRequestBody(description='Json', model=User),
                     MultipartRequestBody(description='Form', model=User),
                 ],
                 response={
                     200: JsonResponseBody(description='OK'),
                     400: JsonResponseBody(description='Error 400'),
                     404: JsonResponseBody(description='Not Found'),
                 })
    def put(self, request):
        return {
            "method": request.method,
        }

    @api1.action(route="/{id}",
                 method='get',
                 parameters=[
                     HeaderParameter('Header', Numeric, required=False, description='Header'),
                     CookieParameter('csrftoken', String, required=False, description='Cookie'),
                     PathParameter('id', Numeric, required=True, description='Path ID'),
                     QueryParameter('query1', List(Enum(enum=['one', 'two'])), required=False,
                                    description='Query1'),
                     QueryParameter('query2', Enum(enum=['one', 'two']), required=False, description='Query2'),
                 ],
                 request=[
                     JsonRequestBody(description='Json', model=User),
                     MultipartRequestBody(description='Form', model=User),
                 ],
                 response={
                     200: [
                         JsonResponseBody(description='OK', model=User),
                         XmlResponseBody(description='OK'),
                     ],
                     400: JsonResponseBody(description='Error 400'),
                     404: JsonResponseBody(description='Not Found'),
                 })
    def show(self, request, id):
        return {
            "id": id,
            "method": request.method,
            "request": {
                "url": request.url,
            }
        }

    @api1.action(route="/{id}",
                 method='post',
                 request=[
                     JsonRequestBody(description='Json', model=Column("name", String, index=True))
                 ])
    def change(self, request, id):
        return {
            "id": id,
            "method": request.method,
            "request": {
                "url": request.url,
            }
        }

    @api1.action(route="/{id}", method='delete')
    def drop(self, request, id):
        return {
            "id": id,
            "method": request.method,
            "request": {
                "url": request.url,
            }
        }
