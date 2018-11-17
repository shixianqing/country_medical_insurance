import re

reg = ".*)$"
aa = "javascript:commitForECMA\\(callbackC,'content.jsp?tableId=25&tableName=TABLE25&tableView=国产药品&Id=132023',null)"
s = aa.split(",")[1]
print(s)