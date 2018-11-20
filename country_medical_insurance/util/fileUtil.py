from selenium import webdriver

def read_time_out_url():
    lines = []
    with open("E:\\spilder\\country_medical_insurance\\country_medical_insurance\\spiders\\time_out_url.txt") as file:
      lines = file.readlines()
      print(lines)

    return lines

