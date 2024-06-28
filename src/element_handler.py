from modules import *

class Handler:
    def __init__(self, driver):
        self.driver = driver

    def getSelector(self, *keys, index=None):
        selector = index + ") " + locator(*keys) if index else locator(*keys)
        assert selector != '', 'Selector is empty'
        return (By.CSS_SELECTOR, selector)

    @handle_exceptions
    def getText(self, *keys, index=None):
        selector = self.getSelector(*keys, index=index)
        element = self.driver.find_element(*selector)
        element = element.text
        if element == '':
            for _ in range(100):  continue
        return element

    @handle_exceptions
    def getElement(self, *keys, index=None):
        selector = self.getSelector(*keys, index=index)
        element = self.driver.find_element(*selector)
        return element
        
    @handle_exceptions
    def getElements(self, *keys, index=None):
        selector = self.getSelector(*keys, index=index)
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(selector)
        )
        return elements

    @handle_exceptions
    def inputValue(self, *keys, value='', index=None):
        selector = self.getSelector(*keys, index=index)
        value = value or self.value
        element = self.driver.find_element(*selector)
        element.clear()
        element.send_keys(value)

    @handle_exceptions
    def clickElement(self, *keys, index=None):
        selector = self.getSelector(*keys, index=index)
        element = self.driver.find_element(*selector)
        click_highlighter(self.driver, element)

    @handle_exceptions
    def waitClickable(self, *keys, time=600, index=None):
        selector = self.getSelector(*keys, index=index)
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(selector)
        )
        click_highlighter(self.driver, element)

    @handle_exceptions
    def waitElement(self, *keys, time=600, index=None):
        selector = self.getSelector(*keys, index=index)
        element = WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(selector)
        )
        return element
    
    @handle_exceptions
    def waitElementInvis(self, *keys, time=10, index=None):
        selector = self.getSelector(*keys, index=index)
        element = WebDriverWait(self.driver, time).until(
            EC.invisibility_of_element_located(selector)
        )
        return element
    
    @handle_exceptions
    def waitText(self, *keys, time=600, index=None):
        selector = self.getSelector(*keys, index=index)
        element = WebDriverWait(self.driver, time).until(
            EC.text_to_be_present_in_element(selector)
        )
        return element