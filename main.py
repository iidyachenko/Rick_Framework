from wsgiref.simple_server import make_server

import views
from framework import Application

# urlpatterns = {
#     '/': views.main_view,
#     '/about/': views.about_view,
#     '/study_programs/': views.StudyPrograms(),
#     '/courses-list/': views.CoursesList(),
#     '/create-course/': views.CreateCourse(),
#     '/create-category/': views.CreateCategory(),
#     '/category-list/': views.CategoryList(),
#     '/copy-course/': views.CopyCourse()
# }


def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = 'SECRET'


front_controllers = [
    secret_controller
]

application = Application(views.routes, front_controllers)

if __name__ == '__main__':
    with make_server('', 8080, application) as httpd:
        print("Serving on port 8080...")
        httpd.serve_forever()

