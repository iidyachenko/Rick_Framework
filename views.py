import datetime
from framework import render
from paterns.creation_paterns import Engine, Logger
from paterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main')
routes = {}


# def main_view(request):
#     secret = request.get('secret_key', None)
#     date = datetime.datetime.today()
#     return '200 OK', render('index.html', data=date.strftime("%A %d %B %Y"))


# def about_view(request):
#     return '200 OK', render('contacts.html')


@AppRoute(routes=routes, url='/')
class MainView:
    @Debug(name='Index')
    def __call__(self, request):
        secret = request.get('secret_key', None)
        date = datetime.datetime.today()
        return '200 OK', render('index.html', data=date.strftime("%A %d %B %Y"))


@AppRoute(routes=routes, url='/about/')
class AboutView:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('contacts.html')


@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @Debug(name='study_programs')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=datetime.date.today())


class NotFound404:
    @Debug(name='NotFound')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CourseList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CourseCreate')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CategoryCreate')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
