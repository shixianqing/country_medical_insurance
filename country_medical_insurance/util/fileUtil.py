from selenium import webdriver

b = webdriver.Chrome()
b.get("http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=25&State=1&bcId=152904713761213296322795806604")
page = b.page_source
print(page)