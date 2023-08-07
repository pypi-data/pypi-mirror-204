# Selenium Kit

Selenium toolkit to download the selenium drivers automatically and to use the selenium drivers with all the necessary functions.

Sample Code

```python
# Import selenium drivers
from selenium-kit import SeleniumDriver

# Create the selenium object
selenium = SeleniumDriver()

# Call the url
url = "https://www.imdb.com/"
selenium.callURL(url)

# Write on the search text field
xpath = "input[@id='suggestion-search']"
element = selenium.elementByXPath(xpath)
selenium.sendKeys(element, preference)

# Click on the first search result
xpath = "div[@class='sc-idXgbr iHkrUj searchform__inputContainer']/div/div/div/ul/li"
movie_search_result = selenium.elementsByXPath(xpath)
sleep(0.5)
selenium.clickOnElement(movie_search_result[0])

# delete the selenium driver
del selenium
```
