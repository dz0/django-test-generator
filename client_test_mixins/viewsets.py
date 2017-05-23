from django.core.urlresolvers import reverse

from django.utils.http import urlencode

from .core import TestMixin, TestSingleObjectMixin


class TestListViewsetMixin(TestMixin):

    def _test_list_viewset(self, username):

        url = reverse(self.url_names['viewset'] + '-list')
        response = self.client.get(url, self.get_list_viewset_query_params())

        try:
            self.assertEqual(response.status_code, self.status_map['list_viewset'][username])
        except AssertionError:
            print(
                ('test', 'test_list_viewset'),
                ('username', username),
                ('url',  url),
                ('status_code',  response.status_code),
                ('json',  response.json())
            )
            raise

    def get_list_viewset_query_params(self):
        return {}


class TestRetrieveViewsetMixin(TestMixin):

    def _test_retrieve_viewset(self, username):

        for instance in self.instances:
            instance = self.prepare_retrieve_instance(instance)

            url = reverse(self.url_names['viewset'] + '-detail', args=[instance.pk])
            response = self.client.get(url, self.get_retrieve_viewset_query_params(instance))

            try:
                self.assertEqual(response.status_code, self.status_map['retrieve_viewset'][username])
            except AssertionError:
                print(
                    ('test', 'test_retrieve_viewset'),
                    ('username', username),
                    ('url',  url),
                    ('status_code',  response.status_code),
                    ('json',  response.json())
                )
                raise

    def prepare_retrieve_instance(self, instance):
        return instance

    def get_retrieve_viewset_query_params(self, instance):
        return {}


class TestCreateViewsetMixin(TestSingleObjectMixin):

    def _test_create_viewset(self, username):

        for instance in self.instances:
            instance = self.prepare_create_instance(instance)

            url = reverse(self.url_names['viewset'] + '-list')

            query_params = self.get_create_viewset_query_params()
            if query_params:
                url += '?' + urlencode(query_params)

            data = self.get_instance_as_dict(instance)

            response = self.client.post(url, data)

            try:
                self.assertEqual(response.status_code, self.status_map['create_viewset'][username])
            except AssertionError:
                print(
                    ('test', 'test_create_viewset'),
                    ('username', username),
                    ('url',  url),
                    ('data',  data),
                    ('status_code',  response.status_code),
                    ('json',  response.json())
                )
                raise

    def prepare_create_instance(self, instance=None):
        return instance

    def get_create_viewset_query_params(self):
        return {}


class TestUpdateViewsetMixin(TestSingleObjectMixin):

    def _test_update_viewset(self, username):

        for instance in self.instances:
            instance = self.prepare_update_instance(instance)

            url = reverse(self.url_names['viewset'] + '-detail', args=[instance.pk])

            query_params = self.get_update_viewset_query_params(instance)
            if query_params:
                url += '?' + urlencode(query_params)

            data = self.get_instance_as_json(instance)

            response = self.client.put(url, data, content_type="application/json")

            try:
                self.assertEqual(response.status_code, self.status_map['update_viewset'][username])
            except AssertionError:
                print(
                    ('test', 'test_update_viewset'),
                    ('username', username),
                    ('url',  url),
                    ('data',  data),
                    ('status_code',  response.status_code),
                    ('json',  response.json())
                )
                raise

    def prepare_update_instance(self, instance):
        return instance

    def get_update_viewset_query_params(self, instance):
        return {}


class TestDeleteViewsetMixin(TestSingleObjectMixin):

    restore_instance = True

    def _test_delete_viewset(self, username):

        for instance in self.instances:
            instance = self.prepare_delete_instance(instance)

            url = reverse(self.url_names['viewset'] + '-detail', args=[instance.pk])

            query_params = self.get_delete_viewset_query_params(instance)
            if query_params:
                url += '?' + urlencode(query_params)

            response = self.client.delete(url)

            try:
                self.assertEqual(response.status_code, self.status_map['delete_viewset'][username])

                # save the instance again so we can delete it again later
                if self.restore_instance:
                    instance.save(update_fields=None)
            except AssertionError:
                print(
                    ('test', 'test_delete_viewset'),
                    ('username', username),
                    ('url',  url),
                    ('status_code',  response.status_code)
                )
                raise

    def prepare_delete_instance(self, instance):
        return instance

    def get_delete_viewset_query_params(self, instance):
        return {}


class TestReadOnlyModelViewsetMixin(TestListViewsetMixin,
                                    TestRetrieveViewsetMixin):
    pass


class TestModelViewsetMixin(TestListViewsetMixin,
                            TestRetrieveViewsetMixin,
                            TestCreateViewsetMixin,
                            TestUpdateViewsetMixin,
                            TestDeleteViewsetMixin):
    pass