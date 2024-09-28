from django.urls import resolve, reverse


class UrlTests(object):

    def test_url_status_code(self):
        url = reverse(self.name, kwargs=self.args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_view(self):
        url = reverse(self.name, kwargs=self.args)
        resolved_view = resolve(url).func

        if self.view_class:
            self.assertEqual(resolved_view.view_class, self.view_class)
        elif self.view_func:
            self.assertEqual(
                resolved_view.__name__, self.view_func.__name__
            )  # Compare function names
            self.assertEqual(
                resolved_view.__module__, self.view_func.__module__
            )  # Optionally compare the module

    def test_url_uses_correct_template(self):
        url = reverse(self.name, kwargs=self.args)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)

    def test_url_reverse(self):
        url = reverse(self.name, kwargs=self.args)
        self.assertEqual(url, "/" + self.url)
