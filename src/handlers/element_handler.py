from modules import *

"""
    This class, `Handler`, provides a set of methods to interact with web elements using Selenium WebDriver.
    It simplifies common actions such as getting text, finding elements, clicking elements, and waiting for conditions.

    Methods:
    - __init__: Initializes the Handler instance with a WebDriver instance.
    - getSelector: Constructs a CSS selector based on provided keys and an optional index.
    - getText: Retrieves the text of an element identified by the given keys and index.
    - getElement: Finds and returns a single web element identified by the given keys and index.
    - getElements: Finds and returns a list of web elements identified by the given keys and index.
    - inputValue: Clears an input field and sends a specified value to it, identified by the given keys and index.
    - clickElement: Clicks on an element identified by the given keys and index.
    - waitClickable: Waits until an element identified by the given keys and index is clickable, then highlights and returns it.
    - waitElement: Waits until an element identified by the given keys and index is visible, then returns it.
    - waitElementInvis: Waits until an element identified by the given keys and index is invisible.
    - waitText: Waits until the specified text is present in an element identified by the given keys and index.
"""

class Handler:
    def __init__(self, driver):
        self.driver = driver
        self.modules = Modules(self)

    def getSelector(self, *keys, index=None):
        selector = index + ") " + locator(*keys) if index else locator(*keys)
        assert selector != '', 'Selector is empty'
        return (By.CSS_SELECTOR, selector)

    @handle_exceptions
    def getText(self, *keys, index=None):
        selector = self.getSelector(*keys, index=index)
        for _ in range(100):
            element = self.driver.find_element(*selector)
            element = element.text
            if element != '': break
        assert element != '', 'Element is empty'
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
    def getClassAttrib(self, *keys, index=None):
        selector = self.getSelector(*keys, index=index)
        element = self.driver.find_element(*selector)
        class_name = element.get_attribute('class')
        return class_name

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
        self.modules.click(element)
        return True
    
    @handle_exceptions
    def waitClickable(self, *keys, time=600, index=None):
        selector = self.getSelector(*keys, index=index)
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(selector)
        )
        self.modules.click(element)

    @handle_exceptions
    def waitElement(self, *keys, time=600, index=None):
        selector = self.getSelector(*keys, index=index)
        element = WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(selector)
        )
        return element
    
    @handle_exceptions
    def waitElementInvis(self, *keys, time=600, index=None):
        selector = self.getSelector(*keys, index=index)
        element = WebDriverWait(self.driver, time).until(
            EC.invisibility_of_element_located(selector)
        )
        return element
    
    @handle_exceptions
    def waitText(self, *keys, time=600, index=None, text):
        selector = self.getSelector(*keys, index=index)
        element = WebDriverWait(self.driver, time).until(
            EC.text_to_be_present_in_element(selector, text_=text)
        )
        return element
    
    @handle_exceptions
    def waitJSEvents(self, *keys):
        element = locator(*keys)
        print(f'Element: {element}')
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script(
                f"return !!document.querySelector('{element}:after')"
            )
        )