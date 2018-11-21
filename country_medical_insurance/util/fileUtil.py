from selenium import webdriver

def read_time_out_url():
    lines = []
    with open("E:\\spilder\\country_medical_insurance\\country_medical_insurance\\spiders\\time_out_url.txt") as file:
      lines = file.readlines()
      print(lines)

    return lines

def writeFile(self, url, fileName):
    with open(file=fileName, mode="a", encoding="utf-8") as file:
        file.write(url)
        file.write("\n")