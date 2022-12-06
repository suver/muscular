from muscles import JsonRequestBody, JsonResponseBody, XmlResponseBody, MultipartRequestBody, HeaderParameter, \
    CookieParameter, PathParameter, QueryParameter, Numeric, List, RestApi
from muscles import Column, String, Enum
from app.models.user import User

api1 = RestApi(name='ApiV1')


@api1.controller('/test_request',
                 description='Контроллер работы со списком пользователей и пользователями',
                 summary='РО'
                 )
class TestRequest:
    """
    Пользователи
    """

    @api1.action(method='option')
    def option(self, request):
        pass

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
        return {"dd": 12}

    @api1.action(method='post',
                 request=[MultipartRequestBody(description='Form', model=User)],
                 response={
                     200: JsonResponseBody(description='OK', model=User),
                 })
    def post(self, request):
        return {
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

    @api1.action(route="/{id}",
                 method='post',
                 parameters=[
                     PathParameter('id', Numeric, required=True, description='Path ID'),
                 ],
                 request=[MultipartRequestBody(description='Form', model=User)],
                 response={
                     200: JsonResponseBody(description='OK', model=User),
                 })
    def show(self, request, id):
        return {
            "dd": id,
            "json": request.json,
            "forms": request.forms,
            "files": request.files,
            "request": {
                "url": request.url,
            }
        }

    @api1.action(route="/{id}/raw",
                 method='post',
                 parameters=[
                     PathParameter('id', Numeric, required=True, description='Path ID'),
                 ],
                 request=[MultipartRequestBody(description='Form', model=User)],
                 response={
                     200: JsonResponseBody(description='OK', model=User),
                 })
    def show1(self, request, id):
        return {
            "dd": id,
            "raw": request.raw,
            "forms": request.forms,
            "files": request.files,
            "request": {
                "url": request.url,
            }
        }

    @api1.action(request=[
        JsonRequestBody(description='Json', model=Column("name", String, index=True))
    ])
    def put(self, request, id):
        pass

    @api1.action(method='delete')
    def delete(self, request, id):
        pass
