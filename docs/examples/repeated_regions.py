from pypom import Page, Region
from selenium.webdriver.common.by import By


class Results(Page):
    _result_locator = (By.CLASS_NAME, 'result')

    @property
    def results(self):
        return [self.Result(self, el) for el in self.find_elements(*self._result_locator)]

    class Result(Region):
        _name_locator = (By.CLASS_NAME, 'name')
        _detail_locator = (By.TAG_NAME, 'a')

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        @property
        def detail_link(self):
            return self.find_element(*self._detail_locator).get_property("href")
