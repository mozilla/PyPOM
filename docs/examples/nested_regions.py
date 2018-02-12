from pypom import Region, Page
from selenium.webdriver.common.by import By


class MainPage(Page):

    @property
    def menu1(self):
        root = self.find_element(By.ID, "menu1")
        return Menu(self, root=root)

    @property
    def menu2(self):
        root = self.find_element(By.ID, "menu2")
        return Menu(self, root=root)


class Menu(Region):

    @property
    def entries(self):
        return [Entry(self.page, item) for item in self.find_elements(*Entry.entry_locator)]


class Entry(Region):
    entry_locator = (By.CLASS_NAME, 'entry')

    @property
    def name(self):
        return self.root.text
